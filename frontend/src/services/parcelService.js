import apiClient from './apiClient';

const parcelService = {
  getParcels: async (params = {}) => {
    return await apiClient.get('/parcels', { params });
  },
  searchParcels: async (params = {}) => {
    return await apiClient.get('/parcels/search', { params });
  },
  getParcelById: async (parcelId) => {
    return await apiClient.get(`/parcels/${parcelId}`);
  },
  getParcelOwners: async (parcelId) => {
    return await apiClient.get(`/parcels/${parcelId}/owners`);
  },
  getParcelHistory: async (parcelId) => {
    return await apiClient.get(`/parcels/${parcelId}/history`);
  }
};

export default parcelService;
