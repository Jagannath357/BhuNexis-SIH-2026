import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import { AppContext } from '../../context/AppContext';
import { DashboardLayout } from '../../components/DashboardLayout';
import { StatCard } from '../../components/StatCard';
import { LandRecordTable } from '../../components/LandRecordTable';
import { FileCheck, Clock, AlertTriangle, AlertCircle, CheckCircle2, Shield } from 'lucide-react';

export function ReviewerDashboard() {
  const { records } = useContext(AppContext);

  const reviewPendingRecords = records.filter(r => 
    r.verificationStatus === 'UNDER REVIEW' || 
    r.verificationStatus === 'LOW CONFIDENCE' || 
    r.verificationStatus === 'CONFLICT'
  );

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200 dark:border-slate-800 pb-4">
          <div>
            <span className="text-[10px] font-extrabold uppercase tracking-widest text-amber-700 dark:text-amber-300 bg-amber-100 dark:bg-amber-950/80 px-2.5 py-0.5 rounded border border-amber-200 dark:border-amber-800">
              Human-in-the-Loop Verification
            </span>
            <h1 className="text-2xl font-extrabold text-slate-900 dark:text-white tracking-tight mt-1">
              Human Verification Center
            </h1>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              Resolve low-confidence character extractions, review boundary conflicts, and certify validated land information.
            </p>
          </div>

          <Link
            to="/r/review"
            className="px-5 py-2.5 bg-amber-600 hover:bg-amber-500 text-white font-bold text-xs rounded-xl shadow-lg transition-colors flex items-center gap-2"
          >
            <FileCheck className="w-4 h-4" />
            <span>Open Review Queue</span>
          </Link>
        </div>

        {/* REVIEWER STAT CARDS */}
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
          <StatCard title="Pending Review" value="24" subtitle="Requires certification" icon={Clock} color="amber" />
          <StatCard title="Low Confidence" value="12" subtitle="OCR character check" icon={AlertTriangle} color="amber" />
          <StatCard title="Conflicts" value="7" subtitle="GIS boundary flag" icon={AlertCircle} color="rose" />
          <StatCard title="GIS Verification" value="5" subtitle="Spatial match pending" icon={Shield} color="blue" />
          <StatCard title="Verified Today" value="18" subtitle="Approved patta records" icon={CheckCircle2} color="emerald" />
          <StatCard title="Accuracy Rate" value="96.4%" subtitle="Verification precision" icon={CheckCircle2} color="emerald" />
        </div>

        {/* Priority Review Queue Table */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-bold text-slate-900 dark:text-white uppercase tracking-wider">
              Priority Human Review Queue
            </h3>
            <span className="text-xs text-amber-700 dark:text-amber-300 font-semibold bg-amber-50 dark:bg-amber-950/60 px-2.5 py-0.5 rounded border border-amber-200 dark:border-amber-800">
              {reviewPendingRecords.length} Pending Records
            </span>
          </div>

          <LandRecordTable records={reviewPendingRecords} role="REVIEWER" />
        </div>
      </div>
    </DashboardLayout>
  );
}
