import { create } from 'zustand';
import { supabase } from '../services/supabase';

type AuthState = {
  userEmail: string | null;
  signIn: (email: string) => Promise<void>;
  signOut: () => Promise<void>;
  hydrate: () => Promise<void>;
};

export const useAuthStore = create<AuthState>((set) => ({
  userEmail: null,
  signIn: async (email) => {
    const { error } = await supabase.auth.signInWithOtp({ email });
    if (error) throw error;
    set({ userEmail: email });
  },
  signOut: async () => {
    await supabase.auth.signOut();
    set({ userEmail: null });
  },
  hydrate: async () => {
    const { data } = await supabase.auth.getUser();
    set({ userEmail: data.user?.email ?? null });
  }
}));
