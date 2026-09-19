import React, { createContext, useContext, useState, useEffect } from 'react';
import authService from '../services/authService';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(() => localStorage.getItem('bhunexis_token') || null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const initAuth = async () => {
      if (token) {
        try {
          const userData = await authService.getCurrentUser();
          setUser(userData);
        } catch (err) {
          console.error("Session restoration failed:", err);
          logout();
        }
      }
      setLoading(false);
    };
    initAuth();
  }, [token]);

  const login = async (email, password, role) => {
    const data = await authService.login(email, password, role);
    setToken(data.access_token);
    setUser(data.user);
    localStorage.setItem('bhunexis_token', data.access_token);
    return data.user;
  };

  const signup = async (fullName, email, password, phone) => {
    const newUser = await authService.signup(fullName, email, password, phone);
    return newUser;
  };

  const logout = async () => {
    try {
      if (token) {
        await authService.logout();
      }
    } catch (e) {
      // ignore
    } finally {
      setUser(null);
      setToken(null);
      localStorage.removeItem('bhunexis_token');
    }
  };

  const updateUser = (updatedData) => {
    setUser((prev) => ({ ...prev, ...updatedData }));
  };

  return (
    <AuthContext.Provider value={{ user, token, role: user?.role, loading, login, signup, logout, updateUser }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
