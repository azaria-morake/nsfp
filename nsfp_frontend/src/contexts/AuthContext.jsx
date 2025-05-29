// src/contexts/AuthContext.jsx
import { createContext, useContext, useState, useEffect } from 'react';
import api from '../api/api';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [currentUser, setCurrentUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const loadUser = async () => {
      try {
        const response = await api.get('/api/teams/me/');
        setCurrentUser(response.data);
      } catch (error) {
        console.error('Not authenticated');
      } finally {
        setIsLoading(false);
      }
    };

    loadUser();
  }, []);

  const login = async (username, password) => {
    const response = await api.post('/api/login/', { username, password });
    localStorage.setItem('authToken', response.data.token);
    setCurrentUser(response.data.user);
    return response.data.user;
  };

  const logout = async () => {
    await api.post('/api/logout/');
    localStorage.removeItem('authToken');
    setCurrentUser(null);
  };

  const register = async (teamData) => {
    const response = await api.post('/api/register/', teamData);
    localStorage.setItem('authToken', response.data.token);
    setCurrentUser(response.data.user);
    return response.data.user;
  };

  const value = {
    currentUser,
    isLoading,
    login,
    logout,
    register,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => useContext(AuthContext);