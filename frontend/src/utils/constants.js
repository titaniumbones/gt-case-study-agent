/**
 * Application constants used throughout the frontend
 */

// API endpoint base URL
export const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? '/api' 
  : 'http://localhost:8001/api';

// Example questions for the homepage
export const EXAMPLE_QUESTIONS = [
  {
    icon: "👥",
    text: "How can I mobilize volunteers for my GivingTuesday campaign?"
  },
  {
    icon: "📣",
    text: "What storytelling techniques work best for GivingTuesday?"
  },
  {
    icon: "📊",
    text: "How can I measure the success of my GivingTuesday campaign?"
  },
  {
    icon: "🏢",
    text: "What's the best way to engage local businesses in my campaign?"
  },
  {
    icon: "🌐",
    text: "How can I leverage social media for my GivingTuesday campaign?"
  },
  {
    icon: "💰",
    text: "What are effective fundraising strategies for small nonprofits?"
  }
];