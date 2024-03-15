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
from webui import webui
from typing import Optional, TypedDict, Callable
from lib.event_manager import EventManager, EventRequest
import json as JSON

class WindowOptions(TypedDict):
    root_folder: str
    index_html: Optional[str]


class Window(TypedDict):
    name: str
    window: webui.window
    options: WindowOptions


class WindowManager:
    windows: list[Window]

    def __init__(self, event_manager: EventManager, port = 5000,  debug: bool = False):
        """Initialize the WindowManager.
        Define the port to use for the webui server.
        Optionally set debug to True to enable debug output.
        """
        self.event_manager = event_manager
        self.debug = debug
        self.port = port
        # Initialize window list and other necessary state variables here
        self.windows = []

    def create_window(self, name, root_folder: str, index_html: Optional[str] = None):
        """Create and configure the window.
        Note: This method might need to be modified to run in the WindowManager's thread depending on how webui handles thread safety.
        """
        new_window = {
            "name": name,
            "options": {"root_folder": root_folder, "index_html": index_html},
        }
        window = webui.window()
        window.set_root_folder(root_folder)
        window.set_port(self.port)
        window.bind("window_message", self.handle_window_message)
        new_window["window"] = window
        self.windows.append(new_window)
        return new_window

    def handle_window_message(self, e: webui.event):
        """Handle incoming window messages, dispatching them to the event_manager."""
        event_name = e.window.get_str(e, 0)
        event_data = e.window.get_str(e, 1)
        event_timeout = e.window.get_int(e, 2) # Optional timeout in seconds
        self.debug and print(f"Dispatching Window Event: {event_name}")
        event = EventRequest(name=event_name, data=event_data)
        result = self.event_manager.dispatch(event, timeout=event_timeout or 3)
        return JSON.dumps(result)

    def get_window(self, name):
        """Get the window with the given name."""
        for window in self.windows:
            if window["name"] == name:
                return window
        return None

    def show_window(self, name):
        """Shows the window with the given name."""
        window = self.get_window(name)
        if window:
            url = window["options"].get("index_html")
            self.debug and print(f"Showing window {name} with url {url}")
            window["window"].show(url)
        else:
            raise ValueError(f"Window {name} not found")

    def start(self, on_exit: Optional[Callable[[], None]] = None):
        """Starts the WindowManager thread, blocking until the webui.wait() thread exits."""
        self.debug and print("Starting WindowManager thread")
        webui.wait()
        if on_exit:
            self.debug and print("Running on_exit callback")
            on_exit()
        self.debug and print("WindowManager thread exited")

    def stop(self):
        """Stops the webui.wait() thread, allowing the program to exit."""
        webui.stop()
        self.debug and print("Stopped WindowManager thread")

    def bind(self, event_name: str, handler: Callable):
        """Binds an event handler to the event_manager, events are global to all windows."""
        self.event_manager.register(event_name, handler)

    def unbind(self, event_name: str, handler: Callable):
        """Unbinds an event handler from the event_manager."""
        self.event_manager.unregister(event_name, handler)
