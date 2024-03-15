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
import sys
import logging
from webui import webui


"""
    WebUI struggles to find its library when bundled with PyInstaller. There's better ways to handle this,
    but for now just monkey-patch the loader to point to the correct path.
"""


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - ["pyInstaller hook"] %(levelname)s - %(message)s',
)


# Define the base directory for bundled resources in a PyInstaller package
BUNDLE_DIR = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))


def webui_monkey_patch():
    # Determine the name of the WebUI library based on the platform
    if sys.platform.startswith("linux"):
        lib_name = "webui-linux-gcc-x64/webui-2.so"
    elif sys.platform.startswith("win"):
        lib_name = "webui-windows-msvc-x64/webui-2.dll"
    else:
        logging.error("Unsupported platform for WebUI library.")
        return

    lib_path = os.path.join(BUNDLE_DIR, lib_name)
    if not os.path.exists(lib_path):
        logging.error(f"WebUI library not found at expected path: {lib_path}")
        return

    # Define a patched version of the WebUI library loader, just return our known path.
    def patched_get_library_path():
        logging.debug(
            f"[patched] returning library path: {lib_path} in webui._get_library_path"
        )
        return lib_path

    logging.debug(f"Monkey-patching WebUI to load library from: {lib_path}")
    webui._get_library_path = patched_get_library_path


# Apply the patch
webui_monkey_patch()
