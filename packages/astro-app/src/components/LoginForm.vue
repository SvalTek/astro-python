<!--
 Copyright (C) 2024 Theros <https://github.com/therosin>

 This file is part of astro-python.

 astro-python is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 astro-python is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with astro-python.  If not, see <http://www.gnu.org/licenses/>.
-->

<template>
  <div class="login-form-container p-4 max-w-sm mx-auto">
    <h2 class="text-2xl font-bold mb-4">Login</h2>
    <hr class="mb-4">
    <div class="login-message mb-4" v-if="loginMessage">
      {{ loginMessage }}

      <div v-if="currentUserProfile.name">
        <p>Logged in as {{ currentUserProfile.name }}</p>
      </div>

    </div>
    <form @submit.prevent="submitLogin">
      <div class="mb-4">
        <label for="username" class="block text-sm font-medium text-gray-700">Username</label>
        <input type="text" id="username" v-model="loginData.username"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          required>
      </div>
      <div class="mb-4">
        <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
        <input type="password" id="password" v-model="loginData.password"
          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          required>
      </div>
      <div>
        <button type="submit"
          class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">Login</button>
      </div>
    </form>
  </div>
</template>

<script>
import { useStore } from '@nanostores/vue'
import UserStore from '../stores/User';
import { setUser } from '../stores/User';

export default {
  name: 'LoginForm',
  setup() {
    const userProfile = useStore(UserStore);
    return { userProfile };
  },
  data() {
    return {
      loginData: {
        username: '',
        password: '',
      },
      loginMessage: null,
    };
  },
  computed: {
    currentUserProfile() {
      return this.userProfile;
    },
  },
  methods: {
    async submitLogin() {
      try {
        const response = await this.$webui.ipcRequest("user-event", {
          action: "login",
          username: this.loginData.username,
          password: this.loginData.password,
        });

        if (response.status === 'success') {
          const { message, user } = response.result;
          console.log('Login successful:', message);
          setUser(user);
          this.loginMessage = 'Login successful';
        } else {
          console.error('Login failed:', response.result);
          this.loginMessage = 'Login failed';
        }
      } catch (error) {
        console.error('Login request failed:', error);
        this.loginMessage = 'Login request failed';
      }
    },
  },
};
</script>

<style scoped>
/* placeholder */
</style>
