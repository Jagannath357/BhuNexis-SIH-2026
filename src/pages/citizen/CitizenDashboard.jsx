import React, { useState, useContext } from 'react';
import { Link } from 'react-router-dom';
import { AppContext } from '../../context/AppContext';
import { useAuth } from '../../hooks/useAuth';
import { getLandRecordsForUser } from '../../utils/permissions';
import { DashboardLayout } from '../../components/DashboardLayout';
import { StatCard } from '../../components/StatCard';
import { LandRecordCard } from '../../components/LandRecordCard';
import { Modal } from '../../components/Modal';
import { Search, FileCheck, MapPin, ArrowRight, FileX, CheckCircle2, Clock, AlertCircle, PlusCircle, Info } from 'lucide-react';

export function CitizenDashboard() {
  const { records } = useContext(AppContext);
  const { user } = useAuth();

  const [isRegisterModalOpen, setIsRegisterModalOpen] = useState(false);

  // Filter records specifically for current logged in Citizen
  const userRecords = getLandRecordsForUser(records, user);

  // Personalized stats calculated ONLY from this Citizen's records
  const totalCount = userRecords.length;
  const verifiedCount = userRecords.filter(r => r.verificationStatus === 'VERIFIED').length;
  const underReviewCount = userRecords.filter(r => 
    ['UNDER REVIEW', 'PENDING', 'LOW CONFIDENCE', 'EXTRACTED'].includes(r.verificationStatus)
  ).length;
  const conflictCount = userRecords.filter(r => r.verificationStatus === 'CONFLICT').length;

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Prominent Search Banner */}
        <div className="bg-gradient-to-r from-slate-900 via-sky-950 to-slate-900 text-white rounded-2xl p-8 shadow-xl border border-slate-800 text-center sm:text-left relative overflow-hidden">
          <div className="relative z-10 max-w-2xl">
            <span className="text-[10px] font-extrabold uppercase tracking-widest text-sky-400 bg-sky-500/10 px-2.5 py-0.5 rounded border border-sky-500/30 inline-block mb-2">
              Citizen Land Records Portal
            </span>
            <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight text-white">
              My Land Records & Parcel Status
            </h1>
            <p className="mt-2 text-xs sm:text-sm text-slate-300">
              Welcome back, <strong className="text-white">{user?.name}</strong>. Access land records registered under your account in Jatni Tehsil, Khordha.
            </p>

            <div className="mt-6 flex flex-wrap gap-3">
              <Link
                to="/u/search"
                className="px-6 py-3 bg-sky-600 hover:bg-sky-500 text-white font-bold text-xs rounded-xl shadow-lg transition-all flex items-center gap-2"
              >
                <Search className="w-4 h-4" />
                <span>Search My Registered Lands</span>
              </Link>
              <Link
                to="/u/map"
                className="px-5 py-3 bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold text-xs rounded-xl border border-slate-700 transition-all flex items-center gap-2"
              >
                <MapPin className="w-4 h-4 text-sky-400" />
                <span>My Parcels Map View</span>
              </Link>
            </div>
          </div>
        </div>

        {/* Personalized Citizen Dashboard Stats */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <StatCard title="My Land Records" value={totalCount} subtitle="Registered under my account" icon={FileCheck} color="blue" />
          <StatCard title="Verified Lands" value={verifiedCount} subtitle="Certified Rayati Patta" icon={CheckCircle2} color="emerald" />
          <StatCard title="Under Review" value={underReviewCount} subtitle="Verification pending" icon={Clock} color="amber" />
          <StatCard title="Conflicted Records" value={conflictCount} subtitle="Boundary issues" icon={AlertCircle} color="rose" />
        </div>

        {/* Main Content: Land Records Grid OR Empty State */}
        {totalCount === 0 ? (
          <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-12 text-center shadow-sm space-y-4 max-w-2xl mx-auto my-6 transition-colors">
            <div className="w-16 h-16 rounded-full bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 flex items-center justify-center text-slate-400 dark:text-slate-500 mx-auto">
              <FileX className="w-8 h-8" />
            </div>

            <div>
              <h3 className="text-lg font-extrabold text-slate-900 dark:text-white">No Land Records Found</h3>
              <p className="text-xs text-slate-500 dark:text-slate-400 mt-1 max-w-md mx-auto">
                You have not registered any land records with BhuNexis yet.
              </p>
            </div>

            <div className="pt-2">
              <button
                onClick={() => setIsRegisterModalOpen(true)}
                className="px-5 py-2.5 bg-sky-600 hover:bg-sky-500 text-white font-bold text-xs rounded-xl shadow-md transition-all inline-flex items-center gap-2"
              >
                <PlusCircle className="w-4 h-4" />
                <span>Register / Add Land</span>
              </button>
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-base font-extrabold text-slate-900 dark:text-white">
                  My Registered Land Records ({totalCount})
                </h3>
                <p className="text-xs text-slate-500 dark:text-slate-400">
                  Land records registered under your account in Khordha District.
                </p>
              </div>

              <Link to="/u/search" className="text-xs font-bold text-sky-600 dark:text-sky-400 hover:text-sky-800 dark:hover:text-sky-300 flex items-center gap-1">
                <span>Search My Records</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {userRecords.map(record => (
                <LandRecordCard key={record.id} record={record} />
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Land Registration Modal */}
      <Modal
        isOpen={isRegisterModalOpen}
        onClose={() => setIsRegisterModalOpen(false)}
        title="Register New Land Parcel"
      >
        <div className="p-4 text-center space-y-4">
          <div className="w-12 h-12 rounded-full bg-amber-100 dark:bg-amber-950/80 text-amber-600 dark:text-amber-400 flex items-center justify-center mx-auto">
            <Info className="w-6 h-6" />
          </div>
          <div>
            <h4 className="text-sm font-bold text-slate-900 dark:text-white">Prototype Demo Notice</h4>
            <p className="text-xs text-slate-600 dark:text-slate-300 mt-1">
              Land registration functionality is not available in this prototype.
            </p>
          </div>
          <button
            onClick={() => setIsRegisterModalOpen(false)}
            className="px-5 py-2 bg-slate-900 dark:bg-sky-600 hover:bg-slate-800 dark:hover:bg-sky-500 text-white text-xs font-bold rounded-xl"
          >
            Close Window
          </button>
        </div>
      </Modal>
    </DashboardLayout>
  );
}
