import React from 'react';
import { PIPELINE_STAGES } from '../data/processingData';
import { CheckCircle2, Loader2, Circle } from 'lucide-react';

export function ProcessingTimeline({ currentStageIndex = 0, isComplete = false }) {
  return (
    <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6 shadow-sm">
      <div className="flex items-center justify-between mb-4 border-b border-slate-100 dark:border-slate-800 pb-3">
        <div>
          <h3 className="text-sm font-bold text-slate-900 dark:text-white uppercase tracking-wider">
            Simulated OCR & AI Processing Pipeline
          </h3>
          <p className="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
            Frontend Prototype Simulation Engine • Khordha District Cadastral Dataset
          </p>
        </div>
        <span className="px-2.5 py-1 text-xs font-bold bg-sky-100 dark:bg-sky-950/80 text-sky-800 dark:text-sky-300 rounded-full border border-sky-300 dark:border-sky-700 animate-pulse">
          {isComplete ? 'Pipeline Completed' : `Stage ${currentStageIndex + 1} of ${PIPELINE_STAGES.length}`}
        </span>
      </div>

      {/* Timeline Steps Grid */}
      <div className="space-y-3">
        {PIPELINE_STAGES.map((stage, idx) => {
          let stepStatus = 'upcoming'; // 'completed', 'active', 'upcoming'
          if (idx < currentStageIndex || isComplete) {
            stepStatus = 'completed';
          } else if (idx === currentStageIndex) {
            stepStatus = 'active';
          }

          return (
            <div 
              key={stage.id} 
              className={`p-3 rounded-xl border transition-all flex items-start gap-3 text-xs ${
                stepStatus === 'completed' 
                  ? 'bg-emerald-50/60 dark:bg-emerald-950/40 border-emerald-200 dark:border-emerald-800 text-slate-800 dark:text-slate-200' 
                  : (stepStatus === 'active' 
                      ? 'bg-sky-50 dark:bg-sky-950/60 border-sky-300 dark:border-sky-700 text-slate-900 dark:text-white shadow-sm' 
                      : 'bg-slate-50/40 dark:bg-slate-800/30 border-slate-200 dark:border-slate-800 text-slate-400 dark:text-slate-500')
              }`}
            >
              <div className="mt-0.5 shrink-0">
                {stepStatus === 'completed' && (
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
                )}
                {stepStatus === 'active' && (
                  <Loader2 className="w-4 h-4 text-sky-600 dark:text-sky-400 animate-spin" />
                )}
                {stepStatus === 'upcoming' && (
                  <Circle className="w-4 h-4 text-slate-300 dark:text-slate-600" />
                )}
              </div>

              <div className="flex-1">
                <div className="flex items-center justify-between">
                  <span className={`font-bold ${stepStatus === 'upcoming' ? 'text-slate-500 dark:text-slate-400' : 'text-slate-900 dark:text-white'}`}>
                    {stage.id}. {stage.name}
                  </span>
                  {stepStatus === 'completed' && (
                    <span className="text-[10px] font-semibold text-emerald-700 dark:text-emerald-300 bg-emerald-100/80 dark:bg-emerald-950/80 px-1.5 py-0.2 rounded border border-emerald-200 dark:border-emerald-800">
                      Passed
                    </span>
                  )}
                  {stepStatus === 'active' && (
                    <span className="text-[10px] font-semibold text-sky-700 dark:text-sky-300 bg-sky-100/80 dark:bg-sky-950/80 px-1.5 py-0.2 rounded border border-sky-200 dark:border-sky-800 animate-pulse">
                      Processing...
                    </span>
                  )}
                </div>
                <p className="mt-0.5 text-[11px] text-slate-500 dark:text-slate-400 leading-tight">
                  {stage.description}
                </p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
