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


export type IpcEventDataTypes = string | number | boolean | IpcEventData | IpcEventData[];

export type IpcEventData = {
  [key: string]: IpcEventDataTypes | IpcEventDataTypes[];
}


export interface IpcEventRequest {
  /** Name of the event to send */
  name: string;
  /** The data to send */
  data: IpcEventData;
  /** The timeout for the event in seconds, default is 3 seconds */
  timeout?: number;
}


export interface IpcEventResponse {
  /** The status of the response */
  status: 'success' | 'error';
  /** The response from the main process */
  result?: IpcEventData;
  /** The error message if the status is error */
  error?: string;
}


/**
 * Send an event to the main process
 * @param request The request to send
 * @returns The response from the main process
 * @throws If the main process does not respond or an error occurs
 * @example
 * ```typescript
 * const response = await SendEventIPC({ name: 'my-event', data: { key: 'value' } });
 * console.log(response);
 * ```
*/
export async function SendEventIPC(request: IpcEventRequest): Promise<IpcEventResponse> {
  const { name, data, timeout = 3 } = request;
  try {
    const event_data = JSON.stringify(data);
    if (event_data.length > 1000000) {
      throw new Error('Data is too large');
    }
    // @ts-expect-error window_message is a global function
    const response = await window_message(name, event_data, timeout);
    const { status, result, error } = JSON.parse(response);
    if (status === 'error') {
      throw new Error(error);
    }
    return { status: 'success', result };
  } catch (error: any) {
    console.error(error);
    return { status: 'error', error: error.message || 'An error occurred' };
  }
}
