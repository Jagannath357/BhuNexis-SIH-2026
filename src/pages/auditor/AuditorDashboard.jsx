import React, { useContext } from 'react';
import { AppContext } from '../../context/AppContext';
import { DashboardLayout } from '../../components/DashboardLayout';
import { StatCard } from '../../components/StatCard';
import { AuditTimeline } from '../../components/AuditTimeline';
import { ShieldCheck, History, Activity, AlertCircle, FileCheck, CheckCircle2, Lock } from 'lucide-react';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';

export function AuditorDashboard() {
  const { auditEvents } = useContext(AppContext);

  const throughputData = [
    { date: 'Aug 29', throughput: 1120, errorRate: 4.1 },
    { date: 'Aug 30', throughput: 1250, errorRate: 3.9 },
    { date: 'Aug 31', throughput: 1190, errorRate: 4.0 },
    { date: 'Sep 01', throughput: 1340, errorRate: 3.7 },
    { date: 'Sep 02', throughput: 1284, errorRate: 3.8 },
    { date: 'Sep 03', throughput: 1310, errorRate: 3.6 },
    { date: 'Sep 04', throughput: 1284, errorRate: 3.8 }
  ];

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200 dark:border-slate-800 pb-4">
          <div>
            <span className="text-[10px] font-extrabold uppercase tracking-widest text-rose-700 dark:text-rose-300 bg-rose-100 dark:bg-rose-950/80 px-2.5 py-0.5 rounded border border-rose-200 dark:border-rose-800">
              Independent Compliance
            </span>
            <h1 className="text-2xl font-extrabold text-slate-900 dark:text-white tracking-tight mt-1">
              Compliance & Audit Inspection
            </h1>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              Independent inspection of processing throughput, verification integrity, and system audit history.
            </p>
          </div>

          <div className="px-3.5 py-1.5 bg-rose-50 dark:bg-rose-950/60 text-rose-800 dark:text-rose-300 border border-rose-200 dark:border-rose-800 rounded-xl font-extrabold text-xs flex items-center gap-1.5 shadow-sm">
            <Lock className="w-4 h-4 text-rose-600 dark:text-rose-400" />
            <span>Strictly Read-Only Inspection Mode</span>
          </div>
        </div>

        {/* AUDITOR STAT CARDS */}
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
          <StatCard title="Total Records Audited" value="18,426" subtitle="Khordha Digitized RoR" icon={ShieldCheck} color="rose" />
          <StatCard title="Throughput Rate" value="1,284/day" subtitle="Daily extraction volume" icon={Activity} color="blue" />
          <StatCard title="System Error Rate" value="3.8%" subtitle="Low confidence ratio" icon={AlertCircle} color="amber" />
          <StatCard title="Verification Rate" value="91.6%" subtitle="Approved certifications" icon={CheckCircle2} color="emerald" />
          <StatCard title="Compliance Status" value="COMPLIANT" subtitle="Odisha State Guidelines" icon={CheckCircle2} color="emerald" />
          <StatCard title="Audit Events" value="4,829" subtitle="Recorded timeline logs" icon={History} color="indigo" />
        </div>

        {/* Throughput & Error Rate Chart */}
        <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-5 shadow-sm">
          <h3 className="text-sm font-bold text-slate-900 dark:text-white uppercase tracking-wider mb-4">
            Daily Processing Throughput vs System Error Rate
          </h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={throughputData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis dataKey="date" stroke="#64748B" fontSize={11} />
                <YAxis yAxisId="left" stroke="#0284C7" fontSize={11} />
                <YAxis yAxisId="right" orientation="right" stroke="#E11D48" fontSize={11} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', color: '#fff', borderRadius: '0.5rem', fontSize: '12px' }} />
                <Line yAxisId="left" type="monotone" dataKey="throughput" stroke="#0284C7" strokeWidth={2.5} name="Throughput (records/day)" />
                <Line yAxisId="right" type="monotone" dataKey="errorRate" stroke="#E11D48" strokeWidth={2.5} name="Error Rate (%)" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Read-Only Audit Log */}
        <div className="space-y-3">
          <AuditTimeline events={auditEvents} readOnly={true} />
        </div>
      </div>
    </DashboardLayout>
  );
}
