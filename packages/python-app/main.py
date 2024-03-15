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
import os
print(f"main.py: running in {os.getcwd()}")
from lib.event_manager import EventManager
from lib.window_manager import WindowManager
from event_handlers.message_event import register_message_events
from event_handlers.user_event import register_user_events

# Set the port to use for the webui server (this must be the same as the port used for "site" in astro.config.mjs eg "site": "http://localhost:5000")
PORT = 5000
# Set to True to enable debug output
DEBUG = False

event_manager = EventManager(debug=DEBUG)
window_manager = WindowManager(event_manager, port=PORT, debug=DEBUG)

"""
  Application logic is done through event handlers, which are registered here.
  User event happens on Astro WebUI ===> Registered python event handler is called with the event data ===> Event handler returns data to the WebUI
  Astro awaits the ipc mechanism so registered event handlers should always be marked as async, event handlers should either return a dict or raise an exception.
  The event manager will automatically send the data back to the WebUI as { status: "success", result: event_handler_return_value } or { status: "error", error: event_handler_exception }
  all responses are json encoded. This means you can only return serializable data from event handlers.
"""
register_message_events(event_manager)
register_user_events(event_manager)


def main():
    window_manager.create_window("main", "dist/astro", "index.html")
    window_manager.show_window("main")
    window_manager.start()


if __name__ == "__main__":
    main()
