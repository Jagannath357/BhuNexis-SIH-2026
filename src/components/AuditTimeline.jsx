import React, { useState } from 'react';
import { History, Shield, Filter, Search, CheckCircle2, AlertTriangle, XCircle, Info } from 'lucide-react';

export function AuditTimeline({ events = [], readOnly = true }) {
  const [searchQuery, setSearchQuery] = useState('');
  const [filterAction, setFilterAction] = useState('ALL');

  const filteredEvents = events.filter(evt => {
    const matchesSearch = 
      evt.userName.toLowerCase().includes(searchQuery.toLowerCase()) ||
      evt.documentId.toLowerCase().includes(searchQuery.toLowerCase()) ||
      evt.actionDisplay.toLowerCase().includes(searchQuery.toLowerCase());
    
    const matchesAction = filterAction === 'ALL' || evt.action === filterAction;

    return matchesSearch && matchesAction;
  });

  return (
    <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm p-6">
      {/* Header & Filter Controls */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-slate-100 dark:border-slate-800 pb-4">
        <div>
          <h3 className="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
            <History className="w-5 h-5 text-sky-600 dark:text-sky-400" />
            <span>Compliance Audit Log & System History</span>
          </h3>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
            Immutable audit logging • Odisha Tehsil Verification Registry
          </p>
        </div>

        {readOnly && (
          <span className="px-2.5 py-1 text-xs font-bold bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 rounded-full border border-slate-200 dark:border-slate-700">
            Read-Only Inspector Access
          </span>
        )}
      </div>

      {/* Filter Bar */}
      <div className="mt-4 flex flex-col sm:flex-row items-center justify-between gap-3 bg-slate-50 dark:bg-slate-800/40 p-3 rounded-xl border border-slate-100 dark:border-slate-800">
        <div className="relative flex-1 w-full">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 dark:text-slate-500" />
          <input
            type="text"
            placeholder="Search by User, Document ID, or Action..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-lg pl-9 pr-3 py-1.5 text-xs text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:border-sky-500"
          />
        </div>

        <div className="flex items-center gap-2 w-full sm:w-auto">
          <Filter className="w-4 h-4 text-slate-400 dark:text-slate-500 shrink-0" />
          <select
            value={filterAction}
            onChange={(e) => setFilterAction(e.target.value)}
            className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-lg px-3 py-1.5 text-xs font-medium text-slate-700 dark:text-slate-200 focus:outline-none focus:border-sky-500"
          >
            <option value="ALL">All Event Types</option>
            <option value="DOCUMENT_UPLOADED">Document Ingested</option>
            <option value="OCR_COMPLETED">Simulated OCR Completed</option>
            <option value="FIELD_UPDATED">Extraction Field Modified</option>
            <option value="RECORD_VERIFIED">Record Certified & Verified</option>
            <option value="CONFLICT_FLAGGED">Boundary Conflict Flagged</option>
            <option value="SETTING_CHANGED">System Setting Changed</option>
          </select>
        </div>
      </div>

      {/* Timeline Items List */}
      <div className="mt-6 space-y-4">
        {filteredEvents.length === 0 ? (
          <div className="text-center py-8 text-slate-500 dark:text-slate-400 text-xs">
            No audit events match your filter criteria.
          </div>
        ) : (
          filteredEvents.map((evt) => (
            <div key={evt.id} className="relative pl-6 border-l-2 border-slate-200 dark:border-slate-800 space-y-1 hover:border-sky-500 dark:hover:border-sky-400 transition-colors">
              <span className="absolute -left-1.5 top-1 w-3 h-3 rounded-full bg-sky-500 border-2 border-white dark:border-slate-900" />

              <div className="flex items-start justify-between gap-2">
                <div className="flex items-center gap-2">
                  <span className="font-bold text-xs text-slate-900 dark:text-white">{evt.actionDisplay}</span>
                  <span className="text-[10px] font-mono bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 px-1.5 py-0.2 rounded border border-slate-200 dark:border-slate-700">
                    {evt.documentId}
                  </span>
                </div>
                <span className="text-[11px] text-slate-400 dark:text-slate-500 whitespace-nowrap">{evt.timestamp}</span>
              </div>

              <p className="text-xs text-slate-600 dark:text-slate-400">
                Performed by <strong className="text-slate-900 dark:text-slate-200">{evt.userName}</strong> ({evt.userRole})
              </p>

              {(evt.oldValue || evt.newValue) && (
                <div className="mt-2 text-[11px] bg-slate-50 dark:bg-slate-800/50 p-2 rounded-lg border border-slate-100 dark:border-slate-800 font-mono text-slate-700 dark:text-slate-300 flex flex-wrap gap-3">
                  {evt.field && <span>Field: <strong className="text-slate-900 dark:text-white">{evt.field}</strong></span>}
                  {evt.oldValue && <span className="text-rose-600 dark:text-rose-400">Old: "{evt.oldValue}"</span>}
                  {evt.newValue && <span className="text-emerald-600 dark:text-emerald-400">New: "{evt.newValue}"</span>}
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
}
