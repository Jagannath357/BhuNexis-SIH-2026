import React, { useContext, useState } from 'react';
import { AppContext } from '../../context/AppContext';
import { useAuth } from '../../hooks/useAuth';
import { useToast } from '../../hooks/useToast';
import { DashboardLayout } from '../../components/DashboardLayout';
import { Sliders, Save, ShieldCheck, Database, CheckCircle2 } from 'lucide-react';

export function SystemSettings() {
  const { systemSettings, updateSettings } = useContext(AppContext);
  const { user } = useAuth();
  const { addToast } = useToast();

  const [formData, setFormData] = useState(systemSettings);

  const handleSubmit = (e) => {
    e.preventDefault();
    updateSettings(formData, user?.name);
    addToast('System settings updated successfully — Demo Mode.', 'success');
  };

  return (
    <DashboardLayout>
      <div className="space-y-6 max-w-3xl">
        <div className="border-b border-slate-200 dark:border-slate-800 pb-4">
          <span className="text-[10px] font-extrabold uppercase tracking-widest text-purple-700 dark:text-purple-300 bg-purple-100 dark:bg-purple-950/60 px-2.5 py-0.5 rounded border border-purple-200 dark:border-purple-800">
            System Settings
          </span>
          <h1 className="text-2xl font-extrabold text-slate-900 dark:text-white tracking-tight mt-1">
            Pipeline & Rule Engine Configurations
          </h1>
          <p className="text-xs text-slate-500 dark:text-slate-400">
            Adjust confidence scoring bounds, automated verification rules, and audit retention settings.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm p-6 space-y-6 transition-colors">
          {/* OCR Threshold */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <label className="text-xs font-bold text-slate-900 dark:text-white">
                Minimum OCR Confidence Threshold (%)
              </label>
              <span className="px-2.5 py-0.5 text-xs font-bold bg-purple-100 dark:bg-purple-950/80 text-purple-800 dark:text-purple-200 rounded border border-purple-200 dark:border-purple-800">
                {formData.ocrConfidenceThreshold}%
              </span>
            </div>
            <input
              type="range"
              min="50"
              max="95"
              step="5"
              value={formData.ocrConfidenceThreshold}
              onChange={(e) => setFormData({ ...formData, ocrConfidenceThreshold: parseInt(e.target.value) })}
              className="w-full h-2 bg-slate-200 dark:bg-slate-800 rounded-lg appearance-none cursor-pointer accent-purple-600"
            />
            <p className="text-[11px] text-slate-500 dark:text-slate-400">
              Records extracted with confidence scores below this value will be automatically routed to the Reviewer Human Verification Queue.
            </p>
          </div>

          <hr className="border-slate-100 dark:border-slate-800" />

          {/* Toggle Features Grid */}
          <div className="space-y-4 text-xs">
            <h4 className="font-bold text-slate-900 dark:text-slate-200 uppercase tracking-wider text-[11px]">
              Automated Validation Modules
            </h4>

            {[
              { key: 'duplicateDetection', title: 'Cross-Database Duplicate Detection', desc: 'Checks survey & khata numbers against registered Odisha revenue records.' },
              { key: 'gisVerification', title: 'Automated GIS Boundary Match Engine', desc: 'Performs spatial polygon geometry cross-validation against Khordha GeoJSON layer.' },
              { key: 'auditLogging', title: 'Immutable Audit Logging', desc: 'Records every field modification, approval, rejection, and session action.' }
            ].map(item => (
              <div key={item.key} className="flex items-start justify-between p-3 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-100 dark:border-slate-700/60">
                <div>
                  <span className="font-bold text-slate-900 dark:text-white block">{item.title}</span>
                  <span className="text-[11px] text-slate-500 dark:text-slate-400">{item.desc}</span>
                </div>
                <input
                  type="checkbox"
                  checked={formData[item.key]}
                  onChange={(e) => setFormData({ ...formData, [item.key]: e.target.checked })}
                  className="w-4 h-4 rounded border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-sky-600 focus:ring-sky-500 cursor-pointer shrink-0 mt-1"
                />
              </div>
            ))}
          </div>

          <div className="pt-4 border-t border-slate-100 dark:border-slate-800 flex justify-end">
            <button
              type="submit"
              className="px-5 py-2.5 bg-sky-600 hover:bg-sky-500 text-white font-bold text-xs rounded-xl shadow-md transition-colors flex items-center gap-2"
            >
              <Save className="w-4 h-4" />
              <span>Save System Settings</span>
            </button>
          </div>
        </form>
      </div>
    </DashboardLayout>
  );
}
