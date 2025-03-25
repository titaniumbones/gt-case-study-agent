import React, { useState } from 'react';
import { 
  Box, 
  TextField, 
  Button, 
  FormControlLabel, 
  Checkbox, 
  Typography,
  CircularProgress
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const QueryForm = ({ initialQuery = '' }) => {
  const [query, setQuery] = useState(initialQuery);
  const [fastMode, setFastMode] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!query.trim()) {
      setError('Please enter a question');
      return;
    }
    
    setLoading(true);
    setError('');
    
    try {
      console.log("Sending request to API:", { query: query.trim(), fast_mode: fastMode });
      
      const response = await axios.post('http://localhost:8001/api/ask', { 
        query: query.trim(),
        fast_mode: fastMode
      });
      
      console.log("API Response:", response.data);
      
      // Convert references to the expected format if needed
      let processedReferences = [];
      
      if (response.data.references) {
        processedReferences = response.data.references.map(ref => {
          // Handle string references (old format)
          if (typeof ref === 'string') {
            return {
              title: ref,
              organization: 'Unknown',
              campaign_name: ref,
              content: '',
              id: `ref-${Math.random().toString(36).substr(2, 9)}`
            };
          }
          // Handle object references (new format)
          return {
            title: ref.title || '',
            organization: ref.organization || 'Unknown Organization',
            campaign_name: ref.campaign_name || 'Unknown Campaign',
            content: ref.content || '',
            id: ref.id || `ref-${Math.random().toString(36).substr(2, 9)}`
          };
        });
      }
      
      console.log("Processed references:", processedReferences);
      
      // Navigate to results page with the response data
      navigate('/results', { 
        state: { 
          query: query.trim(),
          advice: response.data.advice,
          references: processedReferences,
          modelType: fastMode ? 'cost-effective' : 'detailed'
        } 
      });
    } catch (err) {
      console.error('Error submitting query:', err);
      setError('Failed to get advice. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ width: '100%' }}>
      <Box sx={{ mb: 2.5 }}>
        <Typography variant="body1" component="label" htmlFor="query" sx={{ 
          display: 'block',
          mb: 1,
          fontWeight: 600,
        }}>
          What would you like to know about creating a GivingTuesday campaign?
        </Typography>
        <TextField
          id="query"
          name="query"
          multiline
          rows={4}
          fullWidth
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          error={!!error}
          helperText={error}
          sx={{
            '& .MuiOutlinedInput-root': {
              fontSize: '1rem',
            }
          }}
        />
      </Box>
      
      <FormControlLabel
        control={
          <Checkbox 
            checked={fastMode}
            onChange={(e) => setFastMode(e.target.checked)}
            name="fast_mode"
          />
        }
        label="Fast mode (quicker response with Claude 3.5 Haiku, but less detailed)"
        sx={{ mb: 2.5 }}
      />
      
      <Button 
        type="submit" 
        variant="contained" 
        color="primary"
        disabled={loading}
        sx={{ 
          py: 1.5,
          px: 3,
        }}
      >
        {loading ? (
          <CircularProgress size={24} color="inherit" sx={{ mr: 1 }} />
        ) : null}
        {loading ? 'Getting Advice...' : 'Get Advice'}
      </Button>
    </Box>
  );
};

export default QueryForm;