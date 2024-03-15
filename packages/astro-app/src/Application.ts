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
import type { App } from 'vue';
import * as config from './consts'
import ipcPlugin from './plugins/vue/webui-bridge'


const Application = {
  name: config.APP_NAME,
  version: config.APP_VERSION,
  description: config.APP_DESCRIPTION,
};

const appPlugin = {
  install: (app: any, options: object) => {
    app.config.globalProperties.$Application = (key: any) => {
      // retrieve a nested property in `options` using `key` as the path.
      return key.split('.').reduce((o: any, i: any) => {
        if (o) return o[i]
      }, options)
    }
  }
}

export default (app: App) => {
  app.use(appPlugin, {
    meta: Application
  })
  app.use(ipcPlugin)
};
