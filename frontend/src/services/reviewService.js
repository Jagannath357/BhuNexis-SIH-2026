import apiClient from './apiClient';

const reviewService = {
  getReviewQueue: async (params = {}) => {
    return await apiClient.get('/reviews', { params });
  },
  getReviewById: async (reviewId) => {
    return await apiClient.get(`/reviews/${reviewId}`);
  },
  saveCorrection: async (reviewId, correctionData) => {
    return await apiClient.patch(`/reviews/${reviewId}`, correctionData);
  },
  approveReview: async (reviewId, reviewerComment = '') => {
    return await apiClient.post(`/reviews/${reviewId}/approve`, { reviewer_comment: reviewerComment });
  },
  rejectReview: async (reviewId, reviewerComment = '') => {
    return await apiClient.post(`/reviews/${reviewId}/reject`, { reviewer_comment: reviewerComment });
  },
  verifyReview: async (reviewId, reviewerComment = '') => {
    return await apiClient.post(`/reviews/${reviewId}/verify`, { reviewer_comment: reviewerComment });
  }
};

export default reviewService;
