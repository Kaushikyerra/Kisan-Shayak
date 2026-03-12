import { create } from 'zustand';

type AuthState = {
  isAuthenticated: boolean;
  hasOnboarded: boolean;
  userName: string;
  completeOnboarding: () => void;
  login: (name: string) => void;
  logout: () => void;
};

export const useAuthStore = create<AuthState>((set) => ({
  isAuthenticated: false,
  hasOnboarded: false,
  userName: 'Farmer',
  completeOnboarding: () => set({ hasOnboarded: true }),
  login: (name) => set({ isAuthenticated: true, userName: name }),
  logout: () => set({ isAuthenticated: false }),
}));
