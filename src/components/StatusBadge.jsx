import React from 'react';
import { CheckCircle2, Clock, AlertTriangle, AlertCircle, FileText, Loader2, XCircle, UploadCloud } from 'lucide-react';

export function StatusBadge({ status, size = 'md' }) {
  const getBadgeConfig = () => {
    switch (status) {
      case 'VERIFIED':
        return {
          bg: 'bg-emerald-50 dark:bg-emerald-950/80 text-emerald-700 dark:text-emerald-300 border-emerald-200 dark:border-emerald-800',
          icon: CheckCircle2,
          label: 'Verified'
        };
      case 'UNDER REVIEW':
      case 'PENDING':
        return {
          bg: 'bg-amber-50 dark:bg-amber-950/80 text-amber-700 dark:text-amber-300 border-amber-200 dark:border-amber-800',
          icon: Clock,
          label: 'Under Review'
        };
      case 'LOW CONFIDENCE':
        return {
          bg: 'bg-amber-100 dark:bg-amber-900/60 text-amber-800 dark:text-amber-200 border-amber-300 dark:border-amber-700',
          icon: AlertTriangle,
          label: 'Low Confidence'
        };
      case 'CONFLICT':
        return {
          bg: 'bg-rose-50 dark:bg-rose-950/80 text-rose-700 dark:text-rose-300 border-rose-200 dark:border-rose-800',
          icon: AlertCircle,
          label: 'Conflict Flagged'
        };
      case 'EXTRACTED':
        return {
          bg: 'bg-blue-50 dark:bg-blue-950/80 text-blue-700 dark:text-blue-300 border-blue-200 dark:border-blue-800',
          icon: FileText,
          label: 'Extracted'
        };
      case 'PROCESSING':
        return {
          bg: 'bg-indigo-50 dark:bg-indigo-950/80 text-indigo-700 dark:text-indigo-300 border-indigo-200 dark:border-indigo-800',
          icon: Loader2,
          label: 'Processing...',
          spin: true
        };
      case 'REJECTED':
        return {
          bg: 'bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border-slate-300 dark:border-slate-700',
          icon: XCircle,
          label: 'Rejected'
        };
      case 'UPLOADED':
      default:
        return {
          bg: 'bg-slate-100 dark:bg-slate-800/80 text-slate-600 dark:text-slate-400 border-slate-200 dark:border-slate-700',
          icon: UploadCloud,
          label: status || 'Uploaded'
        };
    }
  };

  const config = getBadgeConfig();
  const Icon = config.icon;

  const sizeClasses = size === 'sm' 
    ? 'px-2 py-0.5 text-xs font-medium gap-1' 
    : 'px-2.5 py-1 text-xs font-semibold gap-1.5';

  return (
    <span className={`inline-flex items-center rounded-full border shadow-sm ${config.bg} ${sizeClasses}`}>
      <Icon className={`w-3.5 h-3.5 ${config.spin ? 'animate-spin' : ''}`} />
      <span>{config.label}</span>
    </span>
  );
}
