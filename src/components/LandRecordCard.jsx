import React from 'react';
import { Link } from 'react-router-dom';
import { StatusBadge } from './StatusBadge';
import { ConfidenceBar } from './ConfidenceBar';
import { MapPin, FileText, ArrowRight, Download, UserCheck } from 'lucide-react';
import { downloadMockCertifiedRecord } from '../utils/downloadMockRecord';

export function LandRecordCard({ record, onDownload }) {
  if (!record) return null;

  return (
    <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm hover:shadow-md transition-all p-5 flex flex-col justify-between">
      <div>
        {/* Top Badges */}
        <div className="flex items-center justify-between gap-2 mb-3">
          <span className="text-[11px] font-mono font-bold text-slate-500 dark:text-slate-400 bg-slate-100 dark:bg-slate-800 px-2 py-0.5 rounded border border-slate-200 dark:border-slate-700">
            {record.id}
          </span>
          <StatusBadge status={record.verificationStatus} />
        </div>

        {/* Owner Info */}
        <h4 className="text-base font-extrabold text-slate-900 dark:text-white leading-tight">
          {record.ownerName}
        </h4>
        <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
          s/o {record.fatherName || 'N/A'}
        </p>

        {/* Parcel Details */}
        <div className="mt-4 grid grid-cols-2 gap-2 text-xs border-t border-slate-100 dark:border-slate-800 pt-3">
          <div>
            <span className="text-slate-400 dark:text-slate-500 block text-[10px] uppercase font-semibold">Survey No</span>
            <span className="font-bold text-slate-800 dark:text-slate-200">{record.surveyNumber}</span>
          </div>
          <div>
            <span className="text-slate-400 dark:text-slate-500 block text-[10px] uppercase font-semibold">Khata No</span>
            <span className="font-bold text-slate-800 dark:text-slate-200">{record.khataNumber}</span>
          </div>
          <div>
            <span className="text-slate-400 dark:text-slate-500 block text-[10px] uppercase font-semibold">Plot Area</span>
            <span className="font-semibold text-slate-800 dark:text-slate-200">{record.area} {record.areaUnit}</span>
          </div>
          <div>
            <span className="text-slate-400 dark:text-slate-500 block text-[10px] uppercase font-semibold">Classification</span>
            <span className="font-medium text-slate-700 dark:text-slate-300 truncate block">{record.landClassification}</span>
          </div>
        </div>

        {/* Location Mouza */}
        <div className="mt-3 flex items-center gap-1.5 text-xs text-slate-600 dark:text-slate-300 bg-slate-50 dark:bg-slate-800/80 p-2 rounded-lg border border-slate-100 dark:border-slate-700">
          <MapPin className="w-3.5 h-3.5 text-sky-600 dark:text-sky-400 shrink-0" />
          <span className="truncate">{record.village}, {record.tehsil}, Odisha</span>
        </div>

        {/* Confidence Progress */}
        <div className="mt-4">
          <ConfidenceBar score={record.overallConfidence} label="OCR Confidence" />
        </div>
      </div>

      {/* Card Actions */}
      <div className="mt-5 border-t border-slate-100 dark:border-slate-800 pt-3 flex items-center justify-between gap-2">
        <Link
          to={`/u/records/${record.id}`}
          className="text-xs font-bold text-sky-600 dark:text-sky-400 hover:text-sky-800 dark:hover:text-sky-300 flex items-center gap-1 group"
        >
          <span>View Record Details</span>
          <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-0.5 transition-transform" />
        </Link>

        {record.verificationStatus === 'VERIFIED' && (
          <button
            onClick={() => onDownload ? onDownload(record) : downloadMockCertifiedRecord(record)}
            className="px-2.5 py-1 text-xs font-medium bg-emerald-50 dark:bg-emerald-950/60 hover:bg-emerald-100 dark:hover:bg-emerald-900/60 text-emerald-700 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800 rounded-lg flex items-center gap-1 transition-colors"
          >
            <Download className="w-3 h-3" />
            <span>Copy</span>
          </button>
        )}
      </div>
    </div>
  );
}
