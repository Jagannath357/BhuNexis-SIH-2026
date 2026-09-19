import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { ShieldAlert, ArrowRight } from 'lucide-react';

export default function AccessDenied() {
  const { role } = useAuth();
  const navigate = useNavigate();
  const [countdown, setCountdown] = useState(3);

  const getRedirectPath = () => {
    switch (role) {
      case 'ADMIN': return '/a/dashboard';
      case 'OFFICER': return '/o/dashboard';
      case 'REVIEWER': return '/r/dashboard';
      case 'AUDITOR': return '/au/dashboard';
      case 'CITIZEN': return '/u/dashboard';
      default: return '/login';
    }
  };

  useEffect(() => {
    const timer = setInterval(() => {
      setCountdown((prev) => {
        if (prev <= 1) {
          clearInterval(timer);
          navigate(getRedirectPath());
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [role, navigate]);

  return (
    <div className="min-h-screen bg-[var(--bg-main)] text-[var(--text-primary)] flex items-center justify-center p-6">
      <div className="max-w-md w-full bg-[var(--bg-card)] border border-rose-500/30 rounded-2xl p-8 text-center shadow-2xl">
        <div className="w-16 h-16 rounded-2xl bg-rose-500/10 text-rose-500 border border-rose-500/20 flex items-center justify-center mx-auto mb-5 shadow-lg shadow-rose-500/10">
          <ShieldAlert className="w-8 h-8" />
        </div>
        <h2 className="text-2xl font-bold text-[var(--text-primary)] tracking-tight">Access Denied</h2>
        <p className="text-sm text-[var(--text-secondary)] mt-2">
          You do not have administrative permission to view this resource.
        </p>

        <div className="mt-6 p-4 rounded-xl bg-[var(--bg-main)] border border-[var(--border-color)] text-xs text-[var(--text-muted)]">
          Redirecting to your authorized dashboard in <span className="font-bold text-rose-500 text-sm">{countdown}</span> seconds...
        </div>

        <button
          onClick={() => navigate(getRedirectPath())}
          className="mt-6 w-full py-3 px-4 bg-emerald-600 hover:bg-emerald-700 text-white font-semibold rounded-xl transition-all flex items-center justify-center space-x-2 cursor-pointer shadow-lg shadow-emerald-600/20"
        >
          <span>Go to Authorized Dashboard</span>
          <ArrowRight className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}
