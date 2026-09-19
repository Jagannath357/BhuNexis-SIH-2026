import React from 'react';

export default function StatusBadge({ status }) {
  const getBadgeStyle = (s) => {
    switch (s?.toUpperCase()) {
      case 'VERIFIED':
      case 'APPROVED':
      case 'PASSED':
      case 'RESOLVED':
      case 'HEALTHY':
        return 'bg-emerald-500/10 text-emerald-700 dark:text-emerald-400 border-emerald-500/30';
      case 'PENDING':
      case 'UPLOADED':
      case 'EXTRACTED':
      case 'OCR_PROCESSED':
      case 'VALIDATING':
        return 'bg-amber-500/10 text-amber-700 dark:text-amber-400 border-amber-500/30';
      case 'REVIEW_REQUIRED':
      case 'CONFLICT':
      case 'WARNING':
      case 'HIGH':
        return 'bg-rose-500/10 text-rose-700 dark:text-rose-400 border-rose-500/30';
      case 'REJECTED':
      case 'DEACTIVATED':
      case 'UNHEALTHY':
        return 'bg-red-500/10 text-red-700 dark:text-red-400 border-red-500/30';
      case 'UNAVAILABLE':
        return 'bg-slate-500/10 text-slate-600 dark:text-slate-400 border-slate-500/30';
      default:
        return 'bg-blue-500/10 text-blue-700 dark:text-blue-400 border-blue-500/30';
    }
  };

  return (
    <span className={`px-2.5 py-1 text-xs font-semibold rounded-full border inline-flex items-center gap-1.5 ${getBadgeStyle(status)}`}>
      <span className="w-1.5 h-1.5 rounded-full bg-current" />
      {status || 'UNKNOWN'}
    </span>
  );
}
