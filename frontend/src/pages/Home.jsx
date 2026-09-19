import React from 'react';
import { Link } from 'react-router-dom';
import { useTheme } from '../context/ThemeContext';
import {
  ShieldCheck,
  FileCheck,
  MapPin,
  Cpu,
  Search,
  ArrowRight,
  Sun,
  Moon,
  Layers,
  Database,
  CheckCircle,
  FileText
} from 'lucide-react';

export default function Home() {
  const { theme, toggleTheme } = useTheme();

  const workflowSteps = [
    { step: '01', title: 'Historical Document Ingestion', desc: 'High-resolution PDF scan upload with district, tehsil, and village indexing.' },
    { step: '02', title: 'AI OCR & Handwriting Extraction', desc: 'Regional language Odia/English OCR with confidence scoring per bounding box.' },
    { step: '03', title: 'Structured Record Transformation', desc: 'NLP entity extraction mapping survey, khata, khasra numbers and owner details.' },
    { step: '04', title: 'Automated Rule Validation', desc: 'Cross-verification against PostGIS cadastral geometry and land right records.' },
    { step: '05', title: 'Human-in-the-Loop Certification', desc: 'Revenue officer verification, conflict resolution, and final VERIFIED status.' },
  ];

  return (
    <div className="min-h-screen bg-[var(--bg-main)] text-[var(--text-primary)] transition-colors flex flex-col">
      {/* Navigation Header */}
      <header className="max-w-7xl mx-auto w-full px-6 py-5 flex items-center justify-between sticky top-0 bg-[var(--bg-main)]/90 backdrop-blur-md z-50 border-b border-[var(--border-color)]">
        <Link to="/" className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-500 to-teal-400 flex items-center justify-center font-bold text-white text-xl shadow-lg shadow-emerald-500/20">
            BN
          </div>
          <div>
            <h1 className="font-bold text-xl tracking-tight text-[var(--text-primary)]">BhuNexis</h1>
            <p className="text-xs text-emerald-500 font-semibold">Land Records AI Platform</p>
          </div>
        </Link>

        <div className="flex items-center space-x-4">
          <button
            onClick={toggleTheme}
            className="p-2.5 rounded-lg bg-[var(--bg-card)] border border-[var(--border-color)] text-[var(--text-primary)] hover:bg-slate-200 dark:hover:bg-slate-700 transition-all cursor-pointer shadow-sm"
          >
            {theme === 'light' ? <Moon className="w-5 h-5" /> : <Sun className="w-5 h-5 text-amber-400" />}
          </button>
          <Link
            to="/login"
            className="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white font-semibold rounded-xl text-sm transition-all shadow-md shadow-emerald-600/20 flex items-center space-x-2"
          >
            <span>Portal Login</span>
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </header>

      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-6 py-16 md:py-24 grid md:grid-cols-2 gap-12 items-center flex-1">
        <div>
          <div className="inline-flex items-center space-x-2 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-600 dark:text-emerald-400 text-xs font-bold mb-6">
            <ShieldCheck className="w-4 h-4" />
            <span>Next-Gen Cadastral & Land Record Digitization</span>
          </div>

          <h1 className="text-4xl md:text-6xl font-extrabold tracking-tight text-[var(--text-primary)] leading-tight">
            Intelligent Land Record <span className="text-emerald-500">Digitization</span> & GIS Platform
          </h1>

          <p className="text-base md:text-lg text-[var(--text-secondary)] mt-6 leading-relaxed">
            BhuNexis unifies AI-driven OCR extraction, automated rule validation, human-in-the-loop review, and PostGIS cadastral map integration into an enterprise government land management solution.
          </p>

          <div className="mt-8 flex flex-wrap gap-4">
            <Link
              to="/login"
              className="px-6 py-3.5 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-xl transition-all shadow-xl shadow-emerald-600/30 flex items-center space-x-2"
            >
              <span>Access System Dashboards</span>
              <ArrowRight className="w-5 h-5" />
            </Link>
            <Link
              to="/u/search"
              className="px-6 py-3.5 bg-[var(--bg-card)] border border-[var(--border-color)] hover:border-emerald-500 text-[var(--text-primary)] font-semibold rounded-xl transition-all shadow-sm flex items-center space-x-2"
            >
              <Search className="w-5 h-5 text-emerald-500" />
              <span>Public Citizen Record Search</span>
            </Link>
          </div>
        </div>

        {/* Feature Visual Grid */}
        <div className="grid grid-cols-2 gap-4 relative">
          <div className="space-y-4">
            <div className="p-6 rounded-2xl bg-[var(--bg-card)] border border-[var(--border-color)] shadow-xl">
              <Cpu className="w-8 h-8 text-emerald-500 mb-3" />
              <h3 className="font-bold text-base text-[var(--text-primary)]">AI OCR & Entity Extraction</h3>
              <p className="text-xs text-[var(--text-secondary)] mt-1">Converts legacy scanned land records & handwritten text into structured JSON fields.</p>
            </div>
            <div className="p-6 rounded-2xl bg-[var(--bg-card)] border border-[var(--border-color)] shadow-xl">
              <MapPin className="w-8 h-8 text-teal-500 mb-3" />
              <h3 className="font-bold text-base text-[var(--text-primary)]">PostGIS Cadastral Overlay</h3>
              <p className="text-xs text-[var(--text-secondary)] mt-1">Interactive polygon mapping linked directly to Survey and Khata numbers.</p>
            </div>
          </div>
          <div className="space-y-4 mt-6">
            <div className="p-6 rounded-2xl bg-[var(--bg-card)] border border-[var(--border-color)] shadow-xl">
              <FileCheck className="w-8 h-8 text-amber-500 mb-3" />
              <h3 className="font-bold text-base text-[var(--text-primary)]">Human Verification Queue</h3>
              <p className="text-xs text-[var(--text-secondary)] mt-1">Side-by-side original document comparison with confidence score badges.</p>
            </div>
            <div className="p-6 rounded-2xl bg-[var(--bg-card)] border border-[var(--border-color)] shadow-xl">
              <ShieldCheck className="w-8 h-8 text-cyan-500 mb-3" />
              <h3 className="font-bold text-base text-[var(--text-primary)]">Immutable Audit Logging</h3>
              <p className="text-xs text-[var(--text-secondary)] mt-1">Every correction, approval, and verification event is permanently logged.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Digitization Workflow Diagram Section */}
      <section className="bg-[var(--bg-card)] border-y border-[var(--border-color)] py-16 transition-colors">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center max-w-2xl mx-auto mb-12">
            <h2 className="text-3xl font-extrabold text-[var(--text-primary)]">Land Record Digitization Workflow</h2>
            <p className="text-sm text-[var(--text-secondary)] mt-2">
              From paper scan ingestion to certified GIS-linked land record verification
            </p>
          </div>

          <div className="grid md:grid-cols-5 gap-4">
            {workflowSteps.map((s, idx) => (
              <div key={idx} className="relative p-5 rounded-xl bg-[var(--bg-main)] border border-[var(--border-color)] flex flex-col justify-between">
                <div>
                  <span className="text-2xl font-black text-emerald-500">{s.step}</span>
                  <h4 className="font-bold text-sm text-[var(--text-primary)] mt-2">{s.title}</h4>
                  <p className="text-xs text-[var(--text-secondary)] mt-1.5 leading-relaxed">{s.desc}</p>
                </div>
                {idx < 4 && (
                  <div className="hidden md:block absolute -right-3 top-1/2 -translate-y-1/2 z-10 bg-emerald-500 text-white p-1 rounded-full text-xs shadow-md">
                    →
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-[var(--border-color)] py-8 text-center text-xs text-[var(--text-muted)] bg-[var(--bg-main)]">
        <p>&copy; {new Date().getFullYear()} BhuNexis Integrated Land Records Platform. Government of India Certified Security Standard.</p>
      </footer>
    </div>
  );
}
