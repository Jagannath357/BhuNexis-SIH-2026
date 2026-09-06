import React from 'react';
import { Link } from 'react-router-dom';
import { useTheme } from '../hooks/useTheme';
import { 
  FileCheck, 
  ShieldCheck, 
  Search, 
  Sparkles, 
  Layers, 
  Cpu, 
  History, 
  CheckCircle2, 
  ArrowRight, 
  Lock, 
  Zap, 
  Database,
  Building2,
  FileText,
  Sun,
  Moon
} from 'lucide-react';
import { DisclaimerBanner } from '../components/DisclaimerBanner';

export function Home() {
  const { theme, toggleTheme } = useTheme();

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-900 text-slate-900 dark:text-white font-sans transition-colors">
      <DisclaimerBanner compact={true} />

      {/* Top Landing Header */}
      <header className="border-b border-slate-200 dark:border-slate-800 bg-white/80 dark:bg-slate-950/80 sticky top-0 z-30 backdrop-blur-md transition-colors">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-sky-500 to-indigo-600 p-2 flex items-center justify-center shadow-lg shadow-sky-500/20">
              <FileCheck className="w-6 h-6 text-white" />
            </div>
            <div>
              <span className="font-extrabold text-xl tracking-tight text-slate-900 dark:text-white">BhuNexis</span>
              <span className="ml-2 text-[10px] font-bold uppercase tracking-wider text-sky-700 dark:text-sky-400 bg-sky-100 dark:bg-sky-500/10 px-2 py-0.5 rounded border border-sky-200 dark:border-sky-500/30">
                Portal
              </span>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <button
              onClick={toggleTheme}
              aria-label={theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
              className="p-2 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-100 dark:bg-slate-900 text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-800 transition-all flex items-center gap-1.5 text-xs font-semibold"
              title={theme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
            >
              {theme === 'dark' ? (
                <>
                  <Sun className="w-4 h-4 text-amber-400" />
                  <span className="hidden sm:inline">Light</span>
                </>
              ) : (
                <>
                  <Moon className="w-4 h-4 text-slate-600" />
                  <span className="hidden sm:inline">Dark</span>
                </>
              )}
            </button>

            <Link 
              to="/login"
              className="text-xs font-semibold text-slate-600 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white transition-colors"
            >
              Sign In
            </Link>
            <Link 
              to="/login"
              className="px-4 py-2 text-xs font-bold bg-sky-600 hover:bg-sky-500 text-white rounded-xl shadow-lg shadow-sky-600/30 transition-all flex items-center gap-1.5"
            >
              <span>Explore Platform</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative pt-20 pb-24 px-6 overflow-hidden bg-gradient-to-b from-slate-100 via-slate-50 to-slate-50 dark:from-slate-950 dark:via-slate-900 dark:to-slate-900">
        <div className="max-w-5xl mx-auto text-center relative z-10">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-sky-100 dark:bg-sky-500/10 border border-sky-200 dark:border-sky-500/30 text-sky-800 dark:text-sky-300 text-xs font-semibold mb-6">
            <Sparkles className="w-4 h-4 text-sky-600 dark:text-sky-400" />
            <span>Enterprise Land Record Digitization Platform</span>
          </div>

          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-slate-900 dark:text-white leading-tight">
            Intelligent Land Record <br />
            <span className="bg-gradient-to-r from-sky-600 via-indigo-600 to-emerald-600 dark:from-sky-400 dark:via-indigo-300 dark:to-emerald-400 bg-clip-text text-transparent">
              Digitization & Validation
            </span>
          </h1>

          <p className="mt-4 text-lg font-medium text-slate-700 dark:text-slate-300 max-w-2xl mx-auto">
            "From Legacy Records to Trusted Digital Land Data"
          </p>

          <p className="mt-3 text-sm text-slate-600 dark:text-slate-400 max-w-3xl mx-auto leading-relaxed">
            Transforming historical, handwritten, and scanned legacy land records into structured, searchable, and verified digital GIS parcel datasets through AI-assisted document intelligence.
          </p>

          {/* Call to Actions */}
          <div className="mt-8 flex flex-wrap items-center justify-center gap-4">
            <Link
              to="/login"
              className="px-6 py-3 bg-sky-600 hover:bg-sky-500 text-white font-bold text-sm rounded-xl shadow-xl shadow-sky-600/30 transition-all flex items-center gap-2"
            >
              <span>Launch Demo Credentials Login</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
            <Link
              to="/u/search"
              className="px-6 py-3 bg-white dark:bg-slate-800 hover:bg-slate-100 dark:hover:bg-slate-700 text-slate-800 dark:text-slate-200 border border-slate-200 dark:border-slate-700 font-semibold text-sm rounded-xl transition-all flex items-center gap-2"
            >
              <Search className="w-4 h-4 text-sky-600 dark:text-sky-400" />
              <span>Public Citizen Record Search</span>
            </Link>
          </div>

          {/* Workflow Diagram Strip */}
          <div className="mt-16 p-6 rounded-2xl bg-white/80 dark:bg-slate-950/80 border border-slate-200 dark:border-slate-800 backdrop-blur-md shadow-xl dark:shadow-2xl">
            <h4 className="text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-widest mb-4">
              Core End-to-End Digitization Workflow
            </h4>
            <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-2 text-xs font-semibold">
              {[
                "1. Legacy Scanned Deed",
                "2. Preprocessing & OCR",
                "3. Field Extraction",
                "4. Confidence Scoring",
                "5. Rules Check",
                "6. Human Review",
                "7. Verified GIS Parcel"
              ].map((step, idx) => (
                <div key={idx} className="p-2.5 rounded-lg bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-slate-800 dark:text-slate-300 flex flex-col items-center justify-center text-center">
                  <span className="text-[10px] text-sky-600 dark:text-sky-400 font-bold block mb-1">Step 0{idx + 1}</span>
                  <span className="text-[11px] leading-tight">{step.split('. ')[1]}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Role-Based Platform Capabilities Grid */}
      <section className="py-16 px-6 bg-white dark:bg-slate-950 border-t border-slate-200 dark:border-slate-800">
        <div className="max-w-7xl mx-auto">
          <div className="text-center max-w-2xl mx-auto mb-12">
            <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 dark:text-white tracking-tight">
              Five Specialized User Roles
            </h2>
            <p className="mt-2 text-xs sm:text-sm text-slate-600 dark:text-slate-400">
              Role-Based Access Control (RBAC) designed for complete operational governance.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4">
            {[
              { role: "ADMIN", title: "System Administrator", path: "/a/dashboard", color: "purple", desc: "Governance, user account provisioning, confidence thresholds, system health metrics." },
              { role: "OFFICER", title: "Data Ingestion Specialist", path: "/o/dashboard", color: "blue", desc: "Batch document uploads, simulated OCR execution, extraction error verification." },
              { role: "REVIEWER", title: "Human-in-the-Loop Verifier", path: "/r/dashboard", color: "amber", desc: "Split-screen document review, field editing, approving/rejecting/flagging records." },
              { role: "AUDITOR", title: "Compliance Inspector", path: "/au/dashboard", color: "rose", desc: "Strictly read-only compliance inspection, error rate tracking, immutable audit log." },
              { role: "CITIZEN", title: "Public Landowner", path: "/u/dashboard", color: "emerald", desc: "Public RoR search, certified copy simulation download, grievance submission." }
            ].map((r) => (
              <div key={r.role} className="bg-slate-50 dark:bg-slate-900 rounded-2xl p-5 border border-slate-200 dark:border-slate-800 flex flex-col justify-between hover:border-slate-300 dark:hover:border-slate-700 transition-all">
                <div>
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-slate-200 dark:bg-slate-800 text-sky-700 dark:text-sky-400 border border-slate-300 dark:border-slate-700 inline-block mb-3">
                    {r.role}
                  </span>
                  <h3 className="text-sm font-bold text-slate-900 dark:text-white leading-snug">{r.title}</h3>
                  <p className="mt-2 text-xs text-slate-600 dark:text-slate-400 leading-relaxed">{r.desc}</p>
                </div>
                <Link
                  to="/login"
                  className="mt-4 text-xs font-bold text-sky-600 dark:text-sky-400 hover:text-sky-500 dark:hover:text-sky-300 flex items-center gap-1"
                >
                  <span>Login as {r.role}</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Conceptual Future System Architecture Section */}
      <section className="py-16 px-6 bg-slate-100 dark:bg-slate-900 border-t border-slate-200 dark:border-slate-800">
        <div className="max-w-5xl mx-auto">
          <div className="text-center max-w-2xl mx-auto mb-12">
            <h2 className="text-2xl font-bold text-slate-900 dark:text-white">Target Production System Architecture</h2>
            <p className="text-xs text-slate-600 dark:text-slate-400 mt-1">Enterprise Architecture Blueprint</p>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-center text-xs">
            <div className="p-4 bg-white dark:bg-slate-950 rounded-xl border border-slate-200 dark:border-slate-800">
              <Cpu className="w-6 h-6 text-sky-600 dark:text-sky-400 mx-auto mb-2" />
              <h4 className="font-bold text-slate-900 dark:text-white">Document AI & OCR</h4>
              <p className="text-[11px] text-slate-500 dark:text-slate-400 mt-1">PyTorch • LayoutLM • PaddleOCR</p>
            </div>
            <div className="p-4 bg-white dark:bg-slate-950 rounded-xl border border-slate-200 dark:border-slate-800">
              <Database className="w-6 h-6 text-emerald-600 dark:text-emerald-400 mx-auto mb-2" />
              <h4 className="font-bold text-slate-900 dark:text-white">Database & GIS</h4>
              <p className="text-[11px] text-slate-500 dark:text-slate-400 mt-1">PostgreSQL • PostGIS • Leaflet</p>
            </div>
            <div className="p-4 bg-white dark:bg-slate-950 rounded-xl border border-slate-200 dark:border-slate-800">
              <Zap className="w-6 h-6 text-amber-600 dark:text-amber-400 mx-auto mb-2" />
              <h4 className="font-bold text-slate-900 dark:text-white">Backend & Queue</h4>
              <p className="text-[11px] text-slate-500 dark:text-slate-400 mt-1">FastAPI • Redis • Celery</p>
            </div>
            <div className="p-4 bg-white dark:bg-slate-950 rounded-xl border border-slate-200 dark:border-slate-800">
              <Lock className="w-6 h-6 text-indigo-600 dark:text-indigo-400 mx-auto mb-2" />
              <h4 className="font-bold text-slate-900 dark:text-white">Security & Audit</h4>
              <p className="text-[11px] text-slate-500 dark:text-slate-400 mt-1">JWT Auth • Role Guards • SHA256</p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-950 py-8 px-6 text-center text-xs text-slate-500 dark:text-slate-400">
        <p className="font-semibold text-slate-700 dark:text-slate-300">BhuNexis — Intelligent Land Record System</p>
        <p className="mt-1">District Khordha • Tehsil Jatni • Odisha Demo Environment</p>
      </footer>
    </div>
  );
}
