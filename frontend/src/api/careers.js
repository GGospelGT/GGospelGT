import apiClient from './client';

const careersAPI = {
  // Public APIs for career page
  getJobPostings: async (params = {}) => {
    const queryParams = new URLSearchParams();
    if (params.skip) queryParams.append('skip', params.skip);
    if (params.limit) queryParams.append('limit', params.limit);
    if (params.department) queryParams.append('department', params.department);
    if (params.job_type) queryParams.append('job_type', params.job_type);
    if (params.location) queryParams.append('location', params.location);
    if (params.featured_only) queryParams.append('featured_only', params.featured_only);
    
    const queryString = queryParams.toString();
    const response = await apiClient.get(`/public/content/jobs${queryString ? '?' + queryString : ''}`);
    return response.data;
  },

  getJobBySlug: async (slug) => {
    const response = await apiClient.get(`/public/content/jobs/${slug}`);
    return response.data;
  },

  getFeaturedJobs: async (limit = 3) => {
    const response = await apiClient.get(`/public/content/jobs/featured?limit=${limit}`);
    return response.data;
  },

  getJobDepartments: async () => {
    const response = await apiClient.get('/public/content/jobs/departments');
    return response.data;
  },

  applyToJob: async (jobId, applicationData) => {
    const response = await apiClient.post(`/public/content/jobs/${jobId}/apply`, applicationData);
    return response.data;
  },

  // Admin APIs for job management (requires admin authentication)
  admin: {
    getJobPostings: async (params = {}) => {
      const queryParams = new URLSearchParams();
      if (params.skip) queryParams.append('skip', params.skip);
      if (params.limit) queryParams.append('limit', params.limit);
      if (params.department) queryParams.append('department', params.department);
      if (params.status) queryParams.append('status', params.status);
      if (params.search) queryParams.append('search', params.search);
      
      const queryString = queryParams.toString();
      return await apiCall(`/api/admin/jobs/postings${queryString ? '?' + queryString : ''}`);
    },

    createJobPosting: async (jobData) => {
      return await apiCall('/api/admin/jobs/postings', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(jobData),
      });
    },

    getJobPosting: async (jobId) => {
      return await apiCall(`/api/admin/jobs/postings/${jobId}`);
    },

    updateJobPosting: async (jobId, updateData) => {
      return await apiCall(`/api/admin/jobs/postings/${jobId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(updateData),
      });
    },

    deleteJobPosting: async (jobId) => {
      return await apiCall(`/api/admin/jobs/postings/${jobId}`, {
        method: 'DELETE',
      });
    },

    publishJobPosting: async (jobId) => {
      return await apiCall(`/api/admin/jobs/postings/${jobId}/publish`, {
        method: 'POST',
      });
    },

    getJobApplications: async (params = {}) => {
      const queryParams = new URLSearchParams();
      if (params.skip) queryParams.append('skip', params.skip);
      if (params.limit) queryParams.append('limit', params.limit);
      if (params.job_id) queryParams.append('job_id', params.job_id);
      if (params.status) queryParams.append('status', params.status);
      
      const queryString = queryParams.toString();
      return await apiCall(`/api/admin/jobs/applications${queryString ? '?' + queryString : ''}`);
    },

    updateJobApplication: async (applicationId, updateData) => {
      return await apiCall(`/api/admin/jobs/applications/${applicationId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(updateData),
      });
    },

    getJobStatistics: async () => {
      return await apiCall('/api/admin/jobs/statistics');
    },
  }
};

export default careersAPI;