import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, GeoJSON, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import mapService from '../../services/mapService';
import StatusBadge from '../common/StatusBadge';
import { MapPin, Info } from 'lucide-react';

export default function MapViewer({ height = '500px', districtFilter = '', villageFilter = '' }) {
  const [geoJsonData, setGeoJsonData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedParcel, setSelectedParcel] = useState(null);

  useEffect(() => {
    fetchMapParcels();
  }, [districtFilter, villageFilter]);

  const fetchMapParcels = async () => {
    setLoading(true);
    try {
      const data = await mapService.getGeoJSONParcels({ district: districtFilter, village: villageFilter });
      setGeoJsonData(data);
    } catch (err) {
      console.error("Failed to load GeoJSON map data:", err);
    } finally {
      setLoading(false);
    }
  };

  const onEachFeature = (feature, layer) => {
    const props = feature.properties;
    layer.on({
      click: () => {
        setSelectedParcel(props);
      }
    });
  };

  const styleFeature = (feature) => {
    const status = feature.properties?.status;
    let color = '#3b82f6';
    if (status === 'VERIFIED') color = '#10b981';
    else if (status === 'REVIEW_REQUIRED') color = '#f43f5e';
    else if (status === 'DRAFT') color = '#f59e0b';

    return {
      fillColor: color,
      weight: 2,
      opacity: 0.9,
      color: color,
      fillOpacity: 0.35
    };
  };

  // Centered over Odisha region coordinates (20.27, 85.84)
  const centerPosition = [20.25, 85.75];

  return (
    <div className="relative rounded-2xl overflow-hidden border border-[var(--border-color)] bg-[var(--bg-card)] shadow-lg" style={{ height }}>
      {loading && (
        <div className="absolute inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center text-white">
          <div className="flex items-center space-x-3 bg-slate-900 px-5 py-3 rounded-xl border border-slate-700 shadow-2xl">
            <div className="w-5 h-5 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin" />
            <span className="text-sm font-semibold">Loading PostGIS Parcel Geometry...</span>
          </div>
        </div>
      )}

      <MapContainer
        center={centerPosition}
        zoom={12}
        scrollWheelZoom={true}
        style={{ height: '100%', width: '100%' }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {geoJsonData && (
          <GeoJSON
            data={geoJsonData}
            style={styleFeature}
            onEachFeature={onEachFeature}
          />
        )}
      </MapContainer>

      {/* Parcel Detail Modal Overlay upon click */}
      {selectedParcel && (
        <div className="absolute bottom-4 left-4 right-4 md:left-auto md:right-4 md:w-96 bg-[var(--bg-card)] border border-[var(--border-color)] rounded-xl p-4 shadow-2xl z-40 text-[var(--text-primary)] transition-all">
          <div className="flex items-center justify-between pb-3 border-b border-[var(--border-color)]">
            <div className="flex items-center space-x-2">
              <MapPin className="w-5 h-5 text-emerald-500" />
              <h4 className="font-bold text-base text-[var(--text-primary)]">{selectedParcel.parcel_uid}</h4>
            </div>
            <button
              onClick={() => setSelectedParcel(null)}
              className="text-xs text-[var(--text-muted)] hover:text-[var(--text-primary)] cursor-pointer"
            >
              Close
            </button>
          </div>

          <div className="grid grid-cols-2 gap-3 my-3 text-xs">
            <div>
              <span className="text-[var(--text-secondary)] font-medium">Survey Number:</span>
              <p className="font-bold text-sm text-[var(--text-primary)] mt-0.5">{selectedParcel.survey_number}</p>
            </div>
            <div>
              <span className="text-[var(--text-secondary)] font-medium">Khata Number:</span>
              <p className="font-bold text-sm text-[var(--text-primary)] mt-0.5">{selectedParcel.khata_number}</p>
            </div>
            <div>
              <span className="text-[var(--text-secondary)] font-medium">Village:</span>
              <p className="font-semibold text-[var(--text-primary)] mt-0.5">{selectedParcel.village}</p>
            </div>
            <div>
              <span className="text-[var(--text-secondary)] font-medium">Area:</span>
              <p className="font-semibold text-[var(--text-primary)] mt-0.5">{selectedParcel.area} {selectedParcel.area_unit}</p>
            </div>
          </div>

          <div className="pt-2 border-t border-[var(--border-color)] flex items-center justify-between">
            <span className="text-xs text-[var(--text-secondary)]">Status:</span>
            <StatusBadge status={selectedParcel.status} />
          </div>
        </div>
      )}
    </div>
  );
}
