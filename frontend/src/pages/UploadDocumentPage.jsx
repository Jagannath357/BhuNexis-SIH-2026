import React, { useState } from 'react';
import DashboardLayout from '../components/layout/DashboardLayout';
import documentService from '../services/documentService';
import { FileUp, CheckCircle, AlertCircle, Upload, FileText } from 'lucide-react';

export default function UploadDocumentPage() {
  const [file, setFile] = useState(null);
  const [documentType, setDocumentType] = useState('Khatian / RoR');
  const [language, setLanguage] = useState('odia');
  const [district, setDistrict] = useState('Khordha');
  const [tehsil, setTehsil] = useState('Jatni');
  const [village, setVillage] = useState('Sample Village');
  const [documentDate, setDocumentDate] = useState('');
  
  const [uploading, setUploading] = useState(false);
  const [successResult, setSuccessResult] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setError(null);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError("Please select a PDF document or scan file to upload.");
      return;
    }

    setUploading(true);
    setError(null);
    setSuccessResult(null);

    const formData = new FormData();
    formData.append('file', file);
    formData.append('document_type', documentType);
    formData.append('language', language);
    formData.append('district', district);
    formData.append('tehsil', tehsil);
    formData.append('village', village);
    if (documentDate) formData.append('document_date', documentDate);

    try {
      const res = await documentService.uploadDocument(formData);
      setSuccessResult(res);
      setFile(null);
    } catch (err) {
      setError(err?.message || "Failed to upload document. Check file type and size.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <DashboardLayout>
      <div className="max-w-4xl mx-auto space-y-6">
        <div>
          <h1 className="text-2xl md:text-3xl font-extrabold text-[var(--text-primary)] tracking-tight">
            Ingest Land Record Document
          </h1>
          <p className="text-sm text-[var(--text-secondary)] mt-1">
            Upload PDF scans or image records for AI OCR extraction and automated PostGIS validation
          </p>
        </div>

        {error && (
          <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-600 dark:text-rose-400 text-xs font-semibold flex items-center space-x-2">
            <AlertCircle className="w-5 h-5 flex-shrink-0 text-rose-500" />
            <span>{error}</span>
          </div>
        )}

        {successResult && (
          <div className="p-5 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-700 dark:text-emerald-300 text-sm space-y-2">
            <div className="flex items-center space-x-2 font-bold text-base text-emerald-600 dark:text-emerald-400">
              <CheckCircle className="w-6 h-6" />
              <span>Document Uploaded Successfully!</span>
            </div>
            <p className="text-xs">Document UID: <strong className="font-mono text-emerald-500">{successResult.document_uid}</strong></p>
            <p className="text-xs">Status: <strong className="uppercase">{successResult.processing_status}</strong></p>
          </div>
        )}

        <form onSubmit={handleSubmit} className="bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl p-6 md:p-8 shadow-sm space-y-6">
          {/* Dropzone */}
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-[var(--text-secondary)] mb-2">
              Select Document File (PDF / Images)
            </label>
            <div className="border-2 border-dashed border-[var(--border-color)] hover:border-emerald-500 rounded-2xl p-8 text-center bg-[var(--bg-main)] transition-all cursor-pointer relative">
              <input
                type="file"
                accept=".pdf,.jpg,.jpeg,.png,.tiff"
                onChange={handleFileChange}
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
              />
              <FileUp className="w-10 h-10 text-emerald-500 mx-auto mb-3" />
              {file ? (
                <div className="text-sm font-bold text-emerald-600 dark:text-emerald-400 flex items-center justify-center space-x-2">
                  <FileText className="w-4 h-4" />
                  <span>Selected: {file.name} ({(file.size / 1024 / 1024).toFixed(2)} MB)</span>
                </div>
              ) : (
                <div>
                  <p className="text-sm font-semibold text-[var(--text-primary)]">Click or drag and drop scanned PDF file</p>
                  <p className="text-xs text-[var(--text-muted)] mt-1">Supports PDF, PNG, JPG, TIFF up to 25MB</p>
                </div>
              )}
            </div>
          </div>

          {/* Metadata Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-[var(--text-secondary)] mb-1.5">
                Document Type
              </label>
              <select
                value={documentType}
                onChange={(e) => setDocumentType(e.target.value)}
                className="w-full px-3.5 py-2.5 rounded-xl border border-[var(--border-color)] bg-[var(--bg-main)] text-[var(--text-primary)] text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
              >
                <option value="Khatian / RoR">Khatian / Record of Rights (RoR)</option>
                <option value="Plot Index Map">Plot Index Map</option>
                <option value="Mutation Order">Mutation Order Certificate</option>
                <option value="Deed of Sale">Deed of Sale</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-[var(--text-secondary)] mb-1.5">
                Primary Language
              </label>
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                className="w-full px-3.5 py-2.5 rounded-xl border border-[var(--border-color)] bg-[var(--bg-main)] text-[var(--text-primary)] text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
              >
                <option value="odia">Odia (ଓଡ଼ିଆ)</option>
                <option value="english">English</option>
                <option value="hindi">Hindi</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-[var(--text-secondary)] mb-1.5">
                District
              </label>
              <input
                type="text"
                value={district}
                onChange={(e) => setDistrict(e.target.value)}
                placeholder="Khordha"
                className="w-full px-3.5 py-2.5 rounded-xl border border-[var(--border-color)] bg-[var(--bg-main)] text-[var(--text-primary)] text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-[var(--text-secondary)] mb-1.5">
                Tehsil
              </label>
              <input
                type="text"
                value={tehsil}
                onChange={(e) => setTehsil(e.target.value)}
                placeholder="Jatni"
                className="w-full px-3.5 py-2.5 rounded-xl border border-[var(--border-color)] bg-[var(--bg-main)] text-[var(--text-primary)] text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-[var(--text-secondary)] mb-1.5">
                Village
              </label>
              <input
                type="text"
                value={village}
                onChange={(e) => setVillage(e.target.value)}
                placeholder="Sample Village"
                className="w-full px-3.5 py-2.5 rounded-xl border border-[var(--border-color)] bg-[var(--bg-main)] text-[var(--text-primary)] text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-[var(--text-secondary)] mb-1.5">
                Document Date (Optional)
              </label>
              <input
                type="date"
                value={documentDate}
                onChange={(e) => setDocumentDate(e.target.value)}
                className="w-full px-3.5 py-2.5 rounded-xl border border-[var(--border-color)] bg-[var(--bg-main)] text-[var(--text-primary)] text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={uploading}
            className="w-full py-3.5 px-4 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-xl transition-all flex items-center justify-center space-x-2 cursor-pointer shadow-lg shadow-emerald-600/30 disabled:opacity-50"
          >
            {uploading ? (
              <span>Uploading & Triggering Preprocessing...</span>
            ) : (
              <>
                <Upload className="w-5 h-5" />
                <span>Submit & Upload Document</span>
              </>
            )}
          </button>
        </form>
      </div>
    </DashboardLayout>
  );
}
