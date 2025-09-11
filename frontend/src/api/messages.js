import apiClient from './client';

// Messages API
export const messagesAPI = {
  // Conversations
  createConversation: async (conversationData) => {
    const response = await apiClient.post('/messages/conversations', conversationData);
    return response.data;
  },

  getConversations: async (params = {}) => {
    const response = await apiClient.get('/messages/conversations', { params });
    return response.data;
  },

  getOrCreateConversationForJob: async (jobId, tradespersonId) => {
    const response = await apiClient.get(`/messages/conversations/job/${jobId}?tradesperson_id=${tradespersonId}`);
    return response.data;
  },

  // Messages
  getConversationMessages: async (conversationId, params = {}) => {
    const response = await apiClient.get(`/messages/conversations/${conversationId}/messages`, { params });
    return response.data;
  },

  sendMessage: async (conversationId, messageData) => {
    const response = await apiClient.post(`/messages/conversations/${conversationId}/messages`, messageData);
    return response.data;
  },

  markConversationAsRead: async (conversationId) => {
    const response = await apiClient.put(`/messages/conversations/${conversationId}/read`);
    return response.data;
  },
};

export default messagesAPI;