import React, { useState } from 'react';
import { Search, Filter, RefreshCw, Layers } from 'lucide-react';

export function SearchPanel({ onSearch, onReset }) {
  const [surveyNo, setSurveyNo] = useState('');
  const [khataNo, setKhataNo] = useState('');
  const [ownerName, setOwnerName] = useState('');
  const [village, setVillage] = useState('');
  const [statusFilter, setStatusFilter] = useState('ALL');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch({ surveyNo, khataNo, ownerName, village, statusFilter });
  };

  const handleReset = () => {
    setSurveyNo('');
    setKhataNo('');
    setOwnerName('');
    setVillage('');
    setStatusFilter('ALL');
    if (onReset) onReset();
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm p-5 transition-colors">
      <div className="flex items-center justify-between mb-4 border-b border-slate-100 dark:border-slate-800 pb-3">
        <h4 className="text-sm font-bold text-slate-900 dark:text-white uppercase tracking-wider flex items-center gap-2">
          <Search className="w-4 h-4 text-sky-600 dark:text-sky-400" />
          <span>Multi-Criteria Land Record Search</span>
        </h4>
        <button
          type="button"
          onClick={handleReset}
          className="text-xs text-slate-500 dark:text-slate-400 hover:text-slate-800 dark:hover:text-white flex items-center gap-1 font-medium"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Reset Search</span>
        </button>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3 text-xs">
        <div>
          <label className="block text-[11px] font-semibold text-slate-500 dark:text-slate-400 mb-1">Survey Number</label>
          <input
            type="text"
            placeholder="e.g. 125/3"
            value={surveyNo}
            onChange={(e) => setSurveyNo(e.target.value)}
            className="w-full bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg p-2 text-xs text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:border-sky-500"
          />
        </div>

        <div>
          <label className="block text-[11px] font-semibold text-slate-500 dark:text-slate-400 mb-1">Khata Number</label>
          <input
            type="text"
            placeholder="e.g. 87"
            value={khataNo}
            onChange={(e) => setKhataNo(e.target.value)}
            className="w-full bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg p-2 text-xs text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:border-sky-500"
          />
        </div>

        <div>
          <label className="block text-[11px] font-semibold text-slate-500 dark:text-slate-400 mb-1">Owner Name</label>
          <input
            type="text"
            placeholder="e.g. Ramesh Chandra"
            value={ownerName}
            onChange={(e) => setOwnerName(e.target.value)}
            className="w-full bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg p-2 text-xs text-slate-900 dark:text-slate-100 placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:border-sky-500"
          />
        </div>

        <div>
          <label className="block text-[11px] font-semibold text-slate-500 dark:text-slate-400 mb-1">Mouza / Village</label>
          <select
            value={village}
            onChange={(e) => setVillage(e.target.value)}
            className="w-full bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg p-2 text-xs text-slate-900 dark:text-slate-100 focus:outline-none focus:border-sky-500"
          >
            <option value="">All Mouzas (Khordha)</option>
            <option value="BhuNexis Demo Village">BhuNexis Demo Village</option>
            <option value="Shantipur Mouza">Shantipur Mouza</option>
            <option value="Haripur Mouza">Haripur Mouza</option>
            <option value="Ratanpur Mouza">Ratanpur Mouza</option>
          </select>
        </div>

        <div>
          <label className="block text-[11px] font-semibold text-slate-500 dark:text-slate-400 mb-1">Verification Status</label>
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="w-full bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg p-2 text-xs text-slate-900 dark:text-slate-100 focus:outline-none focus:border-sky-500"
          >
            <option value="ALL">All Statuses</option>
            <option value="VERIFIED">Verified</option>
            <option value="UNDER REVIEW">Under Review</option>
            <option value="LOW CONFIDENCE">Low Confidence</option>
            <option value="CONFLICT">Conflict</option>
            <option value="EXTRACTED">Extracted</option>
          </select>
        </div>
      </div>

      <div className="mt-4 flex justify-end">
        <button
          type="submit"
          className="px-5 py-2 bg-sky-600 hover:bg-sky-500 text-white font-bold text-xs rounded-xl shadow-sm transition-colors flex items-center gap-1.5"
        >
          <Search className="w-3.5 h-3.5" />
          <span>Execute Land Search</span>
        </button>
      </div>
    </form>
  );
}
