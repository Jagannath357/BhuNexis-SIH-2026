import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import { AppContext } from '../../context/AppContext';
import { DashboardLayout } from '../../components/DashboardLayout';
import { StatCard } from '../../components/StatCard';
import { LandRecordTable } from '../../components/LandRecordTable';
import { 
  Users, 
  ShieldCheck, 
  Activity, 
  Sliders, 
  FileText, 
  CheckCircle2, 
  AlertTriangle, 
  Clock, 
  Server, 
  UserCheck, 
  Settings,
  History
} from 'lucide-react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, BarChart, Bar, XAxis, YAxis } from 'recharts';

export function AdminDashboard() {
  const { records, userList, systemSettings, systemStats } = useContext(AppContext);

  const activeCount = userList.filter(u => u.status === 'ACTIVE').length;
  const disabledCount = userList.filter(u => u.status === 'DISABLED').length;

  const roleDistributionData = [
    { name: 'Officers', value: 18, color: '#3B82F6' },
    { name: 'Reviewers', value: 12, color: '#F59E0B' },
    { name: 'Auditors', value: 5, color: '#EF4444' },
    { name: 'Admins', value: 3, color: '#8B5CF6' },
    { name: 'Citizens', value: 10, color: '#10B981' }
  ];

  const systemPerformanceData = [
    { stage: 'OCR Analysis', latency: 42 },
    { stage: 'Preprocessing', latency: 28 },
    { stage: 'Field Parse', latency: 55 },
    { stage: 'Rule Engine', latency: 15 },
    { stage: 'GIS Match', latency: 32 }
  ];

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Page Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200 dark:border-slate-800 pb-4">
          <div>
            <span className="text-[10px] font-extrabold uppercase tracking-widest text-purple-700 dark:text-purple-300 bg-purple-100 dark:bg-purple-950/80 px-2.5 py-0.5 rounded border border-purple-200 dark:border-purple-800">
              System Administration
            </span>
            <h1 className="text-2xl font-extrabold text-slate-900 dark:text-white tracking-tight mt-1">
              Admin Platform Governance
            </h1>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              System health monitoring, user credential provisioning, and threshold configurations.
            </p>
          </div>

          <div className="flex items-center gap-2">
            <Link
              to="/a/users"
              className="px-3.5 py-2 bg-slate-900 dark:bg-slate-800 hover:bg-slate-800 dark:hover:bg-slate-700 text-white font-bold text-xs rounded-xl shadow-sm border border-transparent dark:border-slate-700 transition-colors flex items-center gap-1.5"
            >
              <Users className="w-3.5 h-3.5" />
              <span>User Management</span>
            </Link>
            <Link
              to="/a/settings"
              className="px-3.5 py-2 bg-sky-600 hover:bg-sky-500 text-white font-bold text-xs rounded-xl shadow-sm transition-colors flex items-center gap-1.5"
            >
              <Settings className="w-3.5 h-3.5" />
              <span>System Settings</span>
            </Link>
          </div>
        </div>

        {/* 11 STAT CARDS GRID */}
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
          <StatCard title="Total Users" value={systemStats.totalUsers} subtitle="Registered accounts" icon={Users} color="blue" />
          <StatCard title="Active Users" value={activeCount} subtitle="Active sessions" icon={UserCheck} color="emerald" />
          <StatCard title="Pending Access" value={systemStats.pendingUsers} subtitle="Review queue" icon={Clock} color="amber" />
          <StatCard title="Active Officers" value={systemStats.activeOfficers} subtitle="Ingestion Specialists" icon={FileText} color="blue" />
          <StatCard title="Reviewers" value={systemStats.reviewers} subtitle="Human Verifiers" icon={CheckCircle2} color="amber" />
          <StatCard title="Auditors" value={systemStats.auditors} subtitle="Compliance Inspectors" icon={ShieldCheck} color="rose" />
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
          <StatCard title="System Health" value={`${systemStats.systemHealth}%`} subtitle="Optimal status" icon={Activity} color="emerald" />
          <StatCard title="OCR Threshold" value={`${systemSettings.ocrConfidenceThreshold}%`} subtitle="Configured limit" icon={Sliders} color="purple" />
          <StatCard title="Validation Rules" value={`${systemSettings.validationRulesCount} Active`} subtitle="Automated checks" icon={CheckCircle2} color="blue" />
          <StatCard title="API Speed" value={`${systemStats.apiPerformanceMs} ms`} subtitle="Average latency" icon={Server} color="emerald" />
          <StatCard title="Active Sessions" value={systemStats.activeSessions} subtitle="Live users now" icon={Users} color="indigo" />
        </div>

        {/* Charts & Graphs Row */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* User Distribution Chart */}
          <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-5 shadow-sm">
            <h3 className="text-sm font-bold text-slate-900 dark:text-white uppercase tracking-wider mb-4 flex items-center justify-between">
              <span>Platform Role Distribution</span>
              <span className="text-xs font-normal text-slate-500 dark:text-slate-400">48 Total Accounts</span>
            </h3>
            <div className="h-56">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={roleDistributionData}
                    cx="50%"
                    cy="50%"
                    innerRadius={50}
                    outerRadius={80}
                    paddingAngle={4}
                    dataKey="value"
                  >
                    {roleDistributionData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', color: '#fff', borderRadius: '0.5rem', fontSize: '12px' }} />
                </PieChart>
              </ResponsiveContainer>
            </div>
            <div className="flex flex-wrap items-center justify-center gap-3 mt-2 text-xs font-semibold">
              {roleDistributionData.map(item => (
                <div key={item.name} className="flex items-center gap-1.5">
                  <span className="w-3 h-3 rounded-full" style={{ backgroundColor: item.color }} />
                  <span className="text-slate-700 dark:text-slate-300">{item.name}: {item.value}</span>
                </div>
              ))}
            </div>
          </div>

          {/* System Performance Bar Chart */}
          <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-5 shadow-sm">
            <h3 className="text-sm font-bold text-slate-900 dark:text-white uppercase tracking-wider mb-4">
              Pipeline Stage Execution Speeds (ms)
            </h3>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={systemPerformanceData}>
                  <XAxis dataKey="stage" stroke="#64748B" fontSize={11} />
                  <YAxis stroke="#64748B" fontSize={11} />
                  <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', color: '#fff', borderRadius: '0.5rem', fontSize: '12px' }} />
                  <Bar dataKey="latency" fill="#0284C7" radius={[6, 6, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        {/* Recent Ingested Records Overview */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-bold text-slate-900 dark:text-white uppercase tracking-wider">
              Recent System Records
            </h3>
            <Link to="/a/audit" className="text-xs font-semibold text-sky-600 dark:text-sky-400 hover:text-sky-800 dark:hover:text-sky-300 flex items-center gap-1">
              <History className="w-3.5 h-3.5" />
              <span>Full Audit History</span>
            </Link>
          </div>
          <LandRecordTable records={records.slice(0, 5)} role="ADMIN" />
        </div>
      </div>
    </DashboardLayout>
  );
}
