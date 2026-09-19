import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import DashboardLayout from '../../components/layout/DashboardLayout';
import StatCard from '../../components/common/StatCard';
import StatusBadge from '../../components/common/StatusBadge';
import { dashboardService } from '../../services/settingsService';
import citizenService from '../../services/citizenService';
import { Search, Download, MapPin, FileCheck, Shield, HelpCircle, AlertCircle } from 'lucide-react';

export default function CitizenDashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [downloadMsg, setDownloadMsg] = useState(null);

  useEffect(() => {
    fetchCitizenStats();
  }, []);

  const fetchCitizenStats = async () => {
    try {
      const res = await dashboardService.getCitizenDashboard();
      setData(res.data);
    } catch (err) {
      console.error("Failed to fetch citizen stats:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async (parcelId) => {
    try {
      const res = await citizenService.downloadCertifiedRecord(parcelId);
      setDownloadMsg(`Certified Digital Copy Issued! Certificate ID: ${res.certificate_id}`);
      setTimeout(() => setDownloadMsg(null), 5000);
    } catch (err) {
      alert("Unable to download certificate: " + (err.message || "Record error"));
    }
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl md:text-3xl font-extrabold text-[var(--text-primary)] tracking-tight">
            Citizen & Landowner Portal
          </h1>
          <p className="text-sm text-[var(--text-secondary)] mt-1">
            Access your verified land holdings, search public records & download official certified documents
          </p>
        </div>

        {downloadMsg && (
          <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-600 dark:text-emerald-400 text-xs font-bold flex items-center space-x-2">
            <FileCheck className="w-5 h-5 text-emerald-500" />
            <span>{downloadMsg}</span>
          </div>
        )}

        {loading ? (
          <div className="p-12 text-center text-emerald-500 font-semibold flex items-center justify-center space-x-3">
            <div className="w-6 h-6 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin" />
            <span>Retrieving your authorized land records...</span>
          </div>
        ) : (
          <>
            {/* Action Cards */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-5">
              <StatCard title="My Verified Holdings" value={data?.my_verified_records_count || 0} icon={FileCheck} color="emerald" subtitle="Authenticated land titles" />
              
              <Link to="/u/search" className="bg-[var(--bg-card)] border border-[var(--border-color)] hover:border-emerald-500 rounded-xl p-5 shadow-sm transition-all group cursor-pointer flex items-center justify-between">
                <div>
                  <p className="text-xs font-semibold uppercase tracking-wider text-[var(--text-secondary)]">Public Search</p>
                  <h3 className="text-lg font-bold text-[var(--text-primary)] mt-1 group-hover:text-emerald-500">Search Records</h3>
                  <p className="text-xs text-[var(--text-muted)] mt-1">By Survey, Khata or Village</p>
                </div>
                <div className="p-3 rounded-xl bg-blue-500/10 text-blue-500 border border-blue-500/20">
                  <Search className="w-6 h-6" />
                </div>
              </Link>

              <Link to="/map" className="bg-[var(--bg-card)] border border-[var(--border-color)] hover:border-emerald-500 rounded-xl p-5 shadow-sm transition-all group cursor-pointer flex items-center justify-between">
                <div>
                  <p className="text-xs font-semibold uppercase tracking-wider text-[var(--text-secondary)]">GIS Map</p>
                  <h3 className="text-lg font-bold text-[var(--text-primary)] mt-1 group-hover:text-emerald-500">View Cadastral Map</h3>
                  <p className="text-xs text-[var(--text-muted)] mt-1">Interactive polygon boundaries</p>
                </div>
                <div className="p-3 rounded-xl bg-teal-500/10 text-teal-500 border border-teal-500/20">
                  <MapPin className="w-6 h-6" />
                </div>
              </Link>
            </div>

            {/* My Land Records List */}
            <div className="bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl p-6 shadow-sm">
              <h3 className="text-lg font-bold text-[var(--text-primary)] mb-4">My Verified Land Titles</h3>
              {data?.my_parcels?.length === 0 ? (
                <div className="p-8 text-center border border-dashed border-[var(--border-color)] rounded-xl text-[var(--text-muted)] text-sm">
                  No verified records registered under your name yet.
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {data?.my_parcels?.map((p) => (
                    <div key={p.id} className="p-5 rounded-xl border border-[var(--border-color)] bg-[var(--bg-main)] flex flex-col justify-between space-y-4">
                      <div className="flex items-center justify-between">
                        <span className="font-bold text-base text-emerald-600 dark:text-emerald-400">{p.parcel_uid}</span>
                        <StatusBadge status={p.status} />
                      </div>

                      <div className="grid grid-cols-2 gap-2 text-xs">
                        <div><span className="text-[var(--text-secondary)]">Survey No:</span> <strong className="text-[var(--text-primary)]">{p.survey_number}</strong></div>
                        <div><span className="text-[var(--text-secondary)]">Khata No:</span> <strong className="text-[var(--text-primary)]">{p.khata_number}</strong></div>
                        <div><span className="text-[var(--text-secondary)]">Village:</span> <span className="text-[var(--text-primary)] font-semibold">{p.village}</span></div>
                        <div><span className="text-[var(--text-secondary)]">Area:</span> <span className="text-[var(--text-primary)] font-semibold">{p.recorded_area} {p.recorded_area_unit}</span></div>
                      </div>

                      <div className="pt-3 border-t border-[var(--border-color)] flex items-center justify-between">
                        <button
                          onClick={() => handleDownload(p.id)}
                          className="px-3.5 py-2 bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-xs rounded-lg transition-all shadow-md shadow-emerald-600/20 flex items-center space-x-1.5 cursor-pointer"
                        >
                          <Download className="w-4 h-4" />
                          <span>Download Certified Copy</span>
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </>
        )}
      </div>
    </DashboardLayout>
  );
}
