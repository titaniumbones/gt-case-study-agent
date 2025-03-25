import React from 'react';
import { Box, Typography, Grid, Paper } from '@mui/material';
import { styled } from '@mui/material/styles';

// Define styled components for the question cards
const QuestionCard = styled(Paper)(({ theme }) => ({
  backgroundColor: '#f0f7ff',
  borderRadius: '8px',
  padding: '15px',
  borderLeft: `3px solid ${theme.palette.primary.main}`,
  transition: 'transform 0.2s, box-shadow 0.2s, background-color 0.2s',
  cursor: 'pointer',
  position: 'relative',
  '&:hover': {
    transform: 'translateY(-3px)',
    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
    backgroundColor: '#e1eeff',
  },
  '&:active': {
    transform: 'translateY(-1px)',
    backgroundColor: '#d2e3ff',
  },
  '&::after': {
    content: '"⤴ Click to use"',
    position: 'absolute',
    bottom: '5px',
    right: '8px',
    fontSize: '0.7rem',
    color: theme.palette.primary.main,
    opacity: 0,
    transition: 'opacity 0.2s',
  },
  '&:hover::after': {
    opacity: 0.7,
  },
}));

const QuestionIcon = styled(Box)({
  fontSize: '1.8rem',
  marginBottom: '8px',
});

// Example questions data
const exampleQuestions = [
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

const ExampleQuestions = ({ onSelectQuestion }) => {
  return (
    <Box sx={{ mt: 4 }}>
      <Typography variant="h3" component="h3" sx={{ mb: 2 }}>
        Example Questions
      </Typography>
      
      <Grid container spacing={2}>
        {exampleQuestions.map((question, index) => (
          <Grid item xs={12} sm={6} md={4} key={index}>
            <QuestionCard onClick={() => onSelectQuestion(question.text)}>
              <QuestionIcon>{question.icon}</QuestionIcon>
              <Typography 
                variant="body2" 
                sx={{ 
                  m: 0, 
                  fontSize: '0.95rem', 
                  color: 'primary.main'
                }}
              >
                {question.text}
              </Typography>
            </QuestionCard>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default ExampleQuestions;