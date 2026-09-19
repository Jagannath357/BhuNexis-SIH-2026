import React from 'react';
import { Link } from 'react-router-dom';
import { FileQuestion, ArrowRight } from 'lucide-react';

export default function NotFoundPage() {
  return (
    <div className="min-h-screen bg-[var(--bg-main)] text-[var(--text-primary)] flex items-center justify-center p-6">
      <div className="max-w-md w-full bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl p-8 text-center shadow-2xl">
        <div className="w-16 h-16 rounded-2xl bg-amber-500/10 text-amber-500 border border-amber-500/20 flex items-center justify-center mx-auto mb-5 shadow-lg">
          <FileQuestion className="w-8 h-8" />
        </div>
        <h2 className="text-3xl font-extrabold text-[var(--text-primary)] tracking-tight">404 - Page Not Found</h2>
        <p className="text-sm text-[var(--text-secondary)] mt-2">
          The requested page or resource could not be located on the BhuNexis platform.
        </p>

        <Link
          to="/"
          className="mt-6 w-full py-3.5 px-4 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-xl transition-all flex items-center justify-center space-x-2 cursor-pointer shadow-lg shadow-emerald-600/20 inline-flex"
        >
          <span>Return to Homepage</span>
          <ArrowRight className="w-4 h-4" />
        </Link>
      </div>
    </div>
  );
}
