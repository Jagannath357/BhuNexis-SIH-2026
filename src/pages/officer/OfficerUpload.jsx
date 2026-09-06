import React, { useState, useContext } from 'react';
import { AppContext } from '../../context/AppContext';
import { useAuth } from '../../hooks/useAuth';
import { useToast } from '../../hooks/useToast';
import { DashboardLayout } from '../../components/DashboardLayout';
import { FileUpload } from '../../components/FileUpload';
import { ProcessingTimeline } from '../../components/ProcessingTimeline';
import { ConfidenceBar } from '../../components/ConfidenceBar';
import { StatusBadge } from '../../components/StatusBadge';
import { PIPELINE_STAGES } from '../../data/processingData';
import { 
  UploadCloud, 
  CheckCircle2, 
  ArrowRight, 
  ShieldCheck, 
  AlertTriangle, 
  RotateCcw,
  Send,
  LayoutDashboard
} from 'lucide-react';
import { Link } from 'react-router-dom';

export function OfficerUpload() {
  const { addRecord, addAuditEvent } = useContext(AppContext);
  const { user } = useAuth();
  const { addToast } = useToast();

  const [selectedFile, setSelectedFile] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [currentStage, setCurrentStage] = useState(0);
  const [isComplete, setIsComplete] = useState(false);
  const [extractedRecord, setExtractedRecord] = useState(null);
  const [isSubmitted, setIsSubmitted] = useState(false);

  const startPipeline = () => {
    if (!selectedFile) return;

    setIsProcessing(true);
    setCurrentStage(0);
    setIsComplete(false);
    setIsSubmitted(false);
    setExtractedRecord(null);

    let stage = 0;
    const interval = setInterval(() => {
      stage += 1;
      if (stage < PIPELINE_STAGES.length) {
        setCurrentStage(stage);
      } else {
        clearInterval(interval);
        setIsProcessing(false);
        setIsComplete(true);

        const generatedSurveyNo = `${Math.floor(70 + Math.random() * 80)}/${Math.floor(1 + Math.random() * 5)}`;
        const generatedKhataNo = `${Math.floor(10 + Math.random() * 90)}`;
        const generatedId = `LR-2026-${Math.floor(100 + Math.random() * 900)}`;

        const newRec = {
          id: generatedId,
          documentId: `DOC-${Math.floor(1000 + Math.random() * 9000)}`,
          citizenId: "CIT001",
          ownerName: "Subhashree Jena",
          fatherName: "Bibhuti Jena",
          surveyNumber: generatedSurveyNo,
          khataNumber: generatedKhataNo,
          khasraNumber: `${generatedSurveyNo}-A`,
          area: 1.65,
          areaUnit: "Acres",
          village: "BhuNexis Demo Village",
          tehsil: "Jatni",
          district: "Khordha",
          state: "Odisha",
          landClassification: "Agricultural (Rayati)",
          documentType: selectedFile.name.endsWith('.pdf') ? "Scanned Record of Rights (Patta)" : "Digital Deed Image",
          verificationStatus: "UNDER REVIEW",
          overallConfidence: 84.5,
          extractedFields: {
            ownerName: { value: "Subhashree Jena", confidence: 96, edited: false },
            surveyNumber: { value: generatedSurveyNo, confidence: 88, edited: false },
            khataNumber: { value: generatedKhataNo, confidence: 85, edited: false },
            area: { value: "1.65 Acres", confidence: 79, edited: false },
            village: { value: "BhuNexis Demo Village", confidence: 98, edited: false }
          },
          parcelGeoJsonRef: "PARCEL-106",
          uploadedBy: user?.name || "Arun Kumar Mohanty",
          uploadedAt: new Date().toLocaleString('en-IN', {
            day: '2-digit', month: 'short', year: 'numeric',
            hour: '2-digit', minute: '2-digit', hour12: true
          }),
          verifiedBy: null,
          verifiedAt: null,
          conflictDetails: "Area measurement confidence (79%) below 85% threshold. Routed for human verification.",
          documentUrl: "https://raw.githubusercontent.com/pdfobject/pdfobject.github.io/master/sample-3pp.pdf"
        };

        setExtractedRecord(newRec);
        addRecord(newRec, user?.name);
        addToast(`Document processed successfully. Generated Record ID ${newRec.id}.`, "success");
      }
    }, 350);
  };

  const handleSubmitForReview = () => {
    if (!extractedRecord) return;

    setIsSubmitted(true);
    addAuditEvent({
      userId: user?.id || 'USR-OFF-002',
      userName: user?.name || 'Arun Kumar Mohanty',
      userRole: 'OFFICER',
      action: 'SUBMITTED_FOR_HUMAN_REVIEW',
      actionDisplay: 'Submitted for Human Verification Queue',
      documentId: extractedRecord.documentId,
      field: 'Verification Routing',
      oldValue: 'EXTRACTED',
      newValue: 'UNDER_REVIEW'
    });

    addToast(`Record ${extractedRecord.id} has been successfully submitted for Human Verification.`, "success");
  };

  const handleReset = () => {
    setSelectedFile(null);
    setIsProcessing(false);
    setCurrentStage(0);
    setIsComplete(false);
    setIsSubmitted(false);
    setExtractedRecord(null);
  };

  return (
    <DashboardLayout>
      <div className="space-y-6 max-w-4xl mx-auto">
        {/* Header */}
        <div className="border-b border-slate-200 dark:border-slate-800 pb-4 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <span className="text-[10px] font-extrabold uppercase tracking-widest text-blue-700 dark:text-blue-300 bg-blue-100 dark:bg-blue-950/80 px-2.5 py-0.5 rounded border border-blue-200 dark:border-blue-800">
              Data Ingestion & Processing Cell
            </span>
            <h1 className="text-2xl font-extrabold text-slate-900 dark:text-white tracking-tight mt-1">
              Document Ingestion & Processing
            </h1>
            <p className="text-xs text-slate-500 dark:text-slate-400">
              Upload scanned land records (Patta, Khasra, Sale Deeds) to execute simulated OCR extraction, business validation, and GIS cadastral matching.
            </p>
          </div>

          {isComplete && (
            <button
              onClick={handleReset}
              className="px-4 py-2 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 font-semibold text-xs rounded-xl border border-slate-300 dark:border-slate-700 transition-colors flex items-center gap-1.5 shrink-0"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span>Upload Another Record</span>
            </button>
          )}
        </div>

        {/* Upload Drop Zone Card */}
        <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 shadow-sm p-6 space-y-4">
          <FileUpload onFileSelect={(file) => setSelectedFile(file)} disabled={isProcessing} />

          {selectedFile && !isProcessing && !isComplete && (
            <div className="flex justify-end pt-2">
              <button
                onClick={startPipeline}
                className="px-6 py-3 bg-sky-600 hover:bg-sky-500 text-white font-bold text-xs rounded-xl shadow-lg transition-all flex items-center gap-2"
              >
                <UploadCloud className="w-4 h-4" />
                <span>Execute Document Ingestion & Processing Pipeline</span>
              </button>
            </div>
          )}
        </div>

        {/* 10-Stage Processing Timeline Progress */}
        {(isProcessing || isComplete) && (
          <ProcessingTimeline currentStageIndex={currentStage} isComplete={isComplete} />
        )}

        {/* Comprehensive Extracted Record Summary & Human Verification Handoff */}
        {isComplete && extractedRecord && (
          <div className="bg-emerald-50/80 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800/70 rounded-2xl p-6 space-y-6 shadow-sm">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-emerald-200/60 dark:border-emerald-800/60 pb-4">
              <div className="flex items-center gap-2.5 text-emerald-900 dark:text-emerald-200 font-extrabold text-base">
                <CheckCircle2 className="w-6 h-6 text-emerald-600 dark:text-emerald-400 shrink-0" />
                <div>
                  <h3>Simulated Document Ingestion & Extraction Complete</h3>
                  <p className="text-xs font-normal text-emerald-700 dark:text-emerald-400">
                    Record generated and committed to system repository.
                  </p>
                </div>
              </div>

              <StatusBadge status={extractedRecord.verificationStatus} />
            </div>

            {/* Structured Fields Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 text-xs">
              <div className="p-3 bg-white dark:bg-slate-900 rounded-xl border border-emerald-100 dark:border-emerald-800/60">
                <span className="text-slate-400 dark:text-slate-500 text-[10px] font-bold uppercase block">Record ID & Ref</span>
                <span className="font-mono font-bold text-slate-900 dark:text-white text-sm block">{extractedRecord.id}</span>
                <span className="text-[11px] text-slate-500 dark:text-slate-400 font-mono">{extractedRecord.documentId}</span>
              </div>

              <div className="p-3 bg-white dark:bg-slate-900 rounded-xl border border-emerald-100 dark:border-emerald-800/60">
                <span className="text-slate-400 dark:text-slate-500 text-[10px] font-bold uppercase block">Landowner</span>
                <span className="font-bold text-slate-900 dark:text-white text-sm block">{extractedRecord.ownerName}</span>
                <span className="text-[11px] text-slate-500 dark:text-slate-400">s/o {extractedRecord.fatherName}</span>
              </div>

              <div className="p-3 bg-white dark:bg-slate-900 rounded-xl border border-emerald-100 dark:border-emerald-800/60">
                <span className="text-slate-400 dark:text-slate-500 text-[10px] font-bold uppercase block">Survey / Khata No</span>
                <span className="font-bold text-slate-900 dark:text-white text-sm block">Survey {extractedRecord.surveyNumber}</span>
                <span className="text-[11px] text-slate-500 dark:text-slate-400">Khata No. {extractedRecord.khataNumber}</span>
              </div>

              <div className="p-3 bg-white dark:bg-slate-900 rounded-xl border border-emerald-100 dark:border-emerald-800/60">
                <span className="text-slate-400 dark:text-slate-500 text-[10px] font-bold uppercase block">Plot Area & Classification</span>
                <span className="font-bold text-slate-900 dark:text-white text-sm block">{extractedRecord.area} {extractedRecord.areaUnit}</span>
                <span className="text-[11px] text-slate-500 dark:text-slate-400">{extractedRecord.landClassification}</span>
              </div>

              <div className="p-3 bg-white dark:bg-slate-900 rounded-xl border border-emerald-100 dark:border-emerald-800/60">
                <span className="text-slate-400 dark:text-slate-500 text-[10px] font-bold uppercase block">Mouza / Administrative Center</span>
                <span className="font-bold text-slate-900 dark:text-white text-sm block">{extractedRecord.village}</span>
                <span className="text-[11px] text-slate-500 dark:text-slate-400">{extractedRecord.tehsil}, Khordha, {extractedRecord.state}</span>
              </div>

              <div className="p-3 bg-white dark:bg-slate-900 rounded-xl border border-emerald-100 dark:border-emerald-800/60">
                <span className="text-slate-400 dark:text-slate-500 text-[10px] font-bold uppercase block">Overall OCR Score</span>
                <div className="mt-1">
                  <ConfidenceBar score={extractedRecord.overallConfidence} showValue={true} />
                </div>
              </div>
            </div>

            {/* Technical Verification Breakdown */}
            <div className="p-4 bg-white dark:bg-slate-900 rounded-xl border border-emerald-100 dark:border-emerald-800/60 text-xs space-y-3">
              <h4 className="font-bold text-slate-900 dark:text-white uppercase tracking-wider text-[11px] flex items-center gap-1.5">
                <ShieldCheck className="w-4 h-4 text-sky-600 dark:text-sky-400" />
                <span>Ingestion Pipeline Quality & GIS Verification Report</span>
              </h4>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-[11px]">
                <div className="p-2.5 bg-slate-50 dark:bg-slate-800 rounded-lg border border-slate-200 dark:border-slate-700">
                  <span className="text-slate-500 dark:text-slate-400 block">Business Rule Validation:</span>
                  <span className="font-semibold text-emerald-700 dark:text-emerald-400 block mt-0.5">Passed (24/24 Rules Validated)</span>
                </div>

                <div className="p-2.5 bg-slate-50 dark:bg-slate-800 rounded-lg border border-slate-200 dark:border-slate-700">
                  <span className="text-slate-500 dark:text-slate-400 block">GIS Spatial Boundary Match:</span>
                  <span className="font-semibold text-emerald-700 dark:text-emerald-400 block mt-0.5">Matched (Jatni Cadastral Layer)</span>
                </div>
              </div>

              <div className="p-2.5 bg-amber-50 dark:bg-amber-950/60 border border-amber-200 dark:border-amber-800/80 rounded-lg text-amber-900 dark:text-amber-200 text-[11px] flex items-start gap-2">
                <AlertTriangle className="w-4 h-4 shrink-0 text-amber-600 dark:text-amber-400 mt-0.5" />
                <span>
                  <strong>Routing Decision:</strong> {extractedRecord.conflictDetails}
                </span>
              </div>
            </div>

            {/* Action Handoff Footer */}
            <div className="flex flex-col sm:flex-row items-center justify-between gap-3 pt-2">
              <div className="text-xs text-slate-600 dark:text-slate-400">
                Uploaded by: <strong className="text-slate-900 dark:text-white">{extractedRecord.uploadedBy}</strong> at {extractedRecord.uploadedAt}
              </div>

              {isSubmitted ? (
                <div className="flex flex-wrap items-center justify-end gap-2">
                  <span className="px-3.5 py-2 bg-emerald-100 dark:bg-emerald-950/80 text-emerald-800 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-700 rounded-xl font-extrabold text-xs flex items-center gap-1.5">
                    <CheckCircle2 className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
                    <span>Submitted for Human Verification ✓</span>
                  </span>

                  <Link
                    to="/o/dashboard"
                    className="px-4 py-2 bg-slate-900 dark:bg-slate-800 hover:bg-slate-800 dark:hover:bg-slate-700 text-white font-bold text-xs rounded-xl shadow-sm border border-transparent dark:border-slate-700 flex items-center gap-1.5 transition-colors"
                  >
                    <LayoutDashboard className="w-3.5 h-3.5" />
                    <span>View Ingestion Dashboard</span>
                  </Link>

                  <button
                    onClick={handleReset}
                    className="px-4 py-2 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 font-semibold text-xs rounded-xl border border-slate-300 dark:border-slate-700 transition-colors flex items-center gap-1.5"
                  >
                    <RotateCcw className="w-3.5 h-3.5" />
                    <span>Upload Another</span>
                  </button>
                </div>
              ) : (
                <button
                  onClick={handleSubmitForReview}
                  className="w-full sm:w-auto px-6 py-2.5 bg-sky-600 hover:bg-sky-500 text-white font-extrabold text-xs rounded-xl shadow-md transition-all flex items-center justify-center gap-2"
                >
                  <Send className="w-4 h-4" />
                  <span>Submit for Human Verification</span>
                </button>
              )}
            </div>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}


