import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { useToast } from '../hooks/useToast';
import { useTheme } from '../hooks/useTheme';
import { getDefaultDashboardForRole } from '../utils/permissions';
import { FileCheck, Mail, Key, ArrowRight, Shield, User, FileSpreadsheet, Eye, UserCheck, ArrowLeft, Home, Sun, Moon } from 'lucide-react';

export function Login() {
  const { user, login } = useAuth();
  const { addToast } = useToast();
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();
  const location = useLocation();

  const [activeRole, setActiveRole] = useState('CITIZEN');
  const [email, setEmail] = useState('citizen@bhoomiai.demo');
  const [password, setPassword] = useState('Citizen@123');
  const [error, setError] = useState(null);

  // Redirect authenticated user immediately to their dashboard
  useEffect(() => {
    if (user) {
      const target = location.state?.from?.pathname || getDefaultDashboardForRole(user.role);
      navigate(target, { replace: true });
    }
  }, [user, navigate, location]);

  const roleCategories = [
    { role: 'CITIZEN', label: 'Citizen / Landowner', sublabel: 'External User', icon: User, defaultEmail: 'citizen@bhoomiai.demo', defaultPass: 'Citizen@123' },
    { role: 'ADMIN', label: 'Admin', sublabel: 'System Administrator', icon: Shield, defaultEmail: 'admin@bhoomiai.demo', defaultPass: 'Admin@123' },
    { role: 'OFFICER', label: 'Officer', sublabel: 'Data Ingestion Specialist', icon: FileSpreadsheet, defaultEmail: 'officer@bhoomiai.demo', defaultPass: 'Officer@123' },
    { role: 'REVIEWER', label: 'Reviewer', sublabel: 'Human Verifier', icon: UserCheck, defaultEmail: 'reviewer@bhoomiai.demo', defaultPass: 'Reviewer@123' },
    { role: 'AUDITOR', label: 'Auditor', sublabel: 'Legal & Compliance', icon: Eye, defaultEmail: 'auditor@bhoomiai.demo', defaultPass: 'Auditor@123' }
  ];

  const handleRoleSelect = (roleKey) => {
    const cat = roleCategories.find(c => c.role === roleKey);
    setActiveRole(roleKey);
    setError(null);
    if (cat) {
      setEmail(cat.defaultEmail);
      setPassword(cat.defaultPass);
    }
  };

  const handleLogin = (e) => {
    e.preventDefault();
    setError(null);

    const res = login(email, password, activeRole);

    if (res.success) {
      addToast(`Welcome back, ${res.user.name}. Signed in as ${res.user.roleDisplayName}.`, 'success');
      const target = location.state?.from?.pathname || getDefaultDashboardForRole(res.user.role);
      navigate(target, { replace: true });
    } else {
      setError(res.error);
      addToast(res.error, 'error');
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-900 text-slate-900 dark:text-white font-sans flex flex-col justify-between transition-colors">
      <div className="flex-1 flex items-center justify-center p-4 sm:p-6 my-8">
        <div className="w-full max-w-lg bg-white dark:bg-slate-950 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-2xl p-6 sm:p-8 space-y-6 transition-colors">
          {/* Top Bar Navigation */}
          <div className="flex items-center justify-between pb-3 border-b border-slate-200 dark:border-slate-900">
            <Link
              to="/"
              className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-500 dark:text-slate-400 hover:text-sky-600 dark:hover:text-sky-400 transition-colors"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>Back to Home</span>
            </Link>

            <div className="flex items-center gap-3">
              <button
                onClick={toggleTheme}
                aria-label={theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
                className="p-1.5 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-100 dark:bg-slate-900 text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-800 transition-all flex items-center gap-1 text-[11px] font-semibold"
                title={theme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
              >
                {theme === 'dark' ? (
                  <>
                    <Sun className="w-3.5 h-3.5 text-amber-400" />
                    <span>Light</span>
                  </>
                ) : (
                  <>
                    <Moon className="w-3.5 h-3.5 text-slate-600" />
                    <span>Dark</span>
                  </>
                )}
              </button>

              <Link
                to="/"
                className="inline-flex items-center gap-1 text-[11px] text-slate-500 dark:text-slate-400 hover:text-slate-800 dark:hover:text-slate-200 transition-colors"
              >
                <Home className="w-3.5 h-3.5" />
                <span>Landing</span>
              </Link>
            </div>
          </div>

          {/* Header Branding */}
          <div className="text-center">
            <Link to="/" className="inline-flex items-center gap-2 mb-2">
              <div className="w-10 h-10 rounded-xl bg-sky-600 p-2 text-white flex items-center justify-center shadow-lg">
                <FileCheck className="w-6 h-6" />
              </div>
              <span className="font-extrabold text-2xl tracking-tight text-slate-900 dark:text-white">BhuNexis</span>
            </Link>
            <h2 className="text-lg font-bold text-slate-900 dark:text-white">Platform Sign In</h2>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">
              Select your user category to sign in
            </p>
          </div>

          {/* User Categories Selection Options */}
          <div className="space-y-2">
            <label className="block text-[11px] font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">
              Select User Category
            </label>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
              {roleCategories.map(cat => {
                const Icon = cat.icon;
                const isSelected = activeRole === cat.role;
                return (
                  <button
                    key={cat.role}
                    type="button"
                    onClick={() => handleRoleSelect(cat.role)}
                    className={`p-2.5 rounded-xl border text-left transition-all ${
                      isSelected
                        ? 'bg-sky-50 dark:bg-sky-600/20 border-sky-500 text-sky-950 dark:text-white shadow-md ring-1 ring-sky-500'
                        : 'bg-slate-50 dark:bg-slate-900 border-slate-200 dark:border-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-850 hover:text-slate-900 dark:hover:text-slate-200'
                    }`}
                  >
                    <div className="flex items-center gap-1.5">
                      <Icon className={`w-3.5 h-3.5 shrink-0 ${isSelected ? 'text-sky-600 dark:text-sky-400' : 'text-slate-400 dark:text-slate-500'}`} />
                      <span className="font-bold text-[11px] truncate">{cat.label}</span>
                    </div>
                    <span className="text-[9px] text-slate-400 dark:text-slate-400 block mt-0.5 truncate">{cat.sublabel}</span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Error Notice */}
          {error && (
            <div className="p-3 bg-rose-50 dark:bg-rose-950/80 border border-rose-200 dark:border-rose-800 text-rose-800 dark:text-rose-200 rounded-xl text-xs">
              {error}
            </div>
          )}

          {/* Login Credentials Form */}
          <form onSubmit={handleLogin} className="space-y-4 text-xs">
            <div>
              <label className="block text-[11px] font-semibold text-slate-700 dark:text-slate-300 mb-1">Email Address</label>
              <div className="relative">
                <Mail className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 dark:text-slate-500" />
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl pl-9 pr-4 py-2.5 text-xs text-slate-900 dark:text-white placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:border-sky-500"
                />
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between mb-1">
                <label className="block text-[11px] font-semibold text-slate-700 dark:text-slate-300">Password</label>
                <Link to="/forgot-password" className="text-[10px] text-sky-600 dark:text-sky-400 hover:underline">
                  Forgot Password?
                </Link>
              </div>
              <div className="relative">
                <Key className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 dark:text-slate-500" />
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl pl-9 pr-4 py-2.5 text-xs text-slate-900 dark:text-white placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:border-sky-500"
                />
              </div>
            </div>

            <button
              type="submit"
              className="w-full py-3 bg-sky-600 hover:bg-sky-500 text-white font-bold text-xs rounded-xl shadow-lg shadow-sky-600/30 transition-all flex items-center justify-center gap-2"
            >
              <span>Sign In as {roleCategories.find(c => c.role === activeRole)?.label || activeRole}</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </form>

          {/* Footer Signup Link */}
          <div className="text-center border-t border-slate-200 dark:border-slate-900 pt-4 text-xs text-slate-500 dark:text-slate-400">
            Don't have an account?{' '}
            <Link to="/signup" className="text-sky-600 dark:text-sky-400 font-semibold hover:underline">
              Request Portal Access
            </Link>
          </div>
        </div>
      </div>

      <footer className="border-t border-slate-200 dark:border-slate-800 py-4 text-center text-xs text-slate-500 dark:text-slate-400">
        BhuNexis — Intelligent Land Record System
      </footer>
    </div>
  );
}


