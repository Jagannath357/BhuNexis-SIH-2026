import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import DashboardLayout from '../../components/layout/DashboardLayout';
import StatCard from '../../components/common/StatCard';
import StatusBadge from '../../components/common/StatusBadge';
import { dashboardService } from '../../services/settingsService';
import { CheckSquare, AlertTriangle, CheckCircle, ArrowRight, ShieldCheck } from 'lucide-react';

export default function ReviewerDashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchReviewerStats();
  }, []);

  const fetchReviewerStats = async () => {
    try {
      const res = await dashboardService.getReviewerDashboard();
      setData(res.data);
    } catch (err) {
      console.error("Failed to fetch reviewer stats:", err);
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
              Human-in-the-Loop Verifier Dashboard
            </h1>
            <p className="text-sm text-[var(--text-secondary)] mt-1">
              Review low confidence OCR extractions, resolve land record conflicts & grant final certification
            </p>
          </div>
          <Link
            to="/r/review"
            className="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-xl text-sm transition-all shadow-lg shadow-emerald-600/30 flex items-center space-x-2 cursor-pointer"
          >
            <CheckSquare className="w-4 h-4" />
            <span>Open Review Workspace</span>
          </Link>
        </div>

        {loading ? (
          <div className="p-12 text-center text-emerald-500 font-semibold flex items-center justify-center space-x-3">
            <div className="w-6 h-6 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin" />
            <span>Loading verification queue...</span>
          </div>
        ) : (
          <>
            <div className="grid grid-cols-1 sm:grid-cols-4 gap-5">
              <StatCard title="Pending Review Queue" value={data?.pending_queue || 0} icon={CheckSquare} color="amber" subtitle="Awaiting review" />
              <StatCard title="High Priority Cases" value={data?.high_priority_count || 0} icon={AlertTriangle} color="rose" subtitle="Requires urgent verification" />
              <StatCard title="Validation Conflicts" value={data?.validation_conflicts || 0} icon={AlertTriangle} color="amber" subtitle="Mismatch detected by engine" />
              <StatCard title="Resolved by Me" value={data?.resolved_by_me || 0} icon={CheckCircle} color="emerald" subtitle="Certified records" />
            </div>

            {/* Pending Review Queue Table */}
            <div className="bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl p-6 shadow-sm">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-bold text-[var(--text-primary)]">Cases Requiring Attention</h3>
                <Link to="/r/review" className="text-xs font-bold text-emerald-500 hover:underline flex items-center space-x-1">
                  <span>View All ({data?.pending_queue || 0})</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </Link>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                  <thead>
                    <tr className="border-b border-[var(--border-color)] text-[var(--text-secondary)] uppercase text-xs">
                      <th className="py-3 px-4">Case UID</th>
                      <th className="py-3 px-4">Parcel ID</th>
                      <th className="py-3 px-4">Review Type</th>
                      <th className="py-3 px-4">Priority</th>
                      <th className="py-3 px-4">Status</th>
                      <th className="py-3 px-4">Action</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-[var(--border-color)]">
                    {data?.review_queue?.map((item) => (
                      <tr key={item.id} className="hover:bg-[var(--bg-main)]">
                        <td className="py-3 px-4 font-bold text-amber-600 dark:text-amber-400">{item.case_uid}</td>
                        <td className="py-3 px-4 font-medium text-[var(--text-primary)]">OD-PCL-{String(item.parcel_id).padStart(4, '0')}</td>
                        <td className="py-3 px-4 text-[var(--text-secondary)]">{item.review_type || 'OWNER_MATCH'}</td>
                        <td className="py-3 px-4">
                          <span className={`px-2 py-0.5 text-xs font-bold rounded ${item.priority === 'HIGH' ? 'bg-rose-500/10 text-rose-500' : 'bg-slate-500/10 text-slate-400'}`}>
                            {item.priority || 'MEDIUM'}
                          </span>
                        </td>
                        <td className="py-3 px-4"><StatusBadge status={item.status} /></td>
                        <td className="py-3 px-4">
                          <Link
                            to="/r/review"
                            className="px-3 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-xs rounded-lg transition-all shadow-sm"
                          >
                            Verify Record
                          </Link>
                        </td>
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
