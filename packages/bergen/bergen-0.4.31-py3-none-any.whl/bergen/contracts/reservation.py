from asyncio.futures import Future
from bergen.messages.postman.reserve.reserve_transition import ReserveState
from bergen import messages
from bergen.contracts.exceptions import AssignmentException
from bergen.registries.client import get_current_client
from bergen.schema import Node, NodeType
from bergen.monitor import Monitor, current_monitor
from bergen.messages.postman.reserve.params import ReserveParams
from bergen.messages import *
from bergen.utils import *
from rich.table import Table
from rich.panel import Panel
import asyncio
import logging


logger = logging.getLogger(__name__)


class Reservation:

    def __init__(self, node: Node, provision: str = None, loop=None, monitor: Monitor = None, ignore_node_exceptions=False, enter_on=[ReserveState.ACTIVE], exit_on=[ReserveState.ERROR, ReserveState.CANCELLED], bounced=None, **params) -> None:
        bergen = get_current_client()
        self._postman = bergen.getPostman()

        self.node = node
        self.params = ReserveParams(**params)
        self.monitor = monitor or current_monitor.get()
        self.ignore_node_exceptions = ignore_node_exceptions
        self.state_hook = None
        self.exit_states = exit_on
        self.enter_states = enter_on
        self.provision = provision

        self.bounced = bounced # with_bounced allows us forward bounced checks

        if self.bounced:
            assert "can_forward_bounce" in bergen.auth.scopes, "In order to use with_bounced forwarding you need to have the can_forward_bounced scope"

        if self.monitor:
            self.monitor.addRow(self.build_panel())
            self.log = lambda level, message: self.table.add_row(level, message)
            self.on_progress = lambda message, level: self.log(f"[magenta]{level}", message) if self.monitor.progress else None
        else:
            self.log = lambda level, message: logger.info(message)
            self.on_progress = None


        self.in_sync = False
        self.loop = loop or asyncio.get_event_loop()
        # Status
        self.running = False
        self.reservation = None
        self.critical_error = None
        self.recovering = False #TODO: Implement

        pass
    
    def build_panel(self):
        heading_information = Table.grid(expand=True)
        heading_information.add_column()
        heading_information.add_column(style="green")

        reserving_table = Table(title=f"[bold green]Reserving on ...", show_header=False)
        for key, value in self.params.dict().items():
            reserving_table.add_row(key, str(value))

        heading_information.add_row(self.node.__rich__(), reserving_table)

        self.table = Table()
        self.table.add_column("Level")
        self.table.add_column("Message")

        columns = Table.grid(expand=True)
        columns.add_column()

        columns.add_row(heading_information)
        columns.add_row(self.table)

        return Panel(columns, title="Reservation")


    async def assign_async(self, *args, bypass_shrink=False, bypass_expand=False, persist=True, **kwargs):
        assert self.node.type == NodeType.FUNCTION, "You cannot assign to a Generator Node, use the stream Method!"
        self.log("[green]ASSIGN",f"Assigning!")
        if self.critical_error is not None:
            
            self.log("[red]ASSIGN",f"Contract is broken and we can not assign. Exiting!")
        try:
            shrinked_args, shrinked_kwargs = await shrinkInputs(self.node, args, kwargs) if not bypass_shrink else (args, kwargs)
            return_message = await self._postman.assign(self.reservation, shrinked_args, shrinked_kwargs=shrinked_kwargs, on_progress=self.on_progress, persist=persist, bounced=self.bounced)
            outs = await expandOutputs(self.node, return_message.data.returns) if not bypass_expand else return_message.data.returns
            return outs

        except AssignmentException as e:
            self.log("[red]ASSIGN", str(e))
            if not self.ignore_node_exceptions: raise e
        except Exception as e:
            raise e


    



    async def stream(self, *args, bypass_shrink=False, bypass_expand=False, persist=True, **kwargs):
        assert self.node.type == NodeType.GENERATOR, "You cannot stream a Function Node, use the assign Method!"
        if self.critical_error is not None:
            self.log("[red]ASSIGN",f"Contract is broken and we can not assign. Exiting!")
        try:
            shrinked_args, shrinked_kwargs = await shrinkInputs(self.node, args, kwargs) if not bypass_shrink else (args, kwargs) 
            async for message in self._postman.assign_stream(self.reservation, shrinked_args, serialized_kwargs=shrinked_kwargs, with_progress=True, persist=persist, bounced=self.bounced):

                if isinstance(message, AssignYieldsMessage):
                    outs = await expandOutputs(self.node, message.data.returns) if not bypass_expand else message.data.returns
                    yield outs

                if isinstance(message, AssignLogMessage):
                    if self.on_progress: self.on_progress(message.data.message, message.data.level)
                
                if isinstance(message, AssignCriticalMessage):
                    raise AssignmentException(message.data.type + message.data.message)

                if isinstance(message, AssignDoneMessage):
                    self.log("ASSIGN", f'Done')
                    break

        except asyncio.CancelledError as e:
            self.log("ASSIGN", "Cancelled")
            print("Canncelled")
            raise e

        except AssignmentException as e:
            self.log("ASSIGN", str(e))
            if not self.ignore_node_exceptions: raise e

        
    

    async def contract_worker(self):
        self.running = True
        try:
            async for message in self._postman.reserve_stream(node_id=self.node.id, provision=self.provision, params_dict=self.params.dict(), with_progress=True, bounced=self.bounced):
                # Before here because Reserve Critical is actually an ExceptionMessage
                #TODO: Undo this

                if isinstance(message, ReserveLogMessage):
                    self.log(f'[green]{message.data.level.value}', message.data.message)

                elif isinstance(message, ReserveCriticalMessage):
                    # Reserve Errors are Errors that happen during the Reservation
                    self.log(f'[red]EXCEPTION', message.data.message)
                    self.critical_error = message

                elif isinstance(message, ExceptionMessage):
                    # Porotocol Exceptions are happening on the start
                    self.contract_started.set_exception(message.toException())
                    return

                elif isinstance(message, ReserveTransitionMessage):
                    # Once we acquire a reserved resource our contract (the inner part of the context can start)
                    state = message.data.state

                    if self.state_hook: await self.state_hook(self, message.data.state)
                    
                    if state in self.exit_states:
                        self.critical_error = f"Exited because Reservation Changed to State {state}: {message.data.message}"

                    if state in self.enter_states:
                        pass#self.contract_started.set_result(message.meta.reference)


                #elif isinstance(message, ReserveDoneMessage):
                    # Once we acquire a reserved resource our contract (the inner part of the context can start)
                #    self.contract_started.set_result(message.meta.reference)

                elif isinstance(message, ReserveActiveMessage):
                    # Once we acquire a reserved resource our contract (the inner part of the context can start)
                    self.contract_started.set_result(message.meta.reference)
        
        except asyncio.CancelledError as e:
            self.log("[green]DONE", "Unreserved Sucessfully")

 
    def cancel_reservation(self, future: Future):
        if future.exception():
            self.log("[red]Exception", str(future.exception()))
            raise future.exception()
        elif future.done():
            return


    async def start(self, state_hook = None):
        self.state_hook = state_hook
        return await self.__aenter__()

    async def end(self):
        await self.__aexit__()

    async def __aenter__(self):
        self.contract_started = self.loop.create_future()
        self.worker_task = self.loop.create_task(self.contract_worker())

        self.worker_task.add_done_callback(self.cancel_reservation)
        self.reservation = await self.contract_started
        self.log(f"[green]STARTED",f"Established Reservation {self.reservation}")
        return self

    async def __aexit__(self, *args, **kwargs):
        if not self.worker_task.done():
            #await self._postman.unreserve(reservation=self.reservation, on_progress=self.on_progress)
            self.worker_task.cancel()
            try:
                await self.worker_task
            except asyncio.CancelledError:
                self.log("[green]EXIT", "Gently Exiting Reservation")
            except Exception as e:
                self.log(f"[red]CRITICAL", f"Exitigin with {str(e)}")
    
    def assign(self, *args, bypass_shrink=False, bypass_expand=False, persist=True, **kwargs):
        if self.in_sync:
            return self.loop.run_until_complete(self.assign_async(*args, bypass_shrink=bypass_shrink, bypass_expand=bypass_expand, persist=persist, **kwargs))
        else:
            return self.assign_async(*args, bypass_shrink=bypass_shrink, bypass_expand=bypass_expand, persist=persist, **kwargs)

    def __enter__(self):
        self.in_sync = True
        future = self.loop.run_until_complete(self.__aenter__())
        return future

    def __exit__(self, *args, **kwargs):
        return  self.loop.run_until_complete(self.__aexit__(*args, **kwargs))



    




       