import React, { useState, useContext } from 'react';
import { AppContext } from '../../context/AppContext';
import { useAuth } from '../../hooks/useAuth';
import { getLandRecordsForUser } from '../../utils/permissions';
import { DashboardLayout } from '../../components/DashboardLayout';
import { MapView } from '../../components/MapView';
import { Modal } from '../../components/Modal';
import { DEMO_MAP_PARCELS } from '../../data/mapParcels';
import { FileX, PlusCircle, Info } from 'lucide-react';

export function CitizenMap() {
  const { records } = useContext(AppContext);
  const { user } = useAuth();
  const [isRegisterModalOpen, setIsRegisterModalOpen] = useState(false);

  // Get records for current logged-in Citizen
  const userRecords = getLandRecordsForUser(records, user);
  const userRecordIds = userRecords.map(r => r.id);
  const targetCitizenId = user?.citizenId || user?.id;

  // Filter GeoJSON parcels belonging ONLY to this Citizen
  const filteredGeoJson = {
    ...DEMO_MAP_PARCELS,
    features: DEMO_MAP_PARCELS.features.filter(f => 
      userRecordIds.includes(f.properties.recordId) || f.properties.citizenId === targetCitizenId
    )
  };

  return (
    <DashboardLayout>
      <div className="space-y-4">
        <div>
          <span className="text-[10px] font-extrabold uppercase tracking-widest text-sky-700 dark:text-sky-300 bg-sky-100 dark:bg-sky-950/60 px-2.5 py-0.5 rounded border border-sky-200 dark:border-sky-800">
            My Cadastral Parcels Map
          </span>
          <h1 className="text-2xl font-extrabold text-slate-900 dark:text-white tracking-tight mt-1">
            My Registered Land Parcels
          </h1>
          <p className="text-xs text-slate-500 dark:text-slate-400">
            Interactive GIS parcel map showing land registered under your account in Jatni Tehsil, Khordha.
          </p>
        </div>

        {userRecords.length === 0 ? (
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
          <MapView height="h-[650px]" role="CITIZEN" customGeoJson={filteredGeoJson} />
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
