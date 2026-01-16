/**
 * Pinia store for user authentication and profile state.
 */

import { defineStore } from 'pinia';
import type { User, UserStatusResponse, UpdateProfileForm } from '@/types';
import { get, put } from '@/services/api';

interface UserState {
  user: User | null;
  isAuthenticated: boolean;
  loading: boolean;
  error: string | null;
}

export const useUserStore = defineStore('user', {
  state: (): UserState => ({
    user: null,
    isAuthenticated: false,
    loading: false,
    error: null,
  }),

  getters: {
    username: (state): string => state.user?.username ?? 'Guest',
    profileImage: (state): string | null => state.user?.profile_image ?? null,
    email: (state): string => state.user?.email ?? '',
  },

  actions: {
    /**
     * Fetch current user status from the API.
     */
    async fetchUser(): Promise<void> {
      this.loading = true;
      this.error = null;
      try {
        const response = await get<UserStatusResponse>('/api/user/status/');
        this.user = response.user;
        this.isAuthenticated = response.authenticated;
      } catch (err) {
        this.error = err instanceof Error ? err.message : 'Failed to fetch user';
        this.isAuthenticated = false;
        this.user = null;
      } finally {
        this.loading = false;
      }
    },

    /**
     * Update the current user's profile.
     */
    async updateProfile(data: UpdateProfileForm): Promise<void> {
      this.loading = true;
      this.error = null;
      try {
        let body: FormData | UpdateProfileForm;
        
        if (data.profile_image) {
          const formData = new FormData();
          if (data.email) formData.append('email', data.email);
          if (data.date_of_birth) formData.append('date_of_birth', data.date_of_birth);
          formData.append('profile_image', data.profile_image);
          body = formData;
        } else {
          body = data;
        }
        
        const updatedUser = await put<User>('/api/profile/', body);
        this.user = updatedUser;
      } catch (err) {
        this.error = err instanceof Error ? err.message : 'Failed to update profile';
        throw err;
      } finally {
        this.loading = false;
      }
    },

    /**
     * Logout the user (redirect to logout page).
     */
    logout(): void {
      window.location.href = '/logout/';
    },

    /**
     * Clear any error messages.
     */
    clearError(): void {
      this.error = null;
    },
  },
});
