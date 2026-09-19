import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import DashboardLayout from '../../components/layout/DashboardLayout';
import StatCard from '../../components/common/StatCard';
import StatusBadge from '../../components/common/StatusBadge';
import { dashboardService } from '../../services/settingsService';
import { ShieldCheck, FileText, Activity, Lock, ArrowRight, Eye } from 'lucide-react';

export default function AuditorDashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAuditorStats();
  }, []);

  const fetchAuditorStats = async () => {
    try {
      const res = await dashboardService.getAuditorDashboard();
      setData(res.data);
    } catch (err) {
      console.error("Failed to fetch auditor stats:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <div className="flex items-center space-x-2">
              <h1 className="text-2xl md:text-3xl font-extrabold text-[var(--text-primary)] tracking-tight">
                Legal & Compliance Auditor Dashboard
              </h1>
              <span className="px-2.5 py-1 text-xs font-bold rounded-lg bg-cyan-500/10 text-cyan-600 dark:text-cyan-400 border border-cyan-500/30 flex items-center space-x-1">
                <Lock className="w-3.5 h-3.5" />
                <span>READ ONLY ACCESS</span>
              </span>
            </div>
            <p className="text-sm text-[var(--text-secondary)] mt-1">
              Inspect immutable audit trails, human correction history & AI extraction error rate analytics
            </p>
          </div>
          <Link
            to="/au/audit"
            className="px-5 py-2.5 bg-cyan-600 hover:bg-cyan-700 text-white font-bold rounded-xl text-sm transition-all shadow-lg shadow-cyan-600/30 flex items-center space-x-2 cursor-pointer"
          >
            <Eye className="w-4 h-4" />
            <span>Inspect Complete Audit Logs</span>
          </Link>
        </div>

        {loading ? (
          <div className="p-12 text-center text-cyan-500 font-semibold flex items-center justify-center space-x-3">
            <div className="w-6 h-6 border-2 border-cyan-500 border-t-transparent rounded-full animate-spin" />
            <span>Loading compliance analytics...</span>
          </div>
        ) : (
          <>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-5">
              <StatCard title="Total Audit Event Logs" value={data?.total_audit_events || 0} icon={ShieldCheck} color="cyan" subtitle="Immutable activity logs" />
              <StatCard title="Certified Verified Parcels" value={data?.total_verified_parcels || 0} icon={FileText} color="emerald" subtitle="Passed human verification" />
              <StatCard title="Review Cases Handled" value={data?.total_review_cases || 0} icon={Activity} color="indigo" subtitle="Processed by revenue officers" />
            </div>

            {/* Read-Only Notice Alert */}
            <div className="p-4 rounded-xl bg-cyan-500/10 border border-cyan-500/30 text-cyan-700 dark:text-cyan-300 text-xs font-semibold flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <ShieldCheck className="w-5 h-5 flex-shrink-0 text-cyan-500" />
                <span>Compliance Inspector Mode Active: All modification, approval, and verification controls are strictly disabled.</span>
              </div>
              <StatusBadge status="COMPLIANT" />
            </div>

            {/* Audit Log Timeline Preview */}
            <div className="bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl p-6 shadow-sm">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-bold text-[var(--text-primary)]">Recent System Activity Logs</h3>
                <Link to="/au/audit" className="text-xs font-bold text-cyan-500 hover:underline flex items-center space-x-1">
                  <span>View All Events</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </Link>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                  <thead>
                    <tr className="border-b border-[var(--border-color)] text-[var(--text-secondary)] uppercase text-xs">
                      <th className="py-3 px-4">Event ID</th>
                      <th className="py-3 px-4">User ID</th>
                      <th className="py-3 px-4">Action Type</th>
                      <th className="py-3 px-4">Entity</th>
                      <th className="py-3 px-4">Timestamp</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-[var(--border-color)]">
                    {data?.recent_audit_events?.map((ev) => (
                      <tr key={ev.id} className="hover:bg-[var(--bg-main)]">
                        <td className="py-3 px-4 font-bold text-cyan-600 dark:text-cyan-400">#{ev.id}</td>
                        <td className="py-3 px-4 text-[var(--text-secondary)]">User #{ev.user_id || 'SYSTEM'}</td>
                        <td className="py-3 px-4 font-semibold text-[var(--text-primary)]">{ev.action}</td>
                        <td className="py-3 px-4 text-xs text-[var(--text-secondary)]">{ev.entity_type} #{ev.entity_id}</td>
                        <td className="py-3 px-4 text-xs text-[var(--text-muted)]">{new Date(ev.created_at).toLocaleString()}</td>
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
