import axios from 'axios';

// Create axios instance with default config
const api = axios.create({
  baseURL: 'http://localhost:8001/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Campaign advisor API endpoints
export const campaignAdvisorApi = {
  // Ask a question to the advisor
  askQuestion: async (query, fastMode = false) => {
    try {
      const response = await api.post('/ask', {
        query,
        fast_mode: fastMode,
      });
      
      return response.data;
    } catch (error) {
      console.error('Error asking question:', error);
      throw error;
    }
  },
};

export default api;