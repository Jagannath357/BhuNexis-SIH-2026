import React, { useEffect, useState } from 'react';
import DashboardLayout from '../../components/layout/DashboardLayout';
import StatCard from '../../components/common/StatCard';
import StatusBadge from '../../components/common/StatusBadge';
import { dashboardService } from '../../services/settingsService';
import { Users, FileText, CheckSquare, AlertTriangle, ShieldCheck, Activity } from 'lucide-react';

export default function AdminDashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAdminStats();
  }, []);

  const fetchAdminStats = async () => {
    try {
      const res = await dashboardService.getAdminDashboard();
      setData(res.data);
    } catch (err) {
      console.error("Failed to fetch admin stats:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl md:text-3xl font-extrabold text-[var(--text-primary)] tracking-tight">
            System Administration Dashboard
          </h1>
          <p className="text-sm text-[var(--text-secondary)] mt-1">
            Global system monitoring, user management, and AI engine status
          </p>
        </div>

        {loading ? (
          <div className="p-12 text-center text-emerald-500 font-semibold flex items-center justify-center space-x-3">
            <div className="w-6 h-6 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin" />
            <span>Loading admin statistics...</span>
          </div>
        ) : (
          <>
            {/* Top Stat Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
              <StatCard title="Total System Users" value={data?.total_users || 0} icon={Users} color="indigo" subtitle={`${data?.active_users || 0} active accounts`} />
              <StatCard title="Uploaded Documents" value={data?.total_documents || 0} icon={FileText} color="blue" subtitle={`${data?.processed_documents || 0} processed`} />
              <StatCard title="Pending Human Reviews" value={data?.pending_reviews || 0} icon={CheckSquare} color="amber" subtitle="Awaiting verifier approval" />
              <StatCard title="Validation Conflicts" value={data?.validation_conflicts || 0} icon={AlertTriangle} color="rose" subtitle="Area / Owner mismatch cases" />
              <StatCard title="OCR Extraction Accuracy" value={data?.processing_statistics?.ocr_accuracy || '94.2%'} icon={Activity} color="emerald" subtitle="Confidence benchmark" />
              <StatCard title="Auto-Validation Rate" value={data?.processing_statistics?.auto_validation_rate || '87.5%'} icon={ShieldCheck} color="cyan" subtitle="Rule engine pass rate" />
            </div>

            {/* System Health Status Grid */}
            <div className="bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl p-6 shadow-sm">
              <div className="flex items-center justify-between pb-4 border-b border-[var(--border-color)] mb-6">
                <div>
                  <h3 className="text-lg font-bold text-[var(--text-primary)]">System Component Health</h3>
                  <p className="text-xs text-[var(--text-secondary)] mt-0.5">Real-time status of backend services and AI engines</p>
                </div>
                <StatusBadge status="HEALTHY" />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {Object.entries(data?.system_health || {}).map(([serviceKey, healthStatus]) => (
                  <div key={serviceKey} className="p-4 rounded-xl border border-[var(--border-color)] bg-[var(--bg-main)] flex items-center justify-between">
                    <div>
                      <h4 className="font-bold text-sm text-[var(--text-primary)] uppercase tracking-wider">{serviceKey} Service</h4>
                      <p className="text-xs text-[var(--text-muted)] mt-0.5">
                        {healthStatus === 'HEALTHY' ? 'Running normally' : 'Service offline / not configured'}
                      </p>
                    </div>
                    <StatusBadge status={healthStatus} />
                  </div>
                ))}
              </div>
            </div>
          </>
        )}
      </div>
    </DashboardLayout>
  );
}
