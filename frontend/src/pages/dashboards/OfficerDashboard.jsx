import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import DashboardLayout from '../../components/layout/DashboardLayout';
import StatCard from '../../components/common/StatCard';
import StatusBadge from '../../components/common/StatusBadge';
import { dashboardService } from '../../services/settingsService';
import { FileUp, FileText, CheckCircle, Clock, AlertCircle, ArrowRight } from 'lucide-react';

export default function OfficerDashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchOfficerStats();
  }, []);

  const fetchOfficerStats = async () => {
    try {
      const res = await dashboardService.getOfficerDashboard();
      setData(res.data);
    } catch (err) {
      console.error("Failed to fetch officer stats:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl md:text-3xl font-extrabold text-[var(--text-primary)] tracking-tight">
              Data Ingestion Specialist Dashboard
            </h1>
            <p className="text-sm text-[var(--text-secondary)] mt-1">
              Upload historical land records, manage batch ingestion & monitor OCR extraction status
            </p>
          </div>
          <Link
            to="/o/upload"
            className="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-xl text-sm transition-all shadow-lg shadow-emerald-600/30 flex items-center space-x-2 cursor-pointer"
          >
            <FileUp className="w-4 h-4" />
            <span>Upload New Document</span>
          </Link>
        </div>

        {loading ? (
          <div className="p-12 text-center text-emerald-500 font-semibold flex items-center justify-center space-x-3">
            <div className="w-6 h-6 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin" />
            <span>Loading ingestion statistics...</span>
          </div>
        ) : (
          <>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-5">
              <StatCard title="My Uploaded Documents" value={data?.my_uploads || 0} icon={FileText} color="emerald" subtitle="Total files ingested by you" />
              <StatCard title="OCR Processing" value={data?.status_breakdown?.OCR_PROCESSING || 0} icon={Clock} color="amber" subtitle="Currently extracting text" />
              <StatCard title="Pending Review" value={data?.status_breakdown?.REVIEW_REQUIRED || 0} icon={AlertCircle} color="rose" subtitle="Awaiting revenue verifier" />
            </div>

            {/* Ingestion Lifecycle */}
            <div className="bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl p-6 shadow-sm">
              <h3 className="text-lg font-bold text-[var(--text-primary)] mb-4">Document Processing Lifecycle</h3>
              <div className="flex flex-wrap items-center justify-between gap-2 p-4 rounded-xl bg-[var(--bg-main)] border border-[var(--border-color)] text-xs font-semibold">
                <span className="px-3 py-1.5 rounded-lg bg-blue-500/10 text-blue-600 dark:text-blue-400">1. UPLOADED</span>
                <span className="text-[var(--text-muted)]">→</span>
                <span className="px-3 py-1.5 rounded-lg bg-amber-500/10 text-amber-600 dark:text-amber-400">2. PREPROCESSING</span>
                <span className="text-[var(--text-muted)]">→</span>
                <span className="px-3 py-1.5 rounded-lg bg-indigo-500/10 text-indigo-600 dark:text-indigo-400">3. OCR_PROCESSING</span>
                <span className="text-[var(--text-muted)]">→</span>
                <span className="px-3 py-1.5 rounded-lg bg-purple-500/10 text-purple-600 dark:text-purple-400">4. EXTRACTED</span>
                <span className="text-[var(--text-muted)]">→</span>
                <span className="px-3 py-1.5 rounded-lg bg-cyan-500/10 text-cyan-600 dark:text-cyan-400">5. VALIDATING</span>
                <span className="text-[var(--text-muted)]">→</span>
                <span className="px-3 py-1.5 rounded-lg bg-emerald-500/10 text-emerald-600 dark:text-emerald-400">6. VERIFIED</span>
              </div>
            </div>

            {/* Recent Uploaded Documents Table */}
            <div className="bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl p-6 shadow-sm">
              <h3 className="text-lg font-bold text-[var(--text-primary)] mb-4">Recently Ingested Records</h3>
              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                  <thead>
                    <tr className="border-b border-[var(--border-color)] text-[var(--text-secondary)] uppercase text-xs">
                      <th className="py-3 px-4">Document UID</th>
                      <th className="py-3 px-4">File Name</th>
                      <th className="py-3 px-4">District</th>
                      <th className="py-3 px-4">Status</th>
                      <th className="py-3 px-4">Uploaded Date</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-[var(--border-color)]">
                    {data?.recent_documents?.map((doc) => (
                      <tr key={doc.id} className="hover:bg-[var(--bg-main)]">
                        <td className="py-3 px-4 font-bold text-emerald-600 dark:text-emerald-400">{doc.document_uid}</td>
                        <td className="py-3 px-4 font-medium text-[var(--text-primary)]">{doc.file_name}</td>
                        <td className="py-3 px-4 text-[var(--text-secondary)]">{doc.district || 'Khordha'}</td>
                        <td className="py-3 px-4"><StatusBadge status={doc.processing_status} /></td>
                        <td className="py-3 px-4 text-xs text-[var(--text-muted)]">{new Date(doc.created_at).toLocaleDateString()}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </>
        )}
      </div>
    </DashboardLayout>
  );
}
