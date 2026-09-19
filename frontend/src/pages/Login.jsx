import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import { Shield, UserCheck, Search, Eye, FileText, Lock, Mail, ArrowRight, Sun, Moon, AlertCircle } from 'lucide-react';

export default function Login() {
  const [selectedRole, setSelectedRole] = useState('CITIZEN');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  const { login } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();

  const roleOptions = [
    { id: 'ADMIN', label: 'Admin', desc: 'System Administrator', icon: Shield, color: 'border-indigo-500/40 text-indigo-500 bg-indigo-500/10' },
    { id: 'OFFICER', label: 'Officer', desc: 'Data Ingestion Specialist', icon: FileText, color: 'border-teal-500/40 text-teal-500 bg-teal-500/10' },
    { id: 'REVIEWER', label: 'Reviewer', desc: 'Human-in-the-Loop Verifier', icon: UserCheck, color: 'border-amber-500/40 text-amber-500 bg-amber-500/10' },
    { id: 'AUDITOR', label: 'Auditor', desc: 'Legal & Compliance Inspector', icon: Eye, color: 'border-cyan-500/40 text-cyan-500 bg-cyan-500/10' },
    { id: 'CITIZEN', label: 'Citizen / Landowner', desc: 'Verified Public Search', icon: Search, color: 'border-emerald-500/40 text-emerald-500 bg-emerald-500/10' },
  ];

  const handleRoleSelect = (roleId) => {
    setSelectedRole(roleId);
    setError(null);
    // Autofill demo email for convenient testing
    if (roleId === 'ADMIN') setEmail('admin@bhunexis.demo');
    else if (roleId === 'OFFICER') setEmail('officer@bhunexis.demo');
    else if (roleId === 'REVIEWER') setEmail('reviewer@bhunexis.demo');
    else if (roleId === 'AUDITOR') setEmail('auditor@bhunexis.demo');
    else setEmail('citizen@bhunexis.demo');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    try {
      const user = await login(email, password, selectedRole);
      // Immediately redirect to correct dashboard
      switch (user.role) {
        case 'ADMIN': navigate('/a/dashboard'); break;
        case 'OFFICER': navigate('/o/dashboard'); break;
        case 'REVIEWER': navigate('/r/dashboard'); break;
        case 'AUDITOR': navigate('/au/dashboard'); break;
        case 'CITIZEN': navigate('/u/dashboard'); break;
        default: navigate('/u/dashboard');
      }
    } catch (err) {
      setError(err?.message || 'Authentication failed. Check your credentials and selected role.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-[var(--bg-main)] text-[var(--text-primary)] flex flex-col justify-between p-4 md:p-8 transition-colors">
      {/* Header */}
      <header className="max-w-6xl mx-auto w-full flex items-center justify-between py-4">
        <Link to="/" className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-500 to-teal-400 flex items-center justify-center font-bold text-white text-xl shadow-lg shadow-emerald-500/20">
            BN
          </div>
          <div>
            <h1 className="font-bold text-xl tracking-tight text-[var(--text-primary)]">BhuNexis</h1>
            <p className="text-xs text-emerald-500 font-semibold">Land Records AI Portal</p>
          </div>
        </Link>
        <button
          onClick={toggleTheme}
          className="p-2.5 rounded-lg bg-[var(--bg-card)] border border-[var(--border-color)] text-[var(--text-primary)] hover:bg-slate-200 dark:hover:bg-slate-700 transition-all cursor-pointer shadow-sm"
        >
          {theme === 'light' ? <Moon className="w-5 h-5" /> : <Sun className="w-5 h-5 text-amber-400" />}
        </button>
      </header>

      {/* Main Login Workspace */}
      <main className="max-w-4xl mx-auto w-full my-auto py-8">
        <div className="text-center mb-8">
          <h2 className="text-3xl font-extrabold text-[var(--text-primary)] tracking-tight">
            Sign In to BhuNexis
          </h2>
          <p className="text-sm text-[var(--text-secondary)] mt-2">
            Select your assigned role to access government land record services
          </p>
        </div>

        {/* 1. Exactly 5 Role Selection Cards */}
        <div className="grid grid-cols-2 md:grid-cols-5 gap-3 mb-8">
          {roleOptions.map((opt) => {
            const Icon = opt.icon;
            const isSelected = selectedRole === opt.id;
            return (
              <button
                key={opt.id}
                type="button"
                onClick={() => handleRoleSelect(opt.id)}
                className={`p-4 rounded-xl border text-left transition-all cursor-pointer flex flex-col justify-between ${
                  isSelected
                    ? 'border-emerald-500 bg-emerald-500/10 ring-2 ring-emerald-500/40 shadow-lg'
                    : 'border-[var(--border-color)] bg-[var(--bg-card)] hover:border-slate-400 dark:hover:border-slate-600'
                }`}
              >
                <div className={`w-8 h-8 rounded-lg border ${opt.color} flex items-center justify-center mb-3`}>
                  <Icon className="w-4 h-4" />
                </div>
                <div>
                  <h4 className="font-bold text-sm text-[var(--text-primary)] leading-tight">{opt.label}</h4>
                  <p className="text-[10px] text-[var(--text-muted)] mt-1 line-clamp-1">{opt.desc}</p>
                </div>
              </button>
            );
          })}
        </div>

        {/* 2. Login Form */}
        <div className="bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl p-6 md:p-8 shadow-xl max-w-lg mx-auto">
          {error && (
            <div className="mb-6 p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-600 dark:text-rose-400 text-xs font-semibold flex items-center space-x-2">
              <AlertCircle className="w-5 h-5 flex-shrink-0 text-rose-500" />
              <span>{error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-[var(--text-secondary)] mb-2">
                Email / Username
              </label>
              <div className="relative">
                <Mail className="w-5 h-5 text-[var(--text-muted)] absolute left-3.5 top-3" />
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="name@bhunexis.demo"
                  className="w-full pl-11 pr-4 py-2.5 rounded-xl border border-[var(--border-color)] bg-[var(--bg-main)] text-[var(--text-primary)] text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 transition-all"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-[var(--text-secondary)] mb-2">
                Password
              </label>
              <div className="relative">
                <Lock className="w-5 h-5 text-[var(--text-muted)] absolute left-3.5 top-3" />
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="w-full pl-11 pr-4 py-2.5 rounded-xl border border-[var(--border-color)] bg-[var(--bg-main)] text-[var(--text-primary)] text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 transition-all"
                />
              </div>
              <p className="text-[11px] text-[var(--text-muted)] mt-1.5">Default demo password: <code className="text-emerald-500 font-mono font-bold">password123</code></p>
            </div>

            <button
              type="submit"
              disabled={submitting}
              className="w-full py-3.5 px-4 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-xl transition-all flex items-center justify-center space-x-2 cursor-pointer shadow-lg shadow-emerald-600/30 disabled:opacity-50"
            >
              {submitting ? (
                <span>Authenticating...</span>
              ) : (
                <>
                  <span>Sign In as {selectedRole}</span>
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </form>

          <div className="mt-6 text-center text-xs text-[var(--text-secondary)] pt-4 border-t border-[var(--border-color)]">
            Are you a Citizen without an account?{' '}
            <Link to="/signup" className="text-emerald-500 font-bold hover:underline">
              Register Here
            </Link>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="text-center text-xs text-[var(--text-muted)] py-4">
        &copy; {new Date().getFullYear()} BhuNexis Land Records Platform. Government of India Certified Security Standard.
      </footer>
    </div>
  );
}
