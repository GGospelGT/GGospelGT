import apiClient from './client';

// Statistics API
export const statsAPI = {
  getStats: async () => {
    const response = await apiClient.get('/stats');
    return response.data;
  },

  getCategories: async () => {
    const response = await apiClient.get('/stats/categories');
    return response.data;
  },
};

// Jobs API
export const jobsAPI = {
  createJob: async (jobData) => {
    const response = await apiClient.post('/jobs', jobData);
    return response.data;
  },

  getJobs: async (params = {}) => {
    const response = await apiClient.get('/jobs', { params });
    return response.data;
  },

  getJob: async (jobId) => {
    const response = await apiClient.get(`/jobs/${jobId}`);
    return response.data;
  },

  searchJobs: async (params = {}) => {
    const response = await apiClient.get('/jobs/search', { params });
    return response.data;
  },
};

// Tradespeople API
export const tradespeopleAPI = {
  createTradesperson: async (tradespersonData) => {
    const response = await apiClient.post('/tradespeople', tradespersonData);
    return response.data;
  },

  getTradespeople: async (params = {}) => {
    const response = await apiClient.get('/tradespeople', { params });
    return response.data;
  },

  getTradesperson: async (tradespersonId) => {
    const response = await apiClient.get(`/tradespeople/${tradespersonId}`);
    return response.data;
  },

  getTradespersonReviews: async (tradespersonId, params = {}) => {
    const response = await apiClient.get(`/tradespeople/${tradespersonId}/reviews`, { params });
    return response.data;
  },
};

// Quotes API
export const quotesAPI = {
  createQuote: async (quoteData) => {
    const response = await apiClient.post('/quotes', quoteData);
    return response.data;
  },

  getJobQuotes: async (jobId) => {
    const response = await apiClient.get(`/quotes/job/${jobId}`);
    return response.data;
  },
};

// Reviews API
export const reviewsAPI = {
  createReview: async (reviewData) => {
    const response = await apiClient.post('/reviews', reviewData);
    return response.data;
  },

  getReviews: async (params = {}) => {
    const response = await apiClient.get('/reviews', { params });
    return response.data;
  },

  getFeaturedReviews: async (limit = 4) => {
    const response = await apiClient.get(`/reviews/featured?limit=${limit}`);
    return response.data;
  },
};