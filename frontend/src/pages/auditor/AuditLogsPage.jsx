import React, { useEffect, useState } from 'react';
import DashboardLayout from '../../components/layout/DashboardLayout';
import auditService from '../../services/auditService';
import StatusBadge from '../../components/common/StatusBadge';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { ShieldCheck, Search, Filter, Lock, Eye, Activity } from 'lucide-react';

export default function AuditLogsPage() {
  const [events, setEvents] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);

  // Filters
  const [actionFilter, setActionFilter] = useState('');
  const [entityFilter, setEntityFilter] = useState('');

  useEffect(() => {
    fetchAuditData();
  }, [actionFilter, entityFilter]);

  const fetchAuditData = async () => {
    setLoading(true);
    try {
      const [evData, anData] = await Promise.all([
        auditService.getAuditEvents({ action: actionFilter, entity_type: entityFilter }),
        auditService.getAuditAnalytics()
      ]);
      setEvents(evData);
      setAnalytics(anData);
    } catch (err) {
      console.error("Failed to load audit data:", err);
    } finally {
      setLoading(false);
    }
  };

  const chartData = analytics?.throughput_per_day
    ? Object.entries(analytics.throughput_per_day).map(([date, count]) => ({ date, count }))
    : [
        { date: '2026-09-14', count: 42 },
        { date: '2026-09-15', count: 88 },
        { date: '2026-09-16', count: 120 },
        { date: '2026-09-17', count: 95 },
        { date: '2026-09-18', count: 64 }
      ];

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <div className="flex items-center space-x-2">
              <h1 className="text-2xl md:text-3xl font-extrabold text-[var(--text-primary)] tracking-tight">
                System Audit History & Analytics
              </h1>
              <span className="px-2.5 py-1 text-xs font-bold rounded-lg bg-cyan-500/10 text-cyan-600 dark:text-cyan-400 border border-cyan-500/30 flex items-center space-x-1">
                <Lock className="w-3.5 h-3.5" />
                <span>READ ONLY</span>
              </span>
            </div>
            <p className="text-sm text-[var(--text-secondary)] mt-1">
              Complete historical record of user actions, AI extraction events, and human verifications
            </p>
          </div>
        </div>

        {loading ? (
          <div className="p-12 text-center text-cyan-500 font-semibold flex items-center justify-center space-x-3">
            <div className="w-6 h-6 border-2 border-cyan-500 border-t-transparent rounded-full animate-spin" />
            <span>Loading audit log events...</span>
          </div>
        ) : (
          <>
            {/* Analytics Chart Row */}
            <div className="grid md:grid-cols-2 gap-6">
              <div className="bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl p-5 shadow-sm">
                <h3 className="text-base font-bold text-[var(--text-primary)] mb-1">Daily Record Throughput</h3>
                <p className="text-xs text-[var(--text-muted)] mb-4">Ingestion & verification volume over time</p>
                <div className="h-48 w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={chartData}>
                      <defs>
                        <linearGradient id="colorCount" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="5%" stopColor="#06b6d4" stopOpacity={0.4}/>
                          <stop offset="95%" stopColor="#06b6d4" stopOpacity={0}/>
                        </linearGradient>
                      </defs>
                      <XAxis dataKey="date" stroke="#94a3b8" fontSize={11} />
                      <YAxis stroke="#94a3b8" fontSize={11} />
                      <Tooltip contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', color: '#fff', borderRadius: '0.5rem', fontSize: '12px' }} />
                      <Area type="monotone" dataKey="count" stroke="#06b6d4" strokeWidth={2} fillOpacity={1} fill="url(#colorCount)" />
                    </AreaChart>
                  </ResponsiveContainer>
                </div>
              </div>

              <div className="bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl p-5 shadow-sm">
                <h3 className="text-base font-bold text-[var(--text-primary)] mb-1">Audit Event Types Breakdown</h3>
                <p className="text-xs text-[var(--text-muted)] mb-4">Distribution across login, upload, and review actions</p>
                <div className="h-48 w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={Object.entries(analytics?.events_by_action || {}).map(([action, cnt]) => ({ action, cnt })).slice(0, 5)}>
                      <XAxis dataKey="action" stroke="#94a3b8" fontSize={10} />
                      <YAxis stroke="#94a3b8" fontSize={11} />
                      <Tooltip contentStyle={{ backgroundColor: '#1e293b', borderColor: '#334155', color: '#fff', borderRadius: '0.5rem', fontSize: '12px' }} />
                      <Bar dataKey="cnt" fill="#10b981" radius={[4, 4, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </div>

            {/* Filter Bar */}
            <div className="bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl p-4 flex flex-wrap items-center gap-4 shadow-sm">
              <div className="flex items-center space-x-2 text-xs font-bold text-[var(--text-secondary)] uppercase">
                <Filter className="w-4 h-4 text-cyan-500" />
                <span>Filters:</span>
              </div>
              <input
                type="text"
                placeholder="Filter by action (e.g., LOGIN, FIELD_CORRECTED)..."
                value={actionFilter}
                onChange={(e) => setActionFilter(e.target.value)}
                className="px-3.5 py-2 rounded-xl border border-[var(--border-color)] bg-[var(--bg-main)] text-[var(--text-primary)] text-xs w-64 focus:outline-none focus:ring-1 focus:ring-cyan-500"
              />
              <input
                type="text"
                placeholder="Filter by entity (e.g., User, Document)..."
                value={entityFilter}
                onChange={(e) => setEntityFilter(e.target.value)}
                className="px-3.5 py-2 rounded-xl border border-[var(--border-color)] bg-[var(--bg-main)] text-[var(--text-primary)] text-xs w-64 focus:outline-none focus:ring-1 focus:ring-cyan-500"
              />
            </div>

            {/* Audit Log Events Table */}
            <div className="bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl p-6 shadow-sm">
              <h3 className="text-lg font-bold text-[var(--text-primary)] mb-4">Audit Trail Logs ({events.length})</h3>
              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                  <thead>
                    <tr className="border-b border-[var(--border-color)] text-[var(--text-secondary)] uppercase text-xs">
                      <th className="py-3 px-4">Log ID</th>
                      <th className="py-3 px-4">User ID</th>
                      <th className="py-3 px-4">Action</th>
                      <th className="py-3 px-4">Entity Type</th>
                      <th className="py-3 px-4">Entity ID</th>
                      <th className="py-3 px-4">Changes</th>
                      <th className="py-3 px-4">Timestamp</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-[var(--border-color)]">
                    {events.map((ev) => (
                      <tr key={ev.id} className="hover:bg-[var(--bg-main)]">
                        <td className="py-3 px-4 font-bold text-cyan-600 dark:text-cyan-400">#{ev.id}</td>
                        <td className="py-3 px-4 text-[var(--text-primary)] font-medium">User #{ev.user_id || 'SYSTEM'}</td>
                        <td className="py-3 px-4 font-bold text-emerald-600 dark:text-emerald-400">{ev.action}</td>
                        <td className="py-3 px-4 text-[var(--text-secondary)]">{ev.entity_type || 'N/A'}</td>
                        <td className="py-3 px-4 font-mono text-xs">{ev.entity_id || '-'}</td>
                        <td className="py-3 px-4 text-xs font-mono text-[var(--text-muted)] truncate max-w-xs">
                          {ev.changes ? JSON.stringify(ev.changes) : '-'}
                        </td>
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
