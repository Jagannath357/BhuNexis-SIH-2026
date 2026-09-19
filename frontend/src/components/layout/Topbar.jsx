import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { useTheme } from '../../context/ThemeContext';
import { Sun, Moon, LogOut, User, Shield } from 'lucide-react';

export default function Topbar() {
  const { user, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <header className="h-16 bg-[var(--bg-card)] border-b border-[var(--border-color)] px-6 flex items-center justify-between sticky top-0 z-30 shadow-sm transition-colors">
      <div className="flex items-center space-x-4">
        <h2 className="text-lg font-bold text-[var(--text-primary)] tracking-tight">
          Government Land Records Digitization Platform
        </h2>
      </div>

      <div className="flex items-center space-x-4">
        {/* Light/Dark Theme Toggle */}
        <button
          onClick={toggleTheme}
          title={`Switch to ${theme === 'light' ? 'Dark' : 'Light'} mode`}
          className="p-2.5 rounded-lg bg-[var(--bg-main)] text-[var(--text-primary)] border border-[var(--border-color)] hover:bg-slate-200 dark:hover:bg-slate-700 transition-all flex items-center justify-center cursor-pointer shadow-sm"
        >
          {theme === 'light' ? (
            <Moon className="w-5 h-5 text-slate-700" />
          ) : (
            <Sun className="w-5 h-5 text-amber-400" />
          )}
        </button>

        {/* User Menu */}
        <div className="relative">
          <button
            onClick={() => setDropdownOpen(!dropdownOpen)}
            className="flex items-center space-x-3 p-1.5 rounded-lg border border-[var(--border-color)] hover:bg-[var(--bg-main)] transition-all cursor-pointer"
          >
            <div className="w-9 h-9 rounded-full bg-emerald-600 text-white flex items-center justify-center font-bold text-sm shadow-md">
              {user?.full_name ? user.full_name.charAt(0).toUpperCase() : 'U'}
            </div>
            <div className="text-left hidden md:block">
              <div className="text-sm font-semibold text-[var(--text-primary)] leading-none">
                {user?.full_name || 'User'}
              </div>
              <div className="text-xs text-[var(--text-secondary)] mt-1 font-medium">
                {user?.role || 'Role'}
              </div>
            </div>
          </button>

          {dropdownOpen && (
            <div
              className="absolute right-0 mt-2 w-56 bg-[var(--bg-card)] border border-[var(--border-color)] rounded-xl shadow-2xl py-2 z-50 text-[var(--text-primary)]"
              onMouseLeave={() => setDropdownOpen(false)}
            >
              <div className="px-4 py-2 border-b border-[var(--border-color)]">
                <p className="text-sm font-bold text-[var(--text-primary)]">{user?.full_name}</p>
                <p className="text-xs text-[var(--text-secondary)] truncate">{user?.email}</p>
              </div>
              <button
                onClick={() => { setDropdownOpen(false); navigate('/profile'); }}
                className="w-full text-left px-4 py-2.5 text-sm hover:bg-[var(--bg-main)] flex items-center space-x-2 text-[var(--text-primary)] cursor-pointer"
              >
                <User className="w-4 h-4 text-emerald-500" />
                <span>My Profile</span>
              </button>
              <button
                onClick={handleLogout}
                className="w-full text-left px-4 py-2.5 text-sm hover:bg-rose-50 dark:hover:bg-rose-950/50 text-rose-600 dark:text-rose-400 flex items-center space-x-2 border-t border-[var(--border-color)] cursor-pointer"
              >
                <LogOut className="w-4 h-4 text-rose-500" />
                <span>Log Out</span>
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
