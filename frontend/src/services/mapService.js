import apiClient from './apiClient';

const mapService = {
  getGeoJSONParcels: async (params = {}) => {
    return await apiClient.get('/map/parcels', { params });
  },
  getGeoJSONParcelById: async (parcelId) => {
    return await apiClient.get(`/map/parcels/${parcelId}`);
  }
};

export default mapService;
