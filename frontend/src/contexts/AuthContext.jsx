import React, { createContext, useContext, useState, useEffect } from 'react';
import { authAPI } from '../api/services';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState(localStorage.getItem('token'));

  useEffect(() => {
    // Check if user is logged in on app start
    if (token) {
      getCurrentUser();
    } else {
      setLoading(false);
    }
  }, [token]);

  const getCurrentUser = async () => {
    try {
      const userData = await authAPI.getCurrentUser();
      setUser(userData);
    } catch (error) {
      console.error('Failed to get current user:', error);
      // Token might be expired or invalid
      logout();
    } finally {
      setLoading(false);
    }
  };

  const login = async (email, password) => {
    try {
      const response = await authAPI.login(email, password);
      
      // Store token and user data
      localStorage.setItem('token', response.access_token);
      setToken(response.access_token);
      setUser(response.user);
      
      return { success: true, user: response.user };
    } catch (error) {
      console.error('Login failed:', error);
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Login failed. Please try again.' 
      };
    }
  };

  const registerHomeowner = async (registrationData) => {
    try {
      const userData = await authAPI.registerHomeowner(registrationData);
      return { success: true, user: userData };
    } catch (error) {
      console.error('Registration failed:', error);
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Registration failed. Please try again.' 
      };
    }
  };

  const registerTradesperson = async (registrationData) => {
    try {
      const userData = await authAPI.registerTradesperson(registrationData);
      return { success: true, user: userData };
    } catch (error) {
      console.error('Registration failed:', error);
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Registration failed. Please try again.' 
      };
    }
  };

  const updateProfile = async (profileData) => {
    try {
      const updatedUser = await authAPI.updateProfile(profileData);
      setUser(updatedUser);
      return { success: true, user: updatedUser };
    } catch (error) {
      console.error('Profile update failed:', error);
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Profile update failed. Please try again.' 
      };
    }
  };

  const updateUser = (userData) => {
    setUser(userData);
  };

  const loginWithToken = (token, userData) => {
    localStorage.setItem('token', token);
    setToken(token);
    setUser(userData);
  };

  const logout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
  };

  const isAuthenticated = () => {
    // If we're still loading and have a token, assume authenticated
    // This prevents the race condition where token exists but user data hasn't loaded yet
    if (loading && token) {
      return true;
    }
    // Normal check: both user and token must be present
    return !!user && !!token;
  };

  // Enhanced authentication check that considers loading state
  const isUserAuthenticated = () => {
    // More robust check that considers both user data and loading state
    if (loading && token) {
      return true; // Assume authenticated if we have token and still loading
    }
    return !!user && !!token && !loading;
  };

  const isHomeowner = () => {
    return user?.role === 'homeowner';
  };

  const isTradesperson = () => {
    return user?.role === 'tradesperson';
  };

  const isActive = () => {
    return user?.status === 'active';
  };

  const value = {
    user,
    loading,
    token,
    login,
    loginWithToken,
    logout,
    registerHomeowner,
    registerTradesperson,
    updateProfile,
    updateUser,
    isAuthenticated,
    isHomeowner,
    isTradesperson,
    isActive,
    getCurrentUser
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};