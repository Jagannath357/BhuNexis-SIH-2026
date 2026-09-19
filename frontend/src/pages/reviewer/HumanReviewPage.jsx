import React, { useEffect, useState } from 'react';
import DashboardLayout from '../../components/layout/DashboardLayout';
import reviewService from '../../services/reviewService';
import StatusBadge from '../../components/common/StatusBadge';
import { CheckSquare, Save, CheckCircle, XCircle, ShieldCheck, Edit3, FileText, AlertCircle } from 'lucide-react';

export default function HumanReviewPage() {
  const [reviews, setReviews] = useState([]);
  const [selectedReview, setSelectedReview] = useState(null);
  const [loading, setLoading] = useState(true);
  const [actionMsg, setActionMsg] = useState(null);

  // Form edit fields
  const [fields, setFields] = useState({
    owner_name: 'Anil Kumar Das',
    survey_number: '101',
    khasra_number: '205/1',
    khata_number: '25',
    plot_number: '12',
    area: '1.25',
    area_unit: 'ACRE',
    village: 'Sample Village',
    tehsil: 'Jatni',
    district: 'Khordha',
    land_classification: 'AGRICULTURAL',
    land_use: 'CULTIVATED'
  });

  const [confidences] = useState({
    owner_name: 'HIGH',
    survey_number: 'HIGH',
    khasra_number: 'MEDIUM',
    khata_number: 'HIGH',
    plot_number: 'LOW',
    area: 'LOW',
    area_unit: 'HIGH',
    village: 'HIGH',
    tehsil: 'HIGH',
    district: 'HIGH',
    land_classification: 'MEDIUM',
    land_use: 'MEDIUM'
  });

  const [reviewerComment, setReviewerComment] = useState('');

  useEffect(() => {
    fetchReviewCases();
  }, []);

  const fetchReviewCases = async () => {
    setLoading(true);
    try {
      const data = await reviewService.getReviewQueue({ status: 'PENDING' });
      setReviews(data);
      if (data && data.length > 0) {
        setSelectedReview(data[0]);
      }
    } catch (err) {
      console.error("Failed to load review queue:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleFieldChange = (key, value) => {
    setFields((prev) => ({ ...prev, [key]: value }));
  };

  const handleSaveCorrection = async () => {
    if (!selectedReview) return;
    try {
      await reviewService.saveCorrection(selectedReview.id, {
        field_name: 'area',
        corrected_value: fields.area,
        reviewer_comment: reviewerComment || 'Corrected extracted field value'
      });
      setActionMsg('Field correction saved successfully and logged in Audit Trail!');
      setTimeout(() => setActionMsg(null), 4000);
    } catch (err) {
      alert("Failed to save correction: " + (err.message || 'Error'));
    }
  };

  const handleApprove = async () => {
    if (!selectedReview) return;
    try {
      await reviewService.approveReview(selectedReview.id, reviewerComment);
      setActionMsg('Review Case APPROVED!');
      fetchReviewCases();
      setTimeout(() => setActionMsg(null), 4000);
    } catch (err) {
      alert("Approve failed: " + (err.message || 'Error'));
    }
  };

  const handleReject = async () => {
    if (!selectedReview) return;
    try {
      await reviewService.rejectReview(selectedReview.id, reviewerComment);
      setActionMsg('Review Case REJECTED!');
      fetchReviewCases();
      setTimeout(() => setActionMsg(null), 4000);
    } catch (err) {
      alert("Reject failed: " + (err.message || 'Error'));
    }
  };

  const handleVerify = async () => {
    if (!selectedReview) return;
    try {
      await reviewService.verifyReview(selectedReview.id, reviewerComment);
      setActionMsg('Record VERIFIED & Parcel transitioned to VERIFIED status!');
      fetchReviewCases();
      setTimeout(() => setActionMsg(null), 4000);
    } catch (err) {
      alert("Verification failed: " + (err.message || 'Error'));
    }
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl md:text-3xl font-extrabold text-[var(--text-primary)] tracking-tight">
            Human Review & Verification Workspace
          </h1>
          <p className="text-sm text-[var(--text-secondary)] mt-1">
            Compare original scanned document against AI-extracted fields, correct discrepancies & certify land records
          </p>
        </div>

        {actionMsg && (
          <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-600 dark:text-emerald-400 text-xs font-bold flex items-center space-x-2 shadow-sm">
            <CheckCircle className="w-5 h-5 text-emerald-500" />
            <span>{actionMsg}</span>
          </div>
        )}

        {loading ? (
          <div className="p-12 text-center text-emerald-500 font-semibold flex items-center justify-center space-x-3">
            <div className="w-6 h-6 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin" />
            <span>Loading review cases...</span>
          </div>
        ) : (
          <div className="grid lg:grid-cols-12 gap-6">
            {/* Review Selector List */}
            <div className="lg:col-span-3 bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl p-4 space-y-3">
              <h3 className="font-bold text-sm text-[var(--text-primary)] px-2">Review Queue ({reviews.length})</h3>
              <div className="space-y-2 max-h-[600px] overflow-y-auto pr-1">
                {reviews.map((r) => (
                  <button
                    key={r.id}
                    onClick={() => setSelectedReview(r)}
                    className={`w-full text-left p-3 rounded-xl border transition-all cursor-pointer ${
                      selectedReview?.id === r.id
                        ? 'border-emerald-500 bg-emerald-500/10 shadow-md'
                        : 'border-[var(--border-color)] bg-[var(--bg-main)] hover:border-slate-400'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-xs text-amber-500">{r.case_uid}</span>
                      <StatusBadge status={r.priority || 'MEDIUM'} />
                    </div>
                    <p className="text-xs text-[var(--text-primary)] font-semibold mt-1.5">Parcel #{r.parcel_id}</p>
                    <p className="text-[10px] text-[var(--text-muted)] mt-0.5">{r.review_type || 'Validation Match'}</p>
                  </button>
                ))}
              </div>
            </div>

            {/* Side-by-Side Review Interface */}
            {selectedReview ? (
              <div className="lg:col-span-9 grid md:grid-cols-2 gap-6">
                {/* LEFT: Original Document Viewer */}
                <div className="bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl p-5 flex flex-col justify-between shadow-sm">
                  <div>
                    <div className="flex items-center justify-between pb-3 border-b border-[var(--border-color)] mb-4">
                      <div className="flex items-center space-x-2">
                        <FileText className="w-5 h-5 text-emerald-500" />
                        <h3 className="font-bold text-base text-[var(--text-primary)]">Original Document Scan</h3>
                      </div>
                      <span className="text-xs font-mono text-[var(--text-muted)]">DOC-000101.pdf</span>
                    </div>

                    {/* Mock Scanned Document Representation */}
                    <div className="bg-amber-500/5 dark:bg-slate-900 border border-amber-500/20 rounded-xl p-6 text-xs text-slate-700 dark:text-slate-300 font-mono space-y-3 leading-relaxed shadow-inner">
                      <div className="text-center font-bold border-b border-amber-500/20 pb-2 text-amber-800 dark:text-amber-400 text-sm">
                        GOVERNMENT OF ODISHA REVENUE RECORD (KHATIAN)
                      </div>
                      <div className="grid grid-cols-2 gap-2 pt-2">
                        <div><strong>District:</strong> Khordha</div>
                        <div><strong>Tehsil:</strong> Jatni</div>
                        <div><strong>Village:</strong> Sample Village</div>
                        <div><strong>Khata No:</strong> 25</div>
                      </div>
                      <div className="border-t border-amber-500/20 pt-2 space-y-1">
                        <p><strong>Owner Name:</strong> Anil Kumar Das</p>
                        <p><strong>Khasra/Survey No:</strong> 101 (Plot: 12)</p>
                        <p><strong>Area Recorded:</strong> 1.25 ACRE</p>
                        <p><strong>Classification:</strong> AGRICULTURAL</p>
                      </div>
                    </div>
                  </div>

                  <div className="mt-4 p-3 rounded-xl bg-[var(--bg-main)] border border-[var(--border-color)] text-xs">
                    <p className="text-[var(--text-secondary)] font-semibold">Engine System Note:</p>
                    <p className="text-[var(--text-muted)] mt-0.5">{selectedReview.reviewer_notes || 'Field area mismatch requiring verifier confirmation.'}</p>
                  </div>
                </div>

                {/* RIGHT: Extracted Structured Fields & Controls */}
                <div className="bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl p-5 space-y-4 shadow-sm">
                  <div className="flex items-center justify-between pb-3 border-b border-[var(--border-color)]">
                    <div className="flex items-center space-x-2">
                      <Edit3 className="w-5 h-5 text-emerald-500" />
                      <h3 className="font-bold text-base text-[var(--text-primary)]">Extracted Structured Fields</h3>
                    </div>
                    <StatusBadge status={selectedReview.status} />
                  </div>

                  {/* Form fields with confidence badges */}
                  <div className="space-y-3 max-h-[420px] overflow-y-auto pr-1 text-xs">
                    {Object.entries(fields).map(([key, val]) => {
                      const conf = confidences[key] || 'HIGH';
                      const badgeColor = conf === 'HIGH' ? 'text-emerald-500' : conf === 'MEDIUM' ? 'text-amber-500' : 'text-rose-500';
                      return (
                        <div key={key} className="flex items-center justify-between gap-2 p-2 rounded-lg bg-[var(--bg-main)] border border-[var(--border-color)]">
                          <label className="w-1/3 font-semibold uppercase text-[var(--text-secondary)] truncate">
                            {key.replace('_', ' ')}
                          </label>
                          <input
                            type="text"
                            value={val}
                            onChange={(e) => handleFieldChange(key, e.target.value)}
                            className="w-1/2 px-2.5 py-1.5 rounded-lg border border-[var(--border-color)] bg-[var(--bg-card)] text-[var(--text-primary)] font-medium focus:ring-1 focus:ring-emerald-500"
                          />
                          <span className={`w-1/6 text-[10px] font-bold text-right uppercase ${badgeColor}`}>
                            {conf}
                          </span>
                        </div>
                      );
                    })}
                  </div>

                  <div>
                    <label className="block text-xs font-semibold uppercase text-[var(--text-secondary)] mb-1">Reviewer Comment</label>
                    <input
                      type="text"
                      value={reviewerComment}
                      onChange={(e) => setReviewerComment(e.target.value)}
                      placeholder="Add verification notes or explanation..."
                      className="w-full px-3 py-2 rounded-xl border border-[var(--border-color)] bg-[var(--bg-main)] text-[var(--text-primary)] text-xs"
                    />
                  </div>

                  {/* Action Buttons */}
                  <div className="grid grid-cols-2 gap-2 pt-2 border-t border-[var(--border-color)]">
                    <button
                      onClick={handleSaveCorrection}
                      className="py-2 px-3 bg-amber-600 hover:bg-amber-700 text-white font-bold text-xs rounded-xl transition-all flex items-center justify-center space-x-1 cursor-pointer shadow-md"
                    >
                      <Save className="w-3.5 h-3.5" />
                      <span>Save Correction</span>
                    </button>
                    <button
                      onClick={handleApprove}
                      className="py-2 px-3 bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs rounded-xl transition-all flex items-center justify-center space-x-1 cursor-pointer shadow-md"
                    >
                      <CheckCircle className="w-3.5 h-3.5" />
                      <span>Approve Case</span>
                    </button>
                    <button
                      onClick={handleReject}
                      className="py-2 px-3 bg-rose-600 hover:bg-rose-700 text-white font-bold text-xs rounded-xl transition-all flex items-center justify-center space-x-1 cursor-pointer shadow-md"
                    >
                      <XCircle className="w-3.5 h-3.5" />
                      <span>Reject Record</span>
                    </button>
                    <button
                      onClick={handleVerify}
                      className="py-2 px-3 bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs rounded-xl transition-all flex items-center justify-center space-x-1 cursor-pointer shadow-md shadow-emerald-600/20"
                    >
                      <ShieldCheck className="w-3.5 h-3.5" />
                      <span>Final Verify</span>
                    </button>
                  </div>
                </div>
              </div>
            ) : (
              <div className="lg:col-span-9 p-12 text-center text-[var(--text-muted)] bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl">
                No pending review cases selected.
              </div>
            )}
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}
