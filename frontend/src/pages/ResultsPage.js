import React, { useEffect } from 'react';
import { 
  Box, 
  Card, 
  CardContent, 
  Button, 
  CircularProgress,
  Typography
} from '@mui/material';
import { useLocation, useNavigate } from 'react-router-dom';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import AdviceContent from '../components/AdviceContent';

const ResultsPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  
  // Get data from location state or show loading
  const { query, advice, references, modelType } = location.state || {};
  
  // Log the received data for debugging
  useEffect(() => {
    console.log("Results page received state:", location.state);
    console.log("References received:", references);
  }, [location.state, references]);

  // Handle back button click
  const handleBack = () => {
    navigate('/');
  };

  if (!query || !advice) {
    return (
      <Card sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', py: 8, flexDirection: 'column' }}>
        <CircularProgress sx={{ mb: 2 }} />
        <Typography variant="body1" color="text.secondary">
          Loading advice...
        </Typography>
      </Card>
    );
  }

  return (
    <Card>
      <CardContent>
        <AdviceContent 
          query={query}
          advice={advice}
          references={references || []}
          modelType={modelType || 'detailed'}
        />
        
        <Box sx={{ mt: 4 }}>
          <Button
            variant="outlined"
            color="primary"
            startIcon={<ArrowBackIcon />}
            onClick={handleBack}
            sx={{
              borderRadius: '6px',
              transition: 'all 0.2s',
              fontWeight: 600,
              '&:hover': {
                backgroundColor: 'grey.100',
                transform: 'translateX(-3px)',
              }
            }}
          >
            Ask another question
          </Button>
        </Box>
      </CardContent>
    </Card>
  );
};

export default ResultsPage;