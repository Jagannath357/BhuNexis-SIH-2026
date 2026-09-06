import React, { useState, useContext, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { AppContext } from '../../context/AppContext';
import { useAuth } from '../../hooks/useAuth';
import { getLandRecordsForUser } from '../../utils/permissions';
import { DashboardLayout } from '../../components/DashboardLayout';
import { SearchPanel } from '../../components/SearchPanel';
import { LandRecordCard } from '../../components/LandRecordCard';
import { LandRecordTable } from '../../components/LandRecordTable';
import { Modal } from '../../components/Modal';
import { LayoutGrid, Table, Search, FileX, PlusCircle, Info } from 'lucide-react';

export function CitizenSearch() {
  const [searchParams] = useSearchParams();
  const initialQuery = searchParams.get('q') || '';
  const { records } = useContext(AppContext);
  const { user } = useAuth();

  const [viewMode, setViewMode] = useState('grid');
  const [isRegisterModalOpen, setIsRegisterModalOpen] = useState(false);

  // STRICT CITIZEN FILTERING: Get ONLY records belonging to logged-in Citizen
  const userRecords = getLandRecordsForUser(records, user);
  const [searchResults, setSearchResults] = useState(userRecords);

  useEffect(() => {
    // Re-filter when records or user changes
    const base = getLandRecordsForUser(records, user);
    if (initialQuery) {
      handleSearchWithBase(base, { ownerName: initialQuery });
    } else {
      setSearchResults(base);
    }
  }, [initialQuery, records, user]);

  const handleSearchWithBase = (baseRecords, filters) => {
    let filtered = [...baseRecords];

    if (filters.surveyNo) {
      filtered = filtered.filter(r => r.surveyNumber.toLowerCase().includes(filters.surveyNo.toLowerCase()));
    }
    if (filters.khataNo) {
      filtered = filtered.filter(r => r.khataNumber.toLowerCase().includes(filters.khataNo.toLowerCase()));
    }
    if (filters.ownerName) {
      filtered = filtered.filter(r => r.ownerName.toLowerCase().includes(filters.ownerName.toLowerCase()));
    }
    if (filters.village) {
      filtered = filtered.filter(r => r.village.toLowerCase().includes(filters.village.toLowerCase()));
    }
    if (filters.statusFilter && filters.statusFilter !== 'ALL') {
      filtered = filtered.filter(r => r.verificationStatus === filters.statusFilter);
    }

    setSearchResults(filtered);
  };

  const handleSearch = (filters) => {
    handleSearchWithBase(userRecords, filters);
  };

  const handleReset = () => {
    setSearchResults(userRecords);
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <span className="text-[10px] font-extrabold uppercase tracking-widest text-sky-700 dark:text-sky-300 bg-sky-100 dark:bg-sky-950/60 px-2.5 py-0.5 rounded border border-sky-200 dark:border-sky-800">
            Citizen Search Engine
          </span>
          <h1 className="text-2xl font-extrabold text-slate-900 dark:text-white tracking-tight mt-1">
            Search My Land Records
          </h1>
          <p className="text-xs text-slate-500 dark:text-slate-400">
            Search land records registered under your account by Survey Number, Khata Number, or Mouza.
          </p>
        </div>

        {userRecords.length === 0 ? (
          /* Empty State when Citizen owns ZERO land records overall */
          <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-12 text-center shadow-sm space-y-4 max-w-2xl mx-auto my-6 transition-colors">
            <div className="w-16 h-16 rounded-full bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 flex items-center justify-center text-slate-400 mx-auto">
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
          <>
            {/* Search Input Controls */}
            <SearchPanel onSearch={handleSearch} onReset={handleReset} />

            {/* Results Header & Layout Toggle */}
            <div className="flex items-center justify-between border-b border-slate-200 dark:border-slate-800 pb-3">
              <p className="text-xs font-bold text-slate-700 dark:text-slate-300">
                Showing {searchResults.length} Land Record Results
              </p>

              <div className="flex items-center gap-1 bg-slate-100 dark:bg-slate-800 p-1 rounded-xl border border-slate-200 dark:border-slate-700">
                <button
                  onClick={() => setViewMode('grid')}
                  className={`p-1.5 rounded-lg text-xs ${viewMode === 'grid' ? 'bg-white dark:bg-slate-700 shadow text-sky-600 dark:text-sky-400 font-bold' : 'text-slate-500 dark:text-slate-400'}`}
                  title="Grid View"
                >
                  <LayoutGrid className="w-4 h-4" />
                </button>
                <button
                  onClick={() => setViewMode('table')}
                  className={`p-1.5 rounded-lg text-xs ${viewMode === 'table' ? 'bg-white dark:bg-slate-700 shadow text-sky-600 dark:text-sky-400 font-bold' : 'text-slate-500 dark:text-slate-400'}`}
                  title="Table View"
                >
                  <Table className="w-4 h-4" />
                </button>
              </div>
            </div>

            {/* Results Render */}
            {searchResults.length === 0 ? (
              <div className="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-8 text-center text-slate-500 dark:text-slate-400">
                <p className="text-sm font-semibold text-slate-700 dark:text-slate-200">No matching land record found in your records.</p>
                <p className="text-xs text-slate-400 dark:text-slate-500 mt-1">Try searching by Survey Number, Khata Number, or Mouza.</p>
              </div>
            ) : viewMode === 'grid' ? (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {searchResults.map(rec => (
                  <LandRecordCard key={rec.id} record={rec} />
                ))}
              </div>
            ) : (
              <LandRecordTable records={searchResults} role="CITIZEN" />
            )}
          </>
        )}
      </div>

      {/* Land Registration Modal */}
      <Modal
        isOpen={isRegisterModalOpen}
        onClose={() => setIsRegisterModalOpen(false)}
        title="Register New Land Parcel"
      >
        <div className="p-4 text-center space-y-4">
          <div className="w-12 h-12 rounded-full bg-amber-100 dark:bg-amber-950/60 text-amber-600 dark:text-amber-400 flex items-center justify-center mx-auto">
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
            className="px-5 py-2 bg-slate-900 dark:bg-slate-100 text-white dark:text-slate-900 text-xs font-bold rounded-xl"
          >
            Close Window
          </button>
        </div>
      </Modal>
    </DashboardLayout>
  );
}
