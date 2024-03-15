// Copyright (C) 2024 Theros <https://github.com/therosin>
//
// This file is part of astro-python.
//
// astro-python is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// astro-python is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with astro-python.  If not, see <http://www.gnu.org/licenses/>.
import { SendEventIPC, type IpcEventResponse } from '../../scripts/ipc';

const webui = {
  ipcRequest: (name: string, data: { [key: string]: any }): Promise<IpcEventResponse> => {
    return new Promise((resolve, reject) => {
      SendEventIPC({name, data})
        .then((response: IpcEventResponse) => {
          resolve(response)
        })
        .catch((error: Error) => {
          reject(error)
        })
    })
  }
}


export default {
  install: (app: any) => {
    app.config.globalProperties.$webui = webui
    app.provide('$webui', webui)
  }
}
