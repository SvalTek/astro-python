# Copyright (C) 2024 Theros <https://github.com/therosin>
#
# This file is part of astro-python.
#
# astro-python is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# astro-python is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with astro-python.  If not, see <http://www.gnu.org/licenses/>.
import asyncio
import threading
from typing import Optional, Callable, TypedDict, Dict, Any, Union
from json import dumps, loads

# EventData is a dictionary that can contain any JSON-serializable data.
EventData = Dict[str, Union[str, int, float, bool, list, dict]]


class EventRequest(TypedDict, total=False):
    """Represents an event request to be dispatched."""
    name: str
    data: Optional[EventData] # The data to send with the event.


class EventResponse(TypedDict, total=False):
    """Represents the response to an event request."""
    status: str
    result: Optional[EventData]


EventHandler = Callable[[EventData], Any]


class EventManager:
    """
    Manages events and their handlers.

    Example:
        ```python
        from event_manager import EventManager, EventRequest

        # Create an event manager
        event_manager = EventManager(debug=True)

        # Register an event handler
        async def on_hello(data):
            return f"Hello, {data.get('name')}!"

        event_manager.register("hello", on_hello)

        # Dispatch an event
        event = EventRequest(name="hello", data={"name": "World"})
        response = event_manager.dispatch(event)
        print(response)  # {"status": "success", "result": "Hello, World!"}
        ```
    """


    def __init__(self, debug: bool = False):
        """
        Create a new EventManager instance.

        Parameters:
            debug (bool): Whether to print debug messages to the console.
        """
        self._handlers: Dict[str, EventHandler] = {}
        self.debug = debug
        self.loop = asyncio.new_event_loop()
        self.debug and print("Starting event loop")
        self.thread = threading.Thread(
            target=self.run_async_loop, args=(self.loop,), daemon=True
        )
        self.thread.start()

    def run_async_loop(self, loop):
        """[INTERNAL] Run the asyncio event loop in a separate thread."""
        asyncio.set_event_loop(loop)
        loop.run_forever()

    def register(self, event_name: str, handler: EventHandler):
        """
        Register an event handler.

        Parameters:
            event_name (str): The name of the event to handle.
            handler (EventHandler): The function to call when the event is dispatched.
        """
        self._handlers[event_name] = handler

    def unregister(self, event_name: str):
        """
        Unregister an event handler.

        Parameters:
            event_name (str): The name of the event to unregister.
        """
        del self._handlers[event_name]

    async def dispatch_async(self, event: EventRequest) -> EventResponse:
        """
        Dispatch the event to the appropriate handler.
        Returns the result of the event handler, or raises an error if the event is not handled.

        Parameters:
            event (EventRequest): The event to dispatch.
        """
        event_name = event.get("name")
        event_data = event.get("data")
        event_response: EventResponse = {"status": "unknown", "result": None}

        handler = self._handlers.get(event_name)
        if handler:
            try:
                self.debug and print(f"Dispatching event: {event_name}")
                if event_data is not None:
                    # Convert data to JSON string if necessary
                    event_data_json = (
                        dumps(event_data)
                        if isinstance(event_data, dict)
                        else event_data
                    )
                    self.debug and print(f"Event Data (JSON): {event_data_json}")
                    # Assuming the handler can process a Python dict
                    result = await handler(loads(event_data_json))
                else:
                    result = await handler({})

                self.debug and print(f"Event Handled! Result: {result}")
                event_response["status"] = "success"
                event_response["result"] = result

            except Exception as err:
                self.debug and print(f"Error handling event {event_name}: {err}")
                event_response["status"] = "error"
                event_response["result"] = {"error": str(err)}
        else:
            self.debug and print(f"No handler for event: {event_name}")
            event_response["status"] = "error"
            event_response["result"] = {"error": "No handler for event"}

        return event_response

    def dispatch(
        self, event: EventRequest, timeout: Optional[int] = 3
    ) -> EventResponse:
        """
        Dispatch the event to the appropriate handler.
        Optionally set a timeout for the event to be handled (in seconds).
        Returns the result of the event handler, or raises an error if the event is not handled.

        Parameters:
            event (EventRequest): The event to dispatch.
            timeout (int): The maximum time to wait for the event to be handled (in seconds).
        """
        if not self.loop.is_running():
            raise RuntimeError("Event loop is not running")
        return asyncio.run_coroutine_threadsafe(
            self.dispatch_async(event), self.loop
        ).result(timeout)
