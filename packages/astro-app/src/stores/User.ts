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

import { persistentMap } from '@nanostores/persistent'

export type User = {
  name: string
  avatar?: string
}

const defaultUser: User = {
  name: 'Anonymous',
  avatar: 'https://api.dicebear.com/7.x/adventurer/svg?seed=JohnDoe',
}

const user = persistentMap<User>('user', defaultUser)
export default user

export const setUser = (data: User) => {
  user.set(data)
}

export const setName = (name: string) => {
  user.setKey('name', name)
}

export const setAvatar = (avatar: string) => {
  user.setKey('avatar', avatar)
}

export const resetUser = () => {
  user.set(defaultUser)
}


