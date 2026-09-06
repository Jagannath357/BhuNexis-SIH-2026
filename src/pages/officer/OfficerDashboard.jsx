import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import { AppContext } from '../../context/AppContext';
import { DashboardLayout } from '../../components/DashboardLayout';
import { StatCard } from '../../components/StatCard';
import { LandRecordTable } from '../../components/LandRecordTable';
import { 
  UploadCloud, 
  FileText, 
  Clock, 
  AlertTriangle, 
  CheckCircle2, 
  RefreshCw,
  Layers,
  ArrowRight
} from 'lucide-react';

export function OfficerDashboard() {
  const { records } = useContext(AppContext);

  // Dynamic statistics calculated from current repository state
  const totalUploaded = records.length;
  const processingCount = records.filter(r => ['EXTRACTED', 'PENDING'].includes(r.verificationStatus)).length;
  const extractedCount = records.filter(r => ['VERIFIED', 'EXTRACTED'].includes(r.verificationStatus)).length;
  const awaitingReviewCount = records.filter(r => ['UNDER REVIEW', 'LOW CONFIDENCE'].includes(r.verificationStatus)).length;
  const verifiedCount = records.filter(r => r.verificationStatus === 'VERIFIED').length;
  const conflictCount = records.filter(r => r.verificationStatus === 'CONFLICT').length;

  const avgConfidence = totalUploaded > 0
    ? (records.reduce((acc, r) => acc + (r.overallConfidence || 0), 0) / totalUploaded).toFixed(1)
    : '88.5';

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200 dark:border-slate-800 pb-4">
          <div>
            <span className="text-[10px] font-extrabold uppercase tracking-widest text-blue-700 dark:text-blue-300 bg-blue-100 dark:bg-blue-950/80 px-2.5 py-0.5 rounded border border-blue-200 dark:border-blue-800">
              Data Ingestion Cell
            </span>
            <h1 className="text-2xl font-extrabold text-slate-900 dark:text-white tracking-tight mt-1">
              Document Ingestion Dashboard
            </h1>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              Operational document ingestion cell responsible for uploading land records and executing simulated OCR processing.
            </p>
          </div>

          <Link
            to="/o/upload"
            className="px-6 py-3 bg-sky-600 hover:bg-sky-500 text-white font-bold text-xs rounded-xl shadow-lg shadow-sky-600/30 transition-all flex items-center gap-2 self-start sm:self-auto"
          >
            <UploadCloud className="w-4 h-4" />
            <span>Upload & Process Land Record</span>
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>

        {/* OFFICER STAT CARDS */}
        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-3">
          <StatCard title="Documents Uploaded" value={totalUploaded} subtitle="Total files in system" icon={FileText} color="blue" />
          <StatCard title="Documents Processing" value={processingCount} subtitle="Active pipeline" icon={RefreshCw} color="indigo" />
          <StatCard title="Successfully Extracted" value={extractedCount} subtitle="OCR parsed" icon={CheckCircle2} color="emerald" />
          <StatCard title="Awaiting Verification" value={awaitingReviewCount} subtitle="Human review queue" icon={Clock} color="amber" />
          <StatCard title="Verified Records" value={verifiedCount} subtitle="Approved & certified" icon={CheckCircle2} color="emerald" />
          <StatCard title="Records With Conflicts" value={conflictCount} subtitle="Boundary issues" icon={AlertTriangle} color="rose" />
          <StatCard title="Avg Extraction Confidence" value={`${avgConfidence}%`} subtitle="Field accuracy" icon={Layers} color="purple" />
        </div>

        {/* Processing Queue Table */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-sm font-bold text-slate-900 dark:text-white uppercase tracking-wider">
                Ingestion Queue & Processing Status
              </h3>
              <p className="text-xs text-slate-500 dark:text-slate-400">
                Track status of ingested documents and their verification lifecycle.
              </p>
            </div>
            <Link
              to="/o/upload"
              className="text-xs font-bold text-sky-600 dark:text-sky-400 hover:text-sky-800 dark:hover:text-sky-300 flex items-center gap-1"
            >
              <span>+ Upload New Document</span>
            </Link>
          </div>

          <LandRecordTable records={records} role="OFFICER" />
        </div>
      </div>
    </DashboardLayout>
  );
}

