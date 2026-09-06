import React, { useState, useContext } from 'react';
import { useParams, Link } from 'react-router-dom';
import { AppContext } from '../../context/AppContext';
import { useAuth } from '../../hooks/useAuth';
import { useToast } from '../../hooks/useToast';
import { canUserAccessRecord } from '../../utils/permissions';
import { DashboardLayout } from '../../components/DashboardLayout';
import { StatusBadge } from '../../components/StatusBadge';
import { Modal } from '../../components/Modal';
import { downloadMockCertifiedRecord } from '../../utils/downloadMockRecord';
import { 
  Download, 
  AlertCircle, 
  QrCode, 
  ArrowLeft,
  ShieldAlert,
  Lock
} from 'lucide-react';

export function LandRecordDetails() {
  const { id } = useParams();
  const { records, submitGrievance } = useContext(AppContext);
  const { user } = useAuth();
  const { addToast } = useToast();

  const record = records.find(r => r.id === id);

  const [isGrievanceModalOpen, setIsGrievanceModalOpen] = useState(false);
  const [grievanceForm, setGrievanceForm] = useState({
    issueType: 'Incorrect Owner Name',
    description: '',
    contactEmail: ''
  });

  // AUTHORIZATION CHECK FOR CITIZENS
  const isAuthorized = record && canUserAccessRecord(record, user);

  if (!record || !isAuthorized) {
    return (
      <DashboardLayout>
        <div className="min-h-[60vh] flex flex-col items-center justify-center text-center p-6 max-w-lg mx-auto">
          <div className="w-16 h-16 rounded-full bg-rose-100 dark:bg-rose-950/80 border border-rose-200 dark:border-rose-800 flex items-center justify-center text-rose-600 dark:text-rose-400 mb-4 shadow-sm">
            <ShieldAlert className="w-8 h-8" />
          </div>

          <h2 className="text-2xl font-extrabold text-slate-900 dark:text-white tracking-tight">
            Access Denied
          </h2>

          <p className="mt-2 text-xs text-slate-600 dark:text-slate-300 leading-relaxed font-semibold">
            You are not authorized to view this land record.
          </p>

          <p className="mt-1 text-xs text-slate-500 dark:text-slate-400 max-w-md">
            Under strict privacy enforcement, Citizen accounts can only view certified land records belonging to their own account.
          </p>

          <div className="mt-6">
            <Link
              to="/u/search"
              className="px-5 py-2.5 bg-sky-600 hover:bg-sky-500 text-white font-bold text-xs rounded-xl shadow-md transition-colors inline-flex items-center gap-2"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>Back to My Land Records</span>
            </Link>
          </div>
        </div>
      </DashboardLayout>
    );
  }

  const handleDownload = () => {
    downloadMockCertifiedRecord(record);
    addToast('Prototype certified copy downloaded in Demo Mode.', 'success');
  };

  const handleGrievanceSubmit = (e) => {
    e.preventDefault();
    submitGrievance({
      recordId: record.id,
      ...grievanceForm
    });
    setIsGrievanceModalOpen(false);
    addToast('Grievance correction request submitted successfully (Demo Mode).', 'success');
  };

  return (
    <DashboardLayout>
      <div className="space-y-6 max-w-4xl mx-auto">
        {/* Navigation Back Link */}
        <Link to="/u/search" className="text-xs font-bold text-sky-600 dark:text-sky-400 hover:text-sky-800 dark:hover:text-sky-300 flex items-center gap-1 inline-flex">
          <ArrowLeft className="w-4 h-4" />
          <span>Back to My Land Records</span>
        </Link>

        {/* Main Document Details Card */}
        <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-xl overflow-hidden transition-colors">
          {/* Header Banner */}
          <div className="bg-gradient-to-r from-slate-900 to-slate-800 text-white p-6 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
            <div>
              <span className="text-[10px] font-extrabold uppercase tracking-widest text-sky-400 bg-sky-500/10 px-2 py-0.5 rounded border border-sky-500/30">
                Official Record Excerpt
              </span>
              <h1 className="text-2xl font-extrabold tracking-tight mt-1 text-white">{record.ownerName}</h1>
              <p className="text-xs text-slate-400 mt-0.5">
                Record ID: <span className="font-mono text-white font-bold">{record.id}</span> • Mouza: {record.village}
              </p>
            </div>

            <StatusBadge status={record.verificationStatus} />
          </div>

          {/* Body Content */}
          <div className="p-6 space-y-6 text-xs text-slate-800 dark:text-slate-200">
            {/* Disclaimer Bar */}
            <div className="p-3 bg-amber-50 dark:bg-amber-950/60 border border-amber-200 dark:border-amber-800 rounded-xl text-amber-900 dark:text-amber-200 text-[11px] leading-relaxed flex items-start gap-2">
              <AlertCircle className="w-4 h-4 shrink-0 text-amber-600 dark:text-amber-400 mt-0.5" />
              <span>
                <strong>PROTOTYPE CERTIFIED COPY DEMO:</strong> This record view is generated by the BhuNexis simulation model. Data shown is simulated and does not constitute an official legal certificate.
              </span>
            </div>

            {/* Grid Specifications */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              <div className="p-3 bg-slate-50 dark:bg-slate-800/80 rounded-xl border border-slate-100 dark:border-slate-700">
                <span className="text-slate-400 dark:text-slate-500 text-[10px] font-semibold uppercase block">Landowner</span>
                <span className="font-bold text-slate-900 dark:text-white text-sm block">{record.ownerName}</span>
                <span className="text-[11px] text-slate-500 dark:text-slate-400">s/o {record.fatherName || 'N/A'}</span>
              </div>

              <div className="p-3 bg-slate-50 dark:bg-slate-800/80 rounded-xl border border-slate-100 dark:border-slate-700">
                <span className="text-slate-400 dark:text-slate-500 text-[10px] font-semibold uppercase block">Survey / Plot No</span>
                <span className="font-bold text-slate-900 dark:text-white text-sm block">{record.surveyNumber}</span>
                <span className="text-[11px] text-slate-500 dark:text-slate-400">Khasra: {record.khasraNumber || record.surveyNumber}</span>
              </div>

              <div className="p-3 bg-slate-50 dark:bg-slate-800/80 rounded-xl border border-slate-100 dark:border-slate-700">
                <span className="text-slate-400 dark:text-slate-500 text-[10px] font-semibold uppercase block">Khata Number</span>
                <span className="font-bold text-slate-900 dark:text-white text-sm block">Khata No. {record.khataNumber}</span>
                <span className="text-[11px] text-slate-500 dark:text-slate-400">Mouza Patta Registry</span>
              </div>

              <div className="p-3 bg-slate-50 dark:bg-slate-800/80 rounded-xl border border-slate-100 dark:border-slate-700">
                <span className="text-slate-400 dark:text-slate-500 text-[10px] font-semibold uppercase block">Plot Area</span>
                <span className="font-bold text-slate-900 dark:text-white text-sm block">{record.area} {record.areaUnit}</span>
                <span className="text-[11px] text-slate-500 dark:text-slate-400">Classification: {record.landClassification}</span>
              </div>

              <div className="p-3 bg-slate-50 dark:bg-slate-800/80 rounded-xl border border-slate-100 dark:border-slate-700">
                <span className="text-slate-400 dark:text-slate-500 text-[10px] font-semibold uppercase block">Administrative Region</span>
                <span className="font-bold text-slate-900 dark:text-white text-sm block">{record.village}</span>
                <span className="text-[11px] text-slate-500 dark:text-slate-400">{record.tehsil}, Khordha, {record.state}</span>
              </div>

              <div className="p-3 bg-slate-50 dark:bg-slate-800/80 rounded-xl border border-slate-100 dark:border-slate-700">
                <span className="text-slate-400 dark:text-slate-500 text-[10px] font-semibold uppercase block">Verification Status</span>
                <span className="font-bold text-slate-900 dark:text-white text-sm block">{record.verificationStatus}</span>
                <span className="text-[11px] text-slate-500 dark:text-slate-400">Confidence: {record.overallConfidence}%</span>
              </div>
            </div>

            {/* Simulated QR Code & Digital Seal Matrix */}
            <div className="p-4 bg-slate-900 text-white rounded-xl flex flex-col sm:flex-row items-center justify-between gap-4">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 rounded-lg bg-slate-800 border border-slate-700 flex items-center justify-center text-sky-400 shrink-0">
                  <QrCode className="w-7 h-7" />
                </div>
                <div>
                  <h4 className="font-bold text-xs">Simulated Digital Seal & Verification Matrix</h4>
                  <p className="text-[10px] text-slate-400 font-mono">
                    SHA256: {Math.random().toString(36).substr(2, 16).toUpperCase()}-BHUNEXIS
                  </p>
                </div>
              </div>

              <div className="flex items-center gap-2">
                <button
                  onClick={handleDownload}
                  className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs rounded-xl shadow-md transition-colors flex items-center gap-1.5"
                >
                  <Download className="w-4 h-4" />
                  <span>Download Certified Copy</span>
                </button>
                <button
                  onClick={() => setIsGrievanceModalOpen(true)}
                  className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold text-xs rounded-xl border border-slate-700 transition-colors"
                >
                  Submit Grievance
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Grievance Modal */}
      <Modal
        isOpen={isGrievanceModalOpen}
        onClose={() => setIsGrievanceModalOpen(false)}
        title="Submit Grievance / Correction Request (Demo Mode)"
      >
        <form onSubmit={handleGrievanceSubmit} className="space-y-4 text-xs">
          <div>
            <label className="block font-semibold text-slate-700 dark:text-slate-300 mb-1">Select Issue Category</label>
            <select
              value={grievanceForm.issueType}
              onChange={(e) => setGrievanceForm({ ...grievanceForm, issueType: e.target.value })}
              className="w-full bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 text-slate-900 dark:text-white rounded-lg p-2 text-xs font-semibold focus:outline-none focus:border-sky-500"
            >
              <option value="Incorrect Owner Name">Incorrect Owner Name Spelling</option>
              <option value="Incorrect Survey Number">Incorrect Survey / Plot Number</option>
              <option value="Incorrect Area">Incorrect Plot Area Measurement</option>
              <option value="Incorrect Village">Incorrect Mouza / Tehsil Classification</option>
              <option value="Other">Other Discrepancy</option>
            </select>
          </div>

          <div>
            <label className="block font-semibold text-slate-700 dark:text-slate-300 mb-1">Detailed Description of Discrepancy</label>
            <textarea
              rows={3}
              required
              placeholder="Describe the discrepancy with historical Patta reference..."
              value={grievanceForm.description}
              onChange={(e) => setGrievanceForm({ ...grievanceForm, description: e.target.value })}
              className="w-full bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 text-slate-900 dark:text-white placeholder-slate-400 dark:placeholder-slate-500 rounded-lg p-2 text-xs focus:outline-none focus:border-sky-500"
            />
          </div>

          <div>
            <label className="block font-semibold text-slate-700 dark:text-slate-300 mb-1">Contact Email Address</label>
            <input
              type="email"
              required
              placeholder="citizen@bhoomiai.demo"
              value={grievanceForm.contactEmail}
              onChange={(e) => setGrievanceForm({ ...grievanceForm, contactEmail: e.target.value })}
              className="w-full bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 text-slate-900 dark:text-white placeholder-slate-400 dark:placeholder-slate-500 rounded-lg p-2 text-xs focus:outline-none focus:border-sky-500"
            />
          </div>

          <div className="pt-2 flex justify-end gap-2">
            <button
              type="button"
              onClick={() => setIsGrievanceModalOpen(false)}
              className="px-3.5 py-2 text-xs font-semibold text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 text-xs font-bold bg-sky-600 text-white hover:bg-sky-500 rounded-lg shadow-sm"
            >
              Submit Grievance Request
            </button>
          </div>
        </form>
      </Modal>
    </DashboardLayout>
  );
}
