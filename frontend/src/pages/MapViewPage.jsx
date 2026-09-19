import React, { useState } from 'react';
import DashboardLayout from '../components/layout/DashboardLayout';
import MapViewer from '../components/map/MapViewer';
import { MapPin, Filter } from 'lucide-react';

export default function MapViewPage() {
  const [district, setDistrict] = useState('');
  const [village, setVillage] = useState('');

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl md:text-3xl font-extrabold text-[var(--text-primary)] tracking-tight">
              GIS Cadastral Map Viewer
            </h1>
            <p className="text-sm text-[var(--text-secondary)] mt-1">
              Interactive PostGIS spatial geometry mapping with Survey and Khata plot overlays
            </p>
          </div>
        </div>

        {/* Filter controls */}
        <div className="bg-[var(--bg-card)] border border-[var(--border-color)] rounded-2xl p-4 flex flex-wrap items-center gap-4 shadow-sm">
          <div className="flex items-center space-x-2 text-xs font-bold text-[var(--text-secondary)] uppercase">
            <Filter className="w-4 h-4 text-emerald-500" />
            <span>Map Filters:</span>
          </div>
          <input
            type="text"
            placeholder="Filter by district (e.g. Khordha)..."
            value={district}
            onChange={(e) => setDistrict(e.target.value)}
            className="px-3.5 py-2 rounded-xl border border-[var(--border-color)] bg-[var(--bg-main)] text-[var(--text-primary)] text-xs w-60 focus:outline-none focus:ring-1 focus:ring-emerald-500"
          />
          <input
            type="text"
            placeholder="Filter by village..."
            value={village}
            onChange={(e) => setVillage(e.target.value)}
            className="px-3.5 py-2 rounded-xl border border-[var(--border-color)] bg-[var(--bg-main)] text-[var(--text-primary)] text-xs w-60 focus:outline-none focus:ring-1 focus:ring-emerald-500"
          />
        </div>

        {/* Map Container */}
        <MapViewer height="650px" districtFilter={district} villageFilter={village} />
      </div>
    </DashboardLayout>
  );
}
