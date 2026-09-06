import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useToast } from '../hooks/useToast';
import { useTheme } from '../hooks/useTheme';
import { DisclaimerBanner } from '../components/DisclaimerBanner';
import { FileCheck, Mail, ArrowLeft, CheckCircle2, Home, Sun, Moon } from 'lucide-react';

export function ForgotPassword() {
  const { addToast } = useToast();
  const { theme, toggleTheme } = useTheme();
  const [email, setEmail] = useState('');
  const [sent, setSent] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setSent(true);
    addToast('Password reset instructions simulated in Demo Mode.', 'info');
  };

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-900 text-slate-900 dark:text-white font-sans flex flex-col justify-between transition-colors">
      <DisclaimerBanner compact={true} />

      <div className="flex-1 flex items-center justify-center p-4 sm:p-6 my-8">
        <div className="w-full max-w-md bg-white dark:bg-slate-950 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-2xl p-6 sm:p-8 space-y-6 transition-colors">
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

          <div className="text-center">
            <Link to="/" className="inline-flex items-center gap-2 mb-2">
              <div className="w-9 h-9 rounded-xl bg-sky-600 p-2 text-white flex items-center justify-center">
                <FileCheck className="w-5 h-5" />
              </div>
              <span className="font-extrabold text-2xl tracking-tight text-slate-900 dark:text-white">BhuNexis</span>
            </Link>
            <h2 className="text-lg font-bold text-slate-900 dark:text-white">Password Reset Simulation</h2>
            <p className="text-xs text-slate-500 dark:text-slate-400 mt-1">Enter registered email for demo reset instructions</p>
          </div>

          {sent ? (
            <div className="bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl p-6 text-center space-y-3">
              <div className="w-12 h-12 rounded-full bg-sky-100 dark:bg-sky-500/20 text-sky-600 dark:text-sky-400 flex items-center justify-center mx-auto">
                <CheckCircle2 className="w-6 h-6" />
              </div>
              <h3 className="text-base font-bold text-slate-900 dark:text-white">Reset Instructions Simulated</h3>
              <p className="text-xs text-slate-600 dark:text-slate-300">
                Password reset link simulated for <strong className="text-sky-600 dark:text-sky-400">{email}</strong>. No actual email dispatch occurs in Demo Mode.
              </p>
              <Link
                to="/login"
                className="mt-4 inline-block px-5 py-2 bg-sky-600 hover:bg-sky-500 text-white font-bold text-xs rounded-xl shadow-md"
              >
                Return to Login Page
              </Link>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-4 text-xs">
              <div>
                <label className="block text-[11px] font-semibold text-slate-700 dark:text-slate-300 mb-1">Email Address</label>
                <div className="relative">
                  <Mail className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 dark:text-slate-500" />
                  <input
                    type="email"
                    required
                    placeholder="admin@bhoomiai.demo"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="w-full bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl pl-9 pr-4 py-2.5 text-xs text-slate-900 dark:text-white focus:outline-none focus:border-sky-500"
                  />
                </div>
              </div>

              <button
                type="submit"
                className="w-full py-3 bg-sky-600 hover:bg-sky-500 text-white font-bold text-xs rounded-xl shadow-lg transition-all"
              >
                Send Reset Link (Demo Simulation)
              </button>
            </form>
          )}

          <div className="text-center border-t border-slate-200 dark:border-slate-900 pt-4 text-xs text-slate-500 dark:text-slate-400">
            <Link to="/login" className="text-sky-600 dark:text-sky-400 font-semibold hover:underline inline-flex items-center gap-1">
              <ArrowLeft className="w-3.5 h-3.5" />
              <span>Back to Login Screen</span>
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
