import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import DashboardLayout from '../../components/layout/DashboardLayout';
import citizenService from '../../services/citizenService';
import StatusBadge from '../../components/common/StatusBadge';
import { Search, MapPin, Download, FileText, CheckCircle } from 'lucide-react';

export default function CitizenSearch() {
  const [surveyNumber, setSurveyNumber] = useState('');
  const [khataNumber, setKhataNumber] = useState('');
  const [ownerName, setOwnerName] = useState('');
  const [village, setVillage] = useState('');

  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);
  const [downloadMsg, setDownloadMsg] = useState(null);

  const handleSearch = async (e) => {
    e.preventDefault();
    setLoading(true);
    setSearched(true);
    try {
      const data = await citizenService.searchVerifiedRecords({
        survey_number: surveyNumber,
        khata_number: khataNumber,
        owner_name: ownerName,
        village: village
      });
      setResults(data);
    } catch (err) {
      console.error("Search failed:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async (parcelId) => {
    try {
      const res = await citizenService.downloadCertifiedRecord(parcelId);
      setDownloadMsg(`Certified Copy Generated! ID: ${res.certificate_id}`);
      setTimeout(() => setDownloadMsg(null), 5000);
    } catch (err) {
      alert("Download failed: " + (err.message || "Error"));
    }
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div>
          <h1 className="text-2xl md:text-3xl font-extrabold text-[var(--text-primary)] tracking-tight">
            Search Public Verified Land Records
          </h1>
          <p className="text-sm text-[var(--text-secondary)] mt-1">
            Search officially certified land titles by Survey Number, Khata Number, Owner Name or Village
          </p>
        </div>

        {downloadMsg && (
          <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-600 dark:text-emerald-400 text-xs font-bold flex items-center space-x-2">
            <CheckCircle className="w-5 h-5 text-emerald-500" />
            <span>{downloadMsg}</span>
          </div>
        )}

        {/* Search Filter Form */}
        <form onSubmit={handleSearch} className="bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl p-6 shadow-sm space-y-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
            <div>
              <label className="block text-xs font-semibold uppercase text-[var(--text-secondary)] mb-1">Survey Number</label>
              <input
                type="text"
                placeholder="e.g. 101"
                value={surveyNumber}
                onChange={(e) => setSurveyNumber(e.target.value)}
                className="w-full px-3.5 py-2 rounded-xl border border-[var(--border-color)] bg-[var(--bg-main)] text-[var(--text-primary)] text-xs font-medium focus:ring-1 focus:ring-emerald-500"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold uppercase text-[var(--text-secondary)] mb-1">Khata Number</label>
              <input
                type="text"
                placeholder="e.g. 25"
                value={khataNumber}
                onChange={(e) => setKhataNumber(e.target.value)}
                className="w-full px-3.5 py-2 rounded-xl border border-[var(--border-color)] bg-[var(--bg-main)] text-[var(--text-primary)] text-xs font-medium focus:ring-1 focus:ring-emerald-500"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold uppercase text-[var(--text-secondary)] mb-1">Owner Name</label>
              <input
                type="text"
                placeholder="e.g. Anil Kumar"
                value={ownerName}
                onChange={(e) => setOwnerName(e.target.value)}
                className="w-full px-3.5 py-2 rounded-xl border border-[var(--border-color)] bg-[var(--bg-main)] text-[var(--text-primary)] text-xs font-medium focus:ring-1 focus:ring-emerald-500"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold uppercase text-[var(--text-secondary)] mb-1">Village</label>
              <input
                type="text"
                placeholder="e.g. Sample Village"
                value={village}
                onChange={(e) => setVillage(e.target.value)}
                className="w-full px-3.5 py-2 rounded-xl border border-[var(--border-color)] bg-[var(--bg-main)] text-[var(--text-primary)] text-xs font-medium focus:ring-1 focus:ring-emerald-500"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 px-4 bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs rounded-xl transition-all flex items-center justify-center space-x-2 cursor-pointer shadow-md shadow-emerald-600/20"
          >
            <Search className="w-4 h-4" />
            <span>{loading ? 'Searching Records...' : 'Execute Record Search'}</span>
          </button>
        </form>

        {/* Results List */}
        {searched && (
          <div className="bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl p-6 shadow-sm space-y-4">
            <h3 className="text-lg font-bold text-[var(--text-primary)]">Search Results ({results.length})</h3>
            {results.length === 0 ? (
              <p className="text-sm text-[var(--text-muted)] text-center py-6">No verified land records matched your search filters.</p>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {results.map((p) => (
                  <div key={p.id} className="p-4 rounded-xl border border-[var(--border-color)] bg-[var(--bg-main)] flex flex-col justify-between space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-sm text-emerald-600 dark:text-emerald-400">{p.parcel_uid}</span>
                      <StatusBadge status={p.status} />
                    </div>
                    <div className="grid grid-cols-2 gap-2 text-xs">
                      <div><span className="text-[var(--text-secondary)]">Survey No:</span> <strong className="text-[var(--text-primary)]">{p.survey_number}</strong></div>
                      <div><span className="text-[var(--text-secondary)]">Khata No:</span> <strong className="text-[var(--text-primary)]">{p.khata_number}</strong></div>
                      <div><span className="text-[var(--text-secondary)]">Village:</span> <span className="text-[var(--text-primary)] font-semibold">{p.village}</span></div>
                      <div><span className="text-[var(--text-secondary)]">Area:</span> <span className="text-[var(--text-primary)] font-semibold">{p.recorded_area} {p.recorded_area_unit}</span></div>
                    </div>
                    <div className="pt-2 border-t border-[var(--border-color)] flex items-center justify-between">
                      <button
                        onClick={() => handleDownload(p.id)}
                        className="px-3 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-xs rounded-lg transition-all flex items-center space-x-1 cursor-pointer"
                      >
                        <Download className="w-3.5 h-3.5" />
                        <span>Download Certified Copy</span>
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}
