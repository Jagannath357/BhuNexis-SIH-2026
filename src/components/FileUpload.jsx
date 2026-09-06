import React, { useState, useRef } from 'react';
import { UploadCloud, FileText, AlertCircle, CheckCircle2, X } from 'lucide-react';
import { validateUploadFile } from '../utils/validators';

export function FileUpload({ onFileSelect, disabled = false }) {
  const [dragActive, setDragActive] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [errorMsg, setErrorMsg] = useState(null);
  const inputRef = useRef(null);

  const handleFiles = (files) => {
    if (!files || files.length === 0) return;
    const file = files[0];
    setErrorMsg(null);

    const validation = validateUploadFile(file);
    if (!validation.valid) {
      setErrorMsg(validation.error);
      setSelectedFile(null);
      return;
    }

    setSelectedFile(file);
    if (onFileSelect) {
      onFileSelect(file);
    }
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFiles(e.dataTransfer.files);
    }
  };

  const clearFile = () => {
    setSelectedFile(null);
    setErrorMsg(null);
    if (inputRef.current) inputRef.current.value = '';
  };

  return (
    <div className="w-full">
      <div
        onDragEnter={handleDrag}
        onDragOver={handleDrag}
        onDragLeave={handleDrag}
        onDrop={handleDrop}
        onClick={() => !disabled && inputRef.current?.click()}
        className={`
          relative border-2 border-dashed rounded-2xl p-8 text-center cursor-pointer transition-all
          ${dragActive 
            ? 'border-sky-500 bg-sky-50/60 dark:bg-sky-950/40 scale-[1.01]' 
            : 'border-slate-300 dark:border-slate-700 hover:border-sky-400 dark:hover:border-sky-500 bg-white dark:bg-slate-900 hover:bg-slate-50/50 dark:hover:bg-slate-800/50'
          }
          ${disabled ? 'opacity-50 pointer-events-none' : ''}
        `}
      >
        <input
          ref={inputRef}
          type="file"
          accept=".pdf,.jpg,.jpeg,.png"
          onChange={(e) => handleFiles(e.target.files)}
          className="hidden"
        />

        <div className="w-14 h-14 mx-auto rounded-2xl bg-sky-100/80 dark:bg-sky-950/60 border border-sky-200 dark:border-sky-800 flex items-center justify-center text-sky-600 dark:text-sky-400 shadow-sm mb-4">
          <UploadCloud className="w-7 h-7" />
        </div>

        <h4 className="text-sm font-bold text-slate-800 dark:text-slate-100">
          Drag & Drop Land Record File Here
        </h4>
        <p className="text-xs text-slate-500 dark:text-slate-400 mt-1 max-w-sm mx-auto">
          Supported Formats: <span className="font-semibold text-slate-700 dark:text-slate-300">PDF, JPG, JPEG, PNG</span> (Max 10 MB). Scanned deeds, RoR, Patta, or Khasra documents.
        </p>

        <button
          type="button"
          className="mt-4 px-4 py-2 text-xs font-semibold bg-slate-900 dark:bg-slate-800 text-white hover:bg-slate-800 dark:hover:bg-slate-700 rounded-lg shadow-sm border border-transparent dark:border-slate-700 transition-colors inline-flex items-center gap-1.5"
        >
          <span>Browse File System</span>
        </button>
      </div>

      {/* Error Alert */}
      {errorMsg && (
        <div className="mt-3 p-3 bg-rose-50 dark:bg-rose-950/80 border border-rose-200 dark:border-rose-800 rounded-xl text-xs text-rose-700 dark:text-rose-300 flex items-start gap-2">
          <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
          <span>{errorMsg}</span>
        </div>
      )}

      {/* Selected File Card Preview */}
      {selectedFile && (
        <div className="mt-3 p-4 bg-sky-50/80 dark:bg-sky-950/40 border border-sky-200 dark:border-sky-800 rounded-xl flex items-center justify-between gap-3 text-xs">
          <div className="flex items-center gap-3 overflow-hidden">
            <div className="p-2 rounded-lg bg-sky-600 text-white shrink-0">
              <FileText className="w-5 h-5" />
            </div>
            <div className="overflow-hidden">
              <p className="font-bold text-slate-900 dark:text-white truncate">{selectedFile.name}</p>
              <p className="text-[11px] text-slate-500 dark:text-slate-400">
                {(selectedFile.size / (1024 * 1024)).toFixed(2)} MB • {selectedFile.type}
              </p>
            </div>
          </div>
          <button
            onClick={(e) => {
              e.stopPropagation();
              clearFile();
            }}
            className="p-1 rounded-lg hover:bg-sky-100 dark:hover:bg-sky-900 text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-white"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      )}
    </div>
  );
}
