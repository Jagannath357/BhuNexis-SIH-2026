import React, { useEffect, useState } from 'react';
import DashboardLayout from '../../components/layout/DashboardLayout';
import { settingsService } from '../../services/settingsService';
import { Settings, Save, CheckCircle, Sliders, Shield } from 'lucide-react';

export default function SystemSettings() {
  const [ocrThreshold, setOcrThreshold] = useState(0.85);
  const [valThreshold, setValThreshold] = useState(0.80);
  const [autoApprove, setAutoApprove] = useState(false);
  const [batchSize, setBatchSize] = useState(50);
  const [district, setDistrict] = useState('Khordha');

  const [loading, setLoading] = useState(true);
  const [msg, setMsg] = useState(null);

  useEffect(() => {
    fetchSettings();
  }, []);

  const fetchSettings = async () => {
    try {
      const res = await settingsService.getSettings();
      const s = res.settings;
      if (s) {
        setOcrThreshold(s.ocr_confidence_threshold ?? 0.85);
        setValThreshold(s.validation_confidence_threshold ?? 0.80);
        setAutoApprove(s.auto_approve_high_confidence ?? false);
        setBatchSize(s.max_batch_upload_size ?? 50);
        setDistrict(s.default_district || 'Khordha');
      }
    } catch (err) {
      console.error("Failed to load settings:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await settingsService.updateSettings({
        ocr_confidence_threshold: parseFloat(ocrThreshold),
        validation_confidence_threshold: parseFloat(valThreshold),
        auto_approve_high_confidence: autoApprove,
        max_batch_upload_size: parseInt(batchSize),
        default_district: district
      });
      setMsg("System settings updated & logged in Audit Trail!");
      setTimeout(() => setMsg(null), 4000);
    } catch (err) {
      alert("Settings update failed: " + (err.message || 'Error'));
    }
  };

  return (
    <DashboardLayout>
      <div className="max-w-4xl mx-auto space-y-6">
        <div>
          <h1 className="text-2xl md:text-3xl font-extrabold text-[var(--text-primary)] tracking-tight">
            System Parameters & Rule Configuration
          </h1>
          <p className="text-sm text-[var(--text-secondary)] mt-1">
            Configure OCR engine confidence thresholds, validation rules & batch limits
          </p>
        </div>

        {msg && (
          <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-600 dark:text-emerald-400 text-xs font-bold flex items-center space-x-2">
            <CheckCircle className="w-5 h-5 text-emerald-500" />
            <span>{msg}</span>
          </div>
        )}

        {loading ? (
          <div className="p-12 text-center text-emerald-500 font-semibold flex items-center justify-center space-x-3">
            <div className="w-6 h-6 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin" />
            <span>Loading system configuration...</span>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl p-6 md:p-8 shadow-sm space-y-6">
            <div className="space-y-4">
              <div>
                <label className="block text-xs font-semibold uppercase tracking-wider text-[var(--text-secondary)] mb-1">
                  OCR Confidence Threshold: {ocrThreshold}
                </label>
                <input
                  type="range"
                  min="0.50"
                  max="0.99"
                  step="0.01"
                  value={ocrThreshold}
                  onChange={(e) => setOcrThreshold(e.target.value)}
                  className="w-full accent-emerald-500"
                />
                <p className="text-[11px] text-[var(--text-muted)] mt-1">Records below this OCR confidence trigger a Human Review case.</p>
              </div>

              <div>
                <label className="block text-xs font-semibold uppercase tracking-wider text-[var(--text-secondary)] mb-1">
                  Validation Engine Threshold: {valThreshold}
                </label>
                <input
                  type="range"
                  min="0.50"
                  max="0.99"
                  step="0.01"
                  value={valThreshold}
                  onChange={(e) => setValThreshold(e.target.value)}
                  className="w-full accent-emerald-500"
                />
                <p className="text-[11px] text-[var(--text-muted)] mt-1">Minimum similarity required for PostGIS parcel geometry & owner name matches.</p>
              </div>

              <div className="pt-2 flex items-center space-x-3">
                <input
                  type="checkbox"
                  id="autoApprove"
                  checked={autoApprove}
                  onChange={(e) => setAutoApprove(e.target.checked)}
                  className="w-4 h-4 accent-emerald-500 rounded"
                />
                <label htmlFor="autoApprove" className="text-xs font-semibold text-[var(--text-primary)] cursor-pointer">
                  Auto-approve records exceeding 98% confidence score
                </label>
              </div>

              <div className="grid grid-cols-2 gap-4 pt-2">
                <div>
                  <label className="block text-xs font-semibold uppercase text-[var(--text-secondary)] mb-1">Max Batch Upload Limit</label>
                  <input
                    type="number"
                    value={batchSize}
                    onChange={(e) => setBatchSize(e.target.value)}
                    className="w-full px-3.5 py-2 rounded-xl border border-[var(--border-color)] bg-[var(--bg-main)] text-[var(--text-primary)] text-xs font-bold"
                  />
                </div>
                <div>
                  <label className="block text-xs font-semibold uppercase text-[var(--text-secondary)] mb-1">Default Ingestion District</label>
                  <input
                    type="text"
                    value={district}
                    onChange={(e) => setDistrict(e.target.value)}
                    className="w-full px-3.5 py-2 rounded-xl border border-[var(--border-color)] bg-[var(--bg-main)] text-[var(--text-primary)] text-xs font-bold"
                  />
                </div>
              </div>
            </div>

            <button
              type="submit"
              className="w-full py-3.5 px-4 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-xl transition-all flex items-center justify-center space-x-2 cursor-pointer shadow-lg shadow-emerald-600/30"
            >
              <Save className="w-4 h-4" />
              <span>Save System Settings</span>
            </button>
          </form>
        )}
      </div>
    </DashboardLayout>
  );
}
