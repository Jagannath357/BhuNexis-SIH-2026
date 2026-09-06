import React, { useState, useContext, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { AppContext } from '../../context/AppContext';
import { useAuth } from '../../hooks/useAuth';
import { useToast } from '../../hooks/useToast';
import { DashboardLayout } from '../../components/DashboardLayout';
import { ConfidenceBar } from '../../components/ConfidenceBar';
import { StatusBadge } from '../../components/StatusBadge';
import { Modal } from '../../components/Modal';
import { 
  FileCheck, 
  CheckCircle2, 
  XCircle, 
  AlertTriangle, 
  Edit3, 
  Save, 
  ChevronLeft, 
  ChevronRight, 
  FileText, 
  Layers, 
  ShieldCheck,
  AlertCircle
} from 'lucide-react';

export function HumanReview() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { records, updateRecord, updateRecordStatus } = useContext(AppContext);
  const { user } = useAuth();
  const { addToast } = useToast();

  const recordIdParam = searchParams.get('id');

  // Filter records needing review or get selected record
  const queueRecords = records.filter(r => 
    r.verificationStatus === 'UNDER REVIEW' || 
    r.verificationStatus === 'LOW CONFIDENCE' || 
    r.verificationStatus === 'CONFLICT' ||
    r.verificationStatus === 'EXTRACTED'
  );

  const [currentIndex, setCurrentIndex] = useState(0);
  const currentRecord = records.find(r => r.id === recordIdParam) || queueRecords[currentIndex] || records[0];

  // Editable Form Fields State
  const [formData, setFormData] = useState({
    ownerName: '',
    fatherName: '',
    surveyNumber: '',
    khataNumber: '',
    area: '',
    village: '',
    landClassification: ''
  });

  const [confirmModal, setConfirmModal] = useState({ open: false, action: null });
  const [conflictReason, setConflictReason] = useState('');

  useEffect(() => {
    if (currentRecord) {
      setFormData({
        ownerName: currentRecord.ownerName || '',
        fatherName: currentRecord.fatherName || '',
        surveyNumber: currentRecord.surveyNumber || '',
        khataNumber: currentRecord.khataNumber || '',
        area: currentRecord.area || '',
        village: currentRecord.village || '',
        landClassification: currentRecord.landClassification || ''
      });
    }
  }, [currentRecord]);

  if (!currentRecord) {
    return (
      <DashboardLayout>
        <div className="text-center py-12 text-slate-500">
          <p className="text-sm font-bold">No records pending human review in queue.</p>
        </div>
      </DashboardLayout>
    );
  }

  const handleFieldChange = (fieldKey, value) => {
    setFormData(prev => ({ ...prev, [fieldKey]: value }));
  };

  const handleSaveChanges = () => {
    const updatedExtractedFields = { ...currentRecord.extractedFields };

    Object.keys(formData).forEach(key => {
      if (updatedExtractedFields[key] && updatedExtractedFields[key].value !== formData[key]) {
        updatedExtractedFields[key] = {
          ...updatedExtractedFields[key],
          previousValue: updatedExtractedFields[key].value,
          value: formData[key],
          edited: true,
          confidence: 99
        };
      }
    });

    updateRecord(currentRecord.id, {
      ...formData,
      extractedFields: updatedExtractedFields
    }, user?.name);

    addToast(`Field updates saved for ${currentRecord.id}.`, 'info');
  };

  const executeStatusAction = () => {
    const action = confirmModal.action;
    setConfirmModal({ open: false, action: null });

    if (action === 'APPROVE') {
      handleSaveChanges();
      updateRecordStatus(currentRecord.id, 'VERIFIED', user?.name);
      addToast(`Record ${currentRecord.id} approved & certified as VERIFIED.`, 'success');
    } else if (action === 'REJECT') {
      updateRecordStatus(currentRecord.id, 'REJECTED', user?.name, conflictReason);
      addToast(`Record ${currentRecord.id} marked as REJECTED.`, 'error');
    } else if (action === 'CONFLICT') {
      updateRecordStatus(currentRecord.id, 'CONFLICT', user?.name, conflictReason || 'Spatial boundary overlap');
      addToast(`Record ${currentRecord.id} flagged for boundary conflict review.`, 'warning');
    }
  };

  return (
    <DashboardLayout>
      <div className="space-y-4">
        {/* Top Control Bar & Queue Nav */}
        {/* Page Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-200 dark:border-slate-800 pb-3">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-[10px] font-extrabold uppercase tracking-widest text-amber-700 dark:text-amber-300 bg-amber-100 dark:bg-amber-950/80 px-2 py-0.5 rounded border border-amber-200 dark:border-amber-800">
                Split-Screen Verification Editor
              </span>
              <StatusBadge status={currentRecord.verificationStatus} size="sm" />
            </div>
            <h1 className="text-xl font-extrabold text-slate-900 dark:text-white tracking-tight mt-1">
              Record Review: {currentRecord.id} ({currentRecord.documentId})
            </h1>
          </div>

          <div className="flex items-center gap-2">
            <button
              disabled={currentIndex === 0}
              onClick={() => setCurrentIndex(prev => Math.max(prev - 1, 0))}
              className="p-1.5 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-700 disabled:opacity-40"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <span className="text-xs font-semibold text-slate-600 dark:text-slate-400">
              Queue {currentIndex + 1} of {Math.max(queueRecords.length, 1)}
            </span>
            <button
              disabled={currentIndex >= queueRecords.length - 1}
              onClick={() => setCurrentIndex(prev => Math.min(prev + 1, queueRecords.length - 1))}
              className="p-1.5 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-700 disabled:opacity-40"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* SPLIT-SCREEN LAYOUT: LEFT DOCUMENT vs RIGHT FORM */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 min-h-[600px]">
          {/* LEFT PANEL: ORIGINAL SCANNED DOCUMENT VIEWER */}
          <div className="lg:col-span-6 bg-slate-900 rounded-2xl border border-slate-800 p-4 flex flex-col justify-between text-white shadow-md">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3 mb-3">
              <div className="flex items-center gap-2">
                <FileText className="w-4 h-4 text-sky-400" />
                <span className="text-xs font-bold">Legacy Document Preview ({currentRecord.documentType})</span>
              </div>
              <span className="text-[10px] text-slate-400 font-mono">Simulated PDF Viewer</span>
            </div>

            {/* Document Image Mock Preview Container */}
            <div className="flex-1 bg-slate-950 rounded-xl border border-slate-800 p-4 flex flex-col items-center justify-center relative overflow-hidden group">
              <div className="w-full max-w-sm bg-amber-50 text-slate-900 p-6 rounded shadow-2xl font-serif border border-amber-200 space-y-4 text-left leading-relaxed text-[11px] transform group-hover:scale-[1.02] transition-transform">
                <div className="border-b border-amber-900/30 pb-2 text-center">
                  <h4 className="font-extrabold uppercase text-xs">RECORD OF RIGHTS (PATTA / KHASRA)</h4>
                  <p className="text-[9px] text-amber-800">GOVERNMENT OF ODISHA • REVENUE DEPARTMENT</p>
                </div>

                <div className="space-y-1 text-[10px]">
                  <p><strong>Landowner Name:</strong> <span className="underline decoration-amber-600 font-semibold">{currentRecord.ownerName}</span></p>
                  <p><strong>Father/Husband:</strong> {currentRecord.fatherName || 'Mohan Chandra Patnaik'}</p>
                  <p><strong>Survey / Khasra No:</strong> <span className="font-bold bg-amber-200 px-1">{currentRecord.surveyNumber}</span></p>
                  <p><strong>Khata Number:</strong> {currentRecord.khataNumber}</p>
                  <p><strong>Plot Area:</strong> {currentRecord.area} {currentRecord.areaUnit}</p>
                  <p><strong>Mouza / Tehsil:</strong> {currentRecord.village}, {currentRecord.tehsil}</p>
                </div>

                <div className="pt-2 border-t border-amber-900/30 text-[9px] text-amber-800 flex justify-between italic">
                  <span>Digitized Seal: Registered 1957</span>
                  <span>Khordha Revenue Registry</span>
                </div>
              </div>

              <span className="absolute bottom-2 right-2 text-[10px] text-slate-500 font-mono bg-slate-900/80 px-2 py-1 rounded">
                Scanned Resolution: 300 DPI
              </span>
            </div>

            {/* Document Controls */}
            <div className="mt-3 text-xs text-slate-400 flex items-center justify-between">
              <span>Uploaded by: {currentRecord.uploadedBy}</span>
              <span>Overall OCR Score: <strong className="text-sky-400">{currentRecord.overallConfidence}%</strong></span>
            </div>
          </div>

          {/* RIGHT PANEL: EXTRACTED STRUCTURED FIELDS & EDIT FORM */}
          <div className="lg:col-span-6 bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6 flex flex-col justify-between shadow-sm transition-colors">
            <div>
              <div className="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3 mb-4">
                <h3 className="text-sm font-bold text-slate-900 dark:text-white uppercase tracking-wider flex items-center gap-2">
                  <Edit3 className="w-4 h-4 text-sky-600 dark:text-sky-400" />
                  <span>Extracted Field Verification & Correction</span>
                </h3>
                <ConfidenceBar score={currentRecord.overallConfidence} showValue={true} />
              </div>

              {/* Conflict / Low Confidence Warning Alert */}
              {currentRecord.verificationStatus === 'LOW CONFIDENCE' && (
                <div className="mb-4 p-3 bg-amber-50 dark:bg-amber-950/60 border border-amber-200 dark:border-amber-800 rounded-xl text-xs text-amber-800 dark:text-amber-200 flex items-start gap-2">
                  <AlertTriangle className="w-4 h-4 shrink-0 text-amber-600 dark:text-amber-400 mt-0.5" />
                  <div>
                    <span className="font-bold block">Low Character Confidence Flag</span>
                    <span>{currentRecord.conflictDetails || 'One or more extracted fields fall below the 85% system confidence threshold.'}</span>
                  </div>
                </div>
              )}

              {/* Form Fields */}
              <div className="space-y-3 text-xs">
                {/* Owner Name */}
                <div>
                  <div className="flex justify-between text-[11px] mb-1">
                    <label className="font-bold text-slate-700 dark:text-slate-300">Landowner Name</label>
                    <span className="text-emerald-700 dark:text-emerald-400 font-semibold">Score: {currentRecord.extractedFields?.ownerName?.confidence || 95}%</span>
                  </div>
                  <input
                    type="text"
                    value={formData.ownerName}
                    onChange={(e) => handleFieldChange('ownerName', e.target.value)}
                    className="w-full bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl p-2.5 font-bold text-slate-900 dark:text-white focus:outline-none focus:border-sky-500"
                  />
                </div>

                {/* Survey Number */}
                <div>
                  <div className="flex justify-between text-[11px] mb-1">
                    <label className="font-bold text-slate-700 dark:text-slate-300">Survey / Khasra Number</label>
                    <span className={`font-semibold ${(currentRecord.extractedFields?.surveyNumber?.confidence || 90) < 70 ? 'text-rose-600 dark:text-rose-400 font-bold animate-pulse' : 'text-emerald-700 dark:text-emerald-400'}`}>
                      Score: {currentRecord.extractedFields?.surveyNumber?.confidence || 90}%
                    </span>
                  </div>
                  <input
                    type="text"
                    value={formData.surveyNumber}
                    onChange={(e) => handleFieldChange('surveyNumber', e.target.value)}
                    className={`w-full border rounded-xl p-2.5 font-bold text-slate-900 dark:text-white focus:outline-none focus:border-sky-500 ${
                      (currentRecord.extractedFields?.surveyNumber?.confidence || 90) < 70 ? 'bg-amber-50 dark:bg-amber-950/60 border-amber-400 dark:border-amber-700' : 'bg-slate-50 dark:bg-slate-800 border-slate-300 dark:border-slate-700'
                    }`}
                  />
                </div>

                {/* Khata Number & Area Row */}
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block font-bold text-slate-700 dark:text-slate-300 text-[11px] mb-1">Khata Number</label>
                    <input
                      type="text"
                      value={formData.khataNumber}
                      onChange={(e) => handleFieldChange('khataNumber', e.target.value)}
                      className="w-full bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl p-2.5 font-bold text-slate-900 dark:text-white focus:outline-none focus:border-sky-500"
                    />
                  </div>

                  <div>
                    <label className="block font-bold text-slate-700 dark:text-slate-300 text-[11px] mb-1">Plot Area (Acres)</label>
                    <input
                      type="text"
                      value={formData.area}
                      onChange={(e) => handleFieldChange('area', e.target.value)}
                      className="w-full bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl p-2.5 font-bold text-slate-900 dark:text-white focus:outline-none focus:border-sky-500"
                    />
                  </div>
                </div>

                {/* Mouza & Classification */}
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block font-bold text-slate-700 dark:text-slate-300 text-[11px] mb-1">Mouza / Village</label>
                    <input
                      type="text"
                      value={formData.village}
                      onChange={(e) => handleFieldChange('village', e.target.value)}
                      className="w-full bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl p-2.5 text-slate-900 dark:text-white focus:outline-none focus:border-sky-500"
                    />
                  </div>

                  <div>
                    <label className="block font-bold text-slate-700 dark:text-slate-300 text-[11px] mb-1">Land Classification</label>
                    <input
                      type="text"
                      value={formData.landClassification}
                      onChange={(e) => handleFieldChange('landClassification', e.target.value)}
                      className="w-full bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl p-2.5 text-slate-900 dark:text-white focus:outline-none focus:border-sky-500"
                    />
                  </div>
                </div>

                {/* GIS Polygon Match Indicator */}
                <div className="p-3 bg-slate-50 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700 rounded-xl flex items-center justify-between text-xs">
                  <div className="flex items-center gap-2">
                    <Layers className="w-4 h-4 text-sky-600 dark:text-sky-400" />
                    <span className="font-bold text-slate-800 dark:text-slate-200">GIS Spatial Boundary Match:</span>
                  </div>
                  <span className="px-2 py-0.5 text-[10px] font-bold bg-emerald-100 dark:bg-emerald-950/80 text-emerald-800 dark:text-emerald-300 rounded border border-emerald-300 dark:border-emerald-700">
                    MATCHED (Jatni Layer)
                  </span>
                </div>
              </div>
            </div>

            {/* ACTION BUTTONS: APPROVE / REJECT / FLAG CONFLICT */}
            <div className="mt-6 pt-4 border-t border-slate-100 dark:border-slate-800 flex flex-wrap items-center justify-between gap-2">
              <button
                type="button"
                onClick={handleSaveChanges}
                className="px-3.5 py-2 text-xs font-semibold bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 rounded-xl transition-colors flex items-center gap-1.5"
              >
                <Save className="w-3.5 h-3.5" />
                <span>Save Field Edits</span>
              </button>

              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={() => setConfirmModal({ open: true, action: 'REJECT' })}
                  className="px-3.5 py-2 text-xs font-bold bg-rose-50 dark:bg-rose-950/60 hover:bg-rose-100 dark:hover:bg-rose-900/60 text-rose-700 dark:text-rose-300 border border-rose-200 dark:border-rose-800 rounded-xl transition-colors flex items-center gap-1"
                >
                  <XCircle className="w-3.5 h-3.5" />
                  <span>Reject Record</span>
                </button>

                <button
                  type="button"
                  onClick={() => setConfirmModal({ open: true, action: 'CONFLICT' })}
                  className="px-3.5 py-2 text-xs font-bold bg-amber-50 dark:bg-amber-950/60 hover:bg-amber-100 dark:hover:bg-amber-900/60 text-amber-700 dark:text-amber-300 border border-amber-200 dark:border-amber-800 rounded-xl transition-colors flex items-center gap-1"
                >
                  <AlertCircle className="w-3.5 h-3.5" />
                  <span>Flag Conflict</span>
                </button>

                <button
                  type="button"
                  onClick={() => setConfirmModal({ open: true, action: 'APPROVE' })}
                  className="px-5 py-2 text-xs font-extrabold bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl shadow-lg transition-all flex items-center gap-1.5"
                >
                  <CheckCircle2 className="w-4 h-4" />
                  <span>Approve & Certify</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Confirmation Modal */}
      <Modal
        isOpen={confirmModal.open}
        onClose={() => setConfirmModal({ open: false, action: null })}
        title={`Confirm Verification Action: ${confirmModal.action}`}
      >
        <div className="space-y-4 text-xs">
          <p className="text-slate-600 dark:text-slate-300">
            Are you sure you want to mark Record <strong className="text-slate-900 dark:text-white">{currentRecord.id}</strong> as <strong className="text-slate-900 dark:text-white">{confirmModal.action}</strong>?
          </p>

          {confirmModal.action !== 'APPROVE' && (
            <div>
              <label className="block font-semibold text-slate-700 dark:text-slate-300 mb-1">Reason / Note for Audit Log</label>
              <textarea
                rows={2}
                value={conflictReason}
                onChange={(e) => setConflictReason(e.target.value)}
                placeholder="e.g. Boundary discrepancy with Survey 89/2 or character ambiguity"
                className="w-full bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-lg p-2 text-xs text-slate-900 dark:text-white placeholder-slate-400 dark:placeholder-slate-500"
              />
            </div>
          )}

          <div className="flex justify-end gap-2 pt-2">
            <button
              onClick={() => setConfirmModal({ open: false, action: null })}
              className="px-3.5 py-2 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 font-semibold rounded-lg"
            >
              Cancel
            </button>
            <button
              onClick={executeStatusAction}
              className="px-4 py-2 bg-slate-900 dark:bg-sky-600 hover:bg-slate-800 dark:hover:bg-sky-500 text-white font-bold rounded-lg shadow-sm"
            >
              Confirm & Apply Status Update
            </button>
          </div>
        </div>
      </Modal>
    </DashboardLayout>
  );
}
