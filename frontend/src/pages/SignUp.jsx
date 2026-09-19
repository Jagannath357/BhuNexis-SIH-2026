import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import { User, Mail, Lock, Phone, ArrowRight, Sun, Moon, AlertCircle, CheckCircle } from 'lucide-react';

export default function SignUp() {
  const [fullName, setFullName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [phone, setPhone] = useState('');
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  const { signup } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      await signup(fullName, email, password, phone);
      setSuccess(true);
      setTimeout(() => {
        navigate('/login');
      }, 2000);
    } catch (err) {
      setError(err?.message || 'Registration failed. Check details and try again.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-[var(--bg-main)] text-[var(--text-primary)] flex flex-col justify-between p-4 md:p-8 transition-colors">
      <header className="max-w-6xl mx-auto w-full flex items-center justify-between py-4">
        <Link to="/" className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-500 to-teal-400 flex items-center justify-center font-bold text-white text-xl shadow-lg shadow-emerald-500/20">
            BN
          </div>
          <div>
            <h1 className="font-bold text-xl tracking-tight text-[var(--text-primary)]">BhuNexis</h1>
            <p className="text-xs text-emerald-500 font-semibold">Citizen Land Portal</p>
          </div>
        </Link>
        <button
          onClick={toggleTheme}
          className="p-2.5 rounded-lg bg-[var(--bg-card)] border border-[var(--border-color)] text-[var(--text-primary)] hover:bg-slate-200 dark:hover:bg-slate-700 transition-all cursor-pointer shadow-sm"
        >
          {theme === 'light' ? <Moon className="w-5 h-5" /> : <Sun className="w-5 h-5 text-amber-400" />}
        </button>
      </header>

      <main className="max-w-md mx-auto w-full my-auto py-8">
        <div className="text-center mb-6">
          <h2 className="text-3xl font-extrabold text-[var(--text-primary)] tracking-tight">Citizen Registration</h2>
          <p className="text-sm text-[var(--text-secondary)] mt-2">
            Create a citizen account to search verified land records & submit grievances
          </p>
        </div>

        <div className="bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl p-6 md:p-8 shadow-xl">
          {error && (
            <div className="mb-5 p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-600 dark:text-rose-400 text-xs font-semibold flex items-center space-x-2">
              <AlertCircle className="w-5 h-5 flex-shrink-0 text-rose-500" />
              <span>{error}</span>
            </div>
          )}

          {success && (
            <div className="mb-5 p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-600 dark:text-emerald-400 text-xs font-semibold flex items-center space-x-2">
              <CheckCircle className="w-5 h-5 flex-shrink-0 text-emerald-500" />
              <span>Account created successfully! Redirecting to login...</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-[var(--text-secondary)] mb-1.5">
                Full Name
              </label>
              <div className="relative">
                <User className="w-5 h-5 text-[var(--text-muted)] absolute left-3.5 top-3" />
                <input
                  type="text"
                  required
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  placeholder="Ramesh Chandra Das"
                  className="w-full pl-11 pr-4 py-2.5 rounded-xl border border-[var(--border-color)] bg-[var(--bg-main)] text-[var(--text-primary)] text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 transition-all"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-[var(--text-secondary)] mb-1.5">
                Email Address
              </label>
              <div className="relative">
                <Mail className="w-5 h-5 text-[var(--text-muted)] absolute left-3.5 top-3" />
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="citizen@example.com"
                  className="w-full pl-11 pr-4 py-2.5 rounded-xl border border-[var(--border-color)] bg-[var(--bg-main)] text-[var(--text-primary)] text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 transition-all"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-[var(--text-secondary)] mb-1.5">
                Mobile Phone
              </label>
              <div className="relative">
                <Phone className="w-5 h-5 text-[var(--text-muted)] absolute left-3.5 top-3" />
                <input
                  type="tel"
                  value={phone}
                  onChange={(e) => setPhone(e.target.value)}
                  placeholder="9876543210"
                  className="w-full pl-11 pr-4 py-2.5 rounded-xl border border-[var(--border-color)] bg-[var(--bg-main)] text-[var(--text-primary)] text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 transition-all"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-[var(--text-secondary)] mb-1.5">
                Password
              </label>
              <div className="relative">
                <Lock className="w-5 h-5 text-[var(--text-muted)] absolute left-3.5 top-3" />
                <input
                  type="password"
                  required
                  minLength={6}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="w-full pl-11 pr-4 py-2.5 rounded-xl border border-[var(--border-color)] bg-[var(--bg-main)] text-[var(--text-primary)] text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 transition-all"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={submitting}
              className="w-full py-3.5 px-4 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-xl transition-all flex items-center justify-center space-x-2 cursor-pointer shadow-lg shadow-emerald-600/30 disabled:opacity-50 mt-2"
            >
              {submitting ? (
                <span>Creating Account...</span>
              ) : (
                <>
                  <span>Create Citizen Account</span>
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </form>

          <div className="mt-6 text-center text-xs text-[var(--text-secondary)] pt-4 border-t border-[var(--border-color)]">
            Already have an account?{' '}
            <Link to="/login" className="text-emerald-500 font-bold hover:underline">
              Sign In
            </Link>
          </div>
        </div>
      </main>

      <footer className="text-center text-xs text-[var(--text-muted)] py-4">
        &copy; {new Date().getFullYear()} BhuNexis Citizen Portal. Government of India Certified Security Standard.
      </footer>
    </div>
  );
}
