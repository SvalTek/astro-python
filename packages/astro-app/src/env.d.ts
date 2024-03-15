/// <reference path="../.astro/types.d.ts" />
/// <reference types="astro/client" />

interface IpcEventResponse {
  status: 'success' | 'error';
  result: string
}

declare global {
  /** Send an event to the main process */
  function window_message(channel: string, data: string, timeout: number): Promise<IpcEventResponse>
}
