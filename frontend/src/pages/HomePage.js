import React, { useState } from 'react';
import { Box, Card, CardContent, Typography } from '@mui/material';
import Banner from '../components/Banner';
import QueryForm from '../components/QueryForm';
import ExampleQuestions from '../components/ExampleQuestions';

const HomePage = () => {
  const [query, setQuery] = useState('');

  const handleSelectQuestion = (questionText) => {
    setQuery(questionText);
    
    // Scroll to form (optional)
    const formElement = document.querySelector('form');
    if (formElement) {
      formElement.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <Card>
      <Banner 
        title="Get Expert Advice for Your GivingTuesday Campaign" 
        subtitle="Powered by AI analysis of successful campaigns worldwide"
      />
      <CardContent>
        <Typography variant="body1" paragraph>
          Our AI-powered advisor analyzes real GivingTuesday case studies to provide you with specific, 
          actionable advice for planning and executing your campaign.
        </Typography>
        
        <Box 
          component="div" 
          id="query-form-container"
          sx={{ width: '100%' }}
        >
          <QueryForm initialQuery={query} />
        </Box>
        
        <ExampleQuestions onSelectQuestion={handleSelectQuestion} />
      </CardContent>
    </Card>
  );
};

export default HomePage;