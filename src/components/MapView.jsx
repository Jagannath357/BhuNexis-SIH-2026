import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, GeoJSON, useMap } from 'react-leaflet';
import { DEMO_MAP_PARCELS } from '../data/mapParcels';
import { MapLegend } from './MapLegend';
import { StatusBadge } from './StatusBadge';
import { Search, MapPin, Layers, Info, CheckCircle2, ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';

// Component to handle map view updates when searching
function MapController({ selectedParcel }) {
  const map = useMap();

  useEffect(() => {
    if (selectedParcel && selectedParcel.geometry) {
      const coords = selectedParcel.geometry.coordinates[0];
      if (coords && coords.length > 0) {
        // Average coordinates for center
        const lats = coords.map(c => c[1]);
        const lngs = coords.map(c => c[0]);
        const centerLat = (Math.min(...lats) + Math.max(...lats)) / 2;
        const centerLng = (Math.min(...lngs) + Math.max(...lngs)) / 2;
        map.flyTo([centerLat, centerLng], 17, { duration: 1.2 });
      }
    }
  }, [selectedParcel, map]);

  return null;
}

export function MapView({ height = "h-[600px]", role = "CITIZEN", customGeoJson = null }) {
  const [parcelsGeoJson, setParcelsGeoJson] = useState(customGeoJson || DEMO_MAP_PARCELS);
  const [selectedParcel, setSelectedParcel] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [tileError, setTileError] = useState(false);

  useEffect(() => {
    if (customGeoJson) {
      setParcelsGeoJson(customGeoJson);
    }
  }, [customGeoJson]);

  // Odisha Demo Center: Jatni, Khordha (20.1824° N, 85.7356° E)
  const centerPosition = [20.1824, 85.7356];

  const getStyleForStatus = (status, isSelected) => {
    let fillColor = '#4F46E5'; // Extracted default
    let color = '#3730A3';

    if (status === 'VERIFIED') {
      fillColor = '#059669';
      color = '#047857';
    } else if (status === 'UNDER REVIEW' || status === 'PENDING' || status === 'LOW CONFIDENCE') {
      fillColor = '#D97706';
      color = '#B45309';
    } else if (status === 'CONFLICT') {
      fillColor = '#DC2626';
      color = '#991B1B';
    }

    return {
      fillColor,
      weight: isSelected ? 3 : 2,
      opacity: 1,
      color: isSelected ? '#38BDF8' : color,
      fillOpacity: isSelected ? 0.75 : 0.45
    };
  };

  const onEachParcel = (feature, layer) => {
    const props = feature.properties;
    
    layer.on({
      click: () => {
        setSelectedParcel(feature);
      },
      mouseover: (e) => {
        const l = e.target;
        l.setStyle({ fillOpacity: 0.8, weight: 3 });
      },
      mouseout: (e) => {
        const l = e.target;
        const isSel = selectedParcel?.id === feature.id;
        l.setStyle(getStyleForStatus(props.verificationStatus, isSel));
      }
    });

    layer.bindTooltip(`
      <div class="font-bold text-xs">${props.surveyNumber}</div>
      <div class="text-[10px]">${props.ownerName}</div>
      <div class="text-[10px] font-semibold">${props.verificationStatus}</div>
    `, { sticky: true, className: 'leaflet-custom-tooltip' });
  };

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;

    const q = searchQuery.toLowerCase().trim();
    const found = parcelsGeoJson.features.find(f => 
      f.properties.surveyNumber.toLowerCase().includes(q) ||
      f.properties.khataNumber.toLowerCase().includes(q) ||
      f.properties.ownerName.toLowerCase().includes(q)
    );

    if (found) {
      setSelectedParcel(found);
    }
  };

  return (
    <div className={`relative w-full ${height} rounded-2xl overflow-hidden border border-slate-200 shadow-sm flex flex-col`}>
      {/* Top Map Control Bar */}
      <div className="bg-slate-900 text-white p-3 flex flex-col sm:flex-row items-center justify-between gap-3 z-10">
        <div className="flex items-center gap-2">
          <Layers className="w-5 h-5 text-sky-400" />
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider">
              Khordha Cadastral GIS Explorer (Odisha)
            </h4>
            <p className="text-[10px] text-slate-400">
              Tehsil Jatni • BhuNexis Demo Mouza (GeoJSON Cadastral Boundary Layer)
            </p>
          </div>
        </div>

        {/* Map Search Bar */}
        <form onSubmit={handleSearchSubmit} className="relative w-full sm:w-72">
          <Search className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
          <input
            type="text"
            placeholder="Search Survey No (e.g. 125/3), Khata, Owner..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full bg-slate-800 border border-slate-700 rounded-lg pl-8 pr-3 py-1 text-xs text-white placeholder-slate-400 focus:outline-none focus:border-sky-500"
          />
        </form>
      </div>

      {/* Main Map Render Area */}
      <div className="flex-1 relative">
        <MapContainer
          center={centerPosition}
          zoom={15}
          scrollWheelZoom={true}
          style={{ width: '100%', height: '100%' }}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors • BhuNexis Demo'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            eventHandlers={{
              tileerror: () => setTileError(true)
            }}
          />

          <GeoJSON
            key={JSON.stringify(selectedParcel ? selectedParcel.id : 'all')}
            data={parcelsGeoJson}
            style={(feature) => getStyleForStatus(feature.properties.verificationStatus, selectedParcel?.id === feature.id)}
            onEachFeature={onEachParcel}
          />

          <MapController selectedParcel={selectedParcel} />
        </MapContainer>

        {/* Offline / Tile Load Warning Overlay */}
        {tileError && (
          <div className="absolute top-4 left-4 z-20 bg-amber-500/90 text-white text-xs font-semibold px-3 py-1.5 rounded-lg shadow-md flex items-center gap-2 backdrop-blur-sm">
            <Info className="w-4 h-4" />
            <span>Map Tile Offline Mode: Rendering GeoJSON Boundary Layer</span>
          </div>
        )}

        {/* Floating Legend */}
        <div className="absolute bottom-4 left-4 z-20 hidden md:block">
          <MapLegend />
        </div>

        {/* Selected Parcel Side Panel / Overlay */}
        {selectedParcel && (
          <div className="absolute top-4 right-4 z-20 w-80 bg-white/95 backdrop-blur-md rounded-2xl shadow-2xl border border-slate-200 p-5 text-slate-800 transition-all animate-fade-in">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <div>
                <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Selected Parcel</span>
                <h4 className="text-base font-extrabold text-slate-900 leading-tight">
                  Survey No. {selectedParcel.properties.surveyNumber}
                </h4>
              </div>
              <button
                onClick={() => setSelectedParcel(null)}
                className="text-xs text-slate-400 hover:text-slate-700 p-1 font-bold"
              >
                ✕
              </button>
            </div>

            <div className="mt-3 space-y-2 text-xs">
              <div className="flex justify-between py-1 border-b border-slate-100">
                <span className="text-slate-500">Khata Number:</span>
                <span className="font-bold text-slate-800">{selectedParcel.properties.khataNumber}</span>
              </div>
              <div className="flex justify-between py-1 border-b border-slate-100">
                <span className="text-slate-500">Landowner:</span>
                <span className="font-bold text-slate-900">{selectedParcel.properties.ownerName}</span>
              </div>
              <div className="flex justify-between py-1 border-b border-slate-100">
                <span className="text-slate-500">Plot Area:</span>
                <span className="font-semibold text-slate-800">{selectedParcel.properties.area}</span>
              </div>
              <div className="flex justify-between py-1 border-b border-slate-100">
                <span className="text-slate-500">Classification:</span>
                <span className="font-medium text-slate-700">{selectedParcel.properties.landClassification}</span>
              </div>
              <div className="flex justify-between py-1 border-b border-slate-100">
                <span className="text-slate-500">Mouza / Tehsil:</span>
                <span className="font-medium text-slate-700">{selectedParcel.properties.village}, {selectedParcel.properties.tehsil}</span>
              </div>
              <div className="flex justify-between items-center py-1">
                <span className="text-slate-500">Verification:</span>
                <StatusBadge status={selectedParcel.properties.verificationStatus} size="sm" />
              </div>
            </div>

            <div className="mt-4 pt-3 border-t border-slate-100">
              <Link
                to={`/u/records/${selectedParcel.properties.recordId}`}
                className="w-full py-2 bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs rounded-xl flex items-center justify-center gap-1.5 transition-colors shadow-sm"
              >
                <span>Inspect Record File</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
