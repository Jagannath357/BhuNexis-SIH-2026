import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, GeoJSON, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import mapService from '../../services/mapService';
import StatusBadge from '../common/StatusBadge';
import { MapPin } from 'lucide-react';

// Helper component to auto-fit map view bounds to PostGIS GeoJSON parcels
function AutoFitBounds({ geoJsonData }) {
  const map = useMap();
  useEffect(() => {
    if (geoJsonData && geoJsonData.features && geoJsonData.features.length > 0) {
      try {
        const geoLayer = L.geoJSON(geoJsonData);
        const bounds = geoLayer.getBounds();
        if (bounds && bounds.isValid()) {
          map.fitBounds(bounds, { padding: [50, 50], maxZoom: 17 });
        }
      } catch (err) {
        console.error("Error auto-fitting Cadastral bounds:", err);
      }
    }
  }, [geoJsonData, map]);
  return null;
}

export default function MapViewer({ height = '550px', districtFilter = '', villageFilter = '' }) {
  const [geoJsonData, setGeoJsonData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedParcel, setSelectedParcel] = useState(null);
  const [basemap, setBasemap] = useState('osm'); // 'osm' | 'satellite' | 'dark'

  useEffect(() => {
    fetchMapParcels();
  }, [districtFilter, villageFilter]);

  const fetchMapParcels = async () => {
    setLoading(true);
    try {
      const data = await mapService.getGeoJSONParcels({ district: districtFilter, village: villageFilter });
      setGeoJsonData(data);
    } catch (err) {
      console.error("Failed to load Cadastral GeoJSON map data:", err);
    } finally {
      setLoading(false);
    }
  };

  const styleFeature = (feature) => {
    const status = feature.properties?.status;
    let color = '#3b82f6';
    let fillColor = '#3b82f6';
    
    if (status === 'VERIFIED') {
      color = '#10b981';
      fillColor = '#059669';
    } else if (status === 'REVIEW_REQUIRED') {
      color = '#ef4444';
      fillColor = '#dc2626';
    } else if (status === 'DRAFT') {
      color = '#f59e0b';
      fillColor = '#d97706';
    }

    return {
      fillColor: fillColor,
      weight: 2.5,
      opacity: 0.95,
      color: color,
      fillOpacity: 0.35,
      dashArray: status === 'DRAFT' ? '4, 4' : null
    };
  };

  const onEachFeature = (feature, layer) => {
    const props = feature.properties;
    const plotLabel = props.plot_number || props.survey_number || `Plot #${props.parcel_id}`;

    // Display permanent cadastral plot number label on map
    layer.bindTooltip(
      `<div class="font-bold text-[11px] px-2 py-0.5 rounded shadow-lg bg-slate-900/90 text-amber-300 border border-amber-500/50 backdrop-blur-sm whitespace-nowrap">
        ${plotLabel}
       </div>`,
      {
        permanent: true,
        direction: 'center',
        className: 'cadastral-tooltip-label'
      }
    );

    // Interactive Hover & Click
    layer.on({
      mouseover: (e) => {
        const l = e.target;
        l.setStyle({
          weight: 4,
          fillOpacity: 0.65,
          color: '#fbbf24'
        });
        if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
          l.bringToFront();
        }
      },
      mouseout: (e) => {
        const l = e.target;
        l.setStyle(styleFeature(feature));
      },
      click: () => {
        setSelectedParcel(props);
      }
    });
  };

  const basemapUrls = {
    osm: {
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      attribution: '&copy; OpenStreetMap contributors'
    },
    satellite: {
      url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
      attribution: 'Tiles &copy; Esri &mdash; Source: Esri, Maxar, Earthstar Geographics'
    },
    dark: {
      url: 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
      attribution: '&copy; OpenStreetMap contributors &copy; CARTO'
    }
  };

  const centerPosition = [20.205, 85.71]; // Odisha PostGIS fallback center

  return (
    <div className="relative rounded-2xl overflow-hidden border border-[var(--border-color)] bg-[var(--bg-card)] shadow-xl" style={{ height }}>
      {/* Loading Overlay */}
      {loading && (
        <div className="absolute inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center text-white">
          <div className="flex items-center space-x-3 bg-slate-900 px-5 py-3 rounded-xl border border-slate-700 shadow-2xl">
            <div className="w-5 h-5 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin" />
            <span className="text-sm font-semibold">Loading Live PostGIS Cadastral Parcels...</span>
          </div>
        </div>
      )}

      {/* Top Map Control Toolbar */}
      <div className="absolute top-3 left-3 right-3 z-30 flex items-center justify-between pointer-events-none">
        <div className="pointer-events-auto bg-slate-900/85 backdrop-blur-md px-3 py-1.5 rounded-xl border border-slate-700 text-xs font-semibold text-emerald-400 shadow-lg flex items-center space-x-2">
          <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
          <span>Cadastral GIS Map ({geoJsonData?.features?.length || 0} Parcels Loaded)</span>
        </div>

        {/* Layer Switcher Buttons */}
        <div className="pointer-events-auto bg-slate-900/85 backdrop-blur-md p-1 rounded-xl border border-slate-700 shadow-lg flex items-center space-x-1">
          <button
            onClick={() => setBasemap('osm')}
            className={`px-2.5 py-1 text-xs font-medium rounded-lg transition-all ${
              basemap === 'osm' ? 'bg-emerald-600 text-white shadow' : 'text-slate-300 hover:text-white'
            }`}
          >
            Standard
          </button>
          <button
            onClick={() => setBasemap('satellite')}
            className={`px-2.5 py-1 text-xs font-medium rounded-lg transition-all ${
              basemap === 'satellite' ? 'bg-emerald-600 text-white shadow' : 'text-slate-300 hover:text-white'
            }`}
          >
            Satellite
          </button>
          <button
            onClick={() => setBasemap('dark')}
            className={`px-2.5 py-1 text-xs font-medium rounded-lg transition-all ${
              basemap === 'dark' ? 'bg-emerald-600 text-white shadow' : 'text-slate-300 hover:text-white'
            }`}
          >
            Dark GIS
          </button>
        </div>
      </div>

      {/* Main Map Container */}
      <MapContainer
        center={centerPosition}
        zoom={14}
        scrollWheelZoom={true}
        style={{ height: '100%', width: '100%' }}
      >
        <TileLayer
          key={basemap}
          attribution={basemapUrls[basemap].attribution}
          url={basemapUrls[basemap].url}
        />

        {geoJsonData && (
          <>
            <GeoJSON
              key={JSON.stringify(geoJsonData)}
              data={geoJsonData}
              style={styleFeature}
              onEachFeature={onEachFeature}
            />
            <AutoFitBounds geoJsonData={geoJsonData} />
          </>
        )}
      </MapContainer>

      {/* Cadastral Legend Overlay */}
      <div className="absolute bottom-3 left-3 z-30 bg-slate-900/90 backdrop-blur-md p-3 rounded-xl border border-slate-700/80 text-xs shadow-xl max-w-xs pointer-events-auto">
        <div className="font-bold text-slate-200 mb-2 border-b border-slate-700/80 pb-1 flex items-center justify-between">
          <span>Cadastral Boundary Legend</span>
          <span className="text-[10px] text-amber-400 font-mono">Plot # Labels</span>
        </div>
        <div className="space-y-1.5">
          <div className="flex items-center space-x-2">
            <div className="w-4 h-3 rounded bg-emerald-500/40 border-2 border-emerald-500" />
            <span className="text-slate-300">Verified Land Parcel</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-4 h-3 rounded bg-amber-500/40 border-2 border-amber-500 border-dashed" />
            <span className="text-slate-300">Draft Parcel</span>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-4 h-3 rounded bg-rose-500/40 border-2 border-rose-500" />
            <span className="text-slate-300">Review Required</span>
          </div>
        </div>
      </div>

      {/* Parcel Detail Card Overlay */}
      {selectedParcel && (
        <div className="absolute bottom-3 right-3 z-40 w-80 md:w-96 bg-slate-900/95 backdrop-blur-md border border-slate-700 rounded-2xl p-4 shadow-2xl text-slate-100 transition-all animate-in fade-in slide-in-from-bottom-3">
          <div className="flex items-center justify-between pb-3 border-b border-slate-800">
            <div className="flex items-center space-x-2">
              <MapPin className="w-5 h-5 text-emerald-400 animate-bounce" />
              <div>
                <h4 className="font-bold text-sm text-white">{selectedParcel.parcel_uid}</h4>
                <p className="text-[11px] text-amber-400 font-medium">{selectedParcel.plot_number}</p>
              </div>
            </div>
            <button
              onClick={() => setSelectedParcel(null)}
              className="text-xs bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white px-2 py-1 rounded-lg transition-colors cursor-pointer"
            >
              Close
            </button>
          </div>

          <div className="grid grid-cols-2 gap-2.5 my-3 text-xs">
            <div className="bg-slate-800/60 p-2 rounded-lg border border-slate-700/50">
              <span className="text-slate-400 text-[10px] uppercase font-bold block">Plot / Survey No</span>
              <p className="font-bold text-slate-100 mt-0.5">{selectedParcel.plot_number} ({selectedParcel.survey_number})</p>
            </div>
            <div className="bg-slate-800/60 p-2 rounded-lg border border-slate-700/50">
              <span className="text-slate-400 text-[10px] uppercase font-bold block">Khasra / Khata</span>
              <p className="font-bold text-slate-100 mt-0.5">{selectedParcel.khasra_number} / {selectedParcel.khata_number}</p>
            </div>
            <div className="bg-slate-800/60 p-2 rounded-lg border border-slate-700/50">
              <span className="text-slate-400 text-[10px] uppercase font-bold block">Village & Tehsil</span>
              <p className="font-semibold text-slate-200 mt-0.5">{selectedParcel.village}, {selectedParcel.tehsil}</p>
            </div>
            <div className="bg-slate-800/60 p-2 rounded-lg border border-slate-700/50">
              <span className="text-slate-400 text-[10px] uppercase font-bold block">Recorded Area</span>
              <p className="font-semibold text-emerald-400 mt-0.5">{selectedParcel.area} {selectedParcel.area_unit}</p>
            </div>
            <div className="bg-slate-800/60 p-2 rounded-lg border border-slate-700/50">
              <span className="text-slate-400 text-[10px] uppercase font-bold block">Classification</span>
              <p className="font-medium text-slate-200 mt-0.5">{selectedParcel.land_classification}</p>
            </div>
            <div className="bg-slate-800/60 p-2 rounded-lg border border-slate-700/50">
              <span className="text-slate-400 text-[10px] uppercase font-bold block">Land Use</span>
              <p className="font-medium text-slate-200 mt-0.5">{selectedParcel.land_use}</p>
            </div>
          </div>

          <div className="pt-2 border-t border-slate-800 flex items-center justify-between">
            <span className="text-xs text-slate-400 font-medium">Verification Status:</span>
            <StatusBadge status={selectedParcel.status} />
          </div>
        </div>
      )}
    </div>
  );
}
