import React, { useState, useEffect } from 'react';
import { Box, Typography, Paper, Chip, Grid, Card, CardContent, IconButton } from '@mui/material';
import { styled } from '@mui/material/styles';
import ReactMarkdown from 'react-markdown';
import OpenInNewIcon from '@mui/icons-material/OpenInNew';
import CaseStudyModal from './CaseStudyModal';

const AdviceContainer = styled(Paper)(({ theme }) => ({
  backgroundColor: 'white',
  padding: '20px',
  borderRadius: '8px',
  borderLeft: `5px solid ${theme.palette.secondary.main}`,
  boxShadow: '0 2px 8px rgba(0, 0, 0, 0.05)',
  lineHeight: 1.7,
  marginBottom: theme.spacing(3),
}));

const ModelInfoChip = styled(Chip)(({ theme }) => ({
  backgroundColor: '#f0f7ff',
  borderLeft: `3px solid ${theme.palette.primary.main}`,
  color: theme.palette.primary.main,
  fontSize: '0.9rem',
  height: 'auto',
  padding: '4px 0',
  marginBottom: theme.spacing(2),
  '& .MuiChip-label': {
    padding: '4px 12px',
  }
}));

const QueryContainer = styled(Box)(({ theme }) => ({
  backgroundColor: theme.palette.grey[100],
  borderRadius: '8px',
  padding: '15px',
  margin: '15px 0',
}));

const ReferencesContainer = styled(Box)(({ theme }) => ({
  marginTop: theme.spacing(3),
  padding: theme.spacing(2),
  backgroundColor: '#f0f7ff',
  borderRadius: '8px',
  borderLeft: `4px solid ${theme.palette.primary.main}`,
}));

const ReferenceCard = styled(Card)(({ theme }) => ({
  display: 'flex',
  alignItems: 'flex-start',
  backgroundColor: 'white',
  borderRadius: '8px',
  boxShadow: '0 2px 4px rgba(0,0,0,0.05)',
  marginBottom: theme.spacing(2),
  transition: 'all 0.2s ease',
  cursor: 'pointer',
  '&:hover': {
    boxShadow: '0 4px 8px rgba(0,0,0,0.1)',
    transform: 'translateY(-2px)',
  },
  '&:active': {
    transform: 'translateY(0)',
  }
}));

// Custom renderer for markdown components
const components = {
  h1: (props) => <Typography variant="h4" color="textPrimary" gutterBottom {...props} />,
  h2: (props) => <Typography variant="h5" color="textPrimary" gutterBottom {...props} />,
  h3: (props) => <Typography variant="h6" color="primary" gutterBottom {...props} />,
  p: (props) => <Typography variant="body1" paragraph {...props} />,
  ul: (props) => <Box component="ul" sx={{ pl: 2 }} {...props} />,
  ol: (props) => <Box component="ol" sx={{ pl: 2 }} {...props} />,
  li: (props) => <Typography component="li" variant="body1" sx={{ mb: 0.5 }} {...props} />,
};

// Hardcoded sample references for testing
const SAMPLE_REFERENCES = [
  {
    title: "Sample Organization - Test Campaign 1",
    organization: "Sample Organization",
    campaign_name: "Test Campaign 1",
    content: "# Sample Organization: Test Campaign 1\n\n## Description\nThis is a sample campaign for testing purposes.\n\n## Strategies\nUsed social media effectively.\n\n## Results\nRaised $10,000 for the cause.",
    id: "sample-1"
  },
  {
    title: "Test Nonprofit - Sample Campaign 2",
    organization: "Test Nonprofit",
    campaign_name: "Sample Campaign 2",
    content: "# Test Nonprofit: Sample Campaign 2\n\n## Description\nAnother sample to ensure the interface works.\n\n## Strategies\nEngaged volunteers effectively.\n\n## Results\nIncreased donor base by 20%.",
    id: "sample-2"
  }
];

const AdviceContent = ({ query, advice, references, modelType }) => {
  const [modalOpen, setModalOpen] = useState(false);
  const [selectedCaseStudy, setSelectedCaseStudy] = useState(null);
  const [displayReferences, setDisplayReferences] = useState([]);

  // Process references when the component mounts or references change
  useEffect(() => {
    console.log('Processing references in AdviceContent:', references);
    
    // First try to format the references if they exist
    let processedRefs = [];
    
    try {
      if (Array.isArray(references) && references.length > 0) {
        processedRefs = references.map(ref => {
          if (typeof ref === 'object' && ref !== null) {
            return {
              title: ref.title || 'Unknown Case Study',
              organization: ref.organization || 'Unknown Organization',
              campaign_name: ref.campaign_name || 'Unknown Campaign',
              content: ref.content || '',
              id: ref.id || `ref-${Math.random().toString(36).substr(2, 9)}`
            };
          }
          return {
            title: String(ref),
            organization: 'Unknown Organization',
            campaign_name: String(ref),
            content: '',
            id: `ref-${Math.random().toString(36).substr(2, 9)}`
          };
        });
      }
    } catch (error) {
      console.error('Error processing references:', error);
    }
    
    // If there are no valid references, use sample ones for testing
    if (processedRefs.length === 0) {
      console.log('Using sample references');
      processedRefs = SAMPLE_REFERENCES;
    }
    
    console.log('Final references to display:', processedRefs);
    setDisplayReferences(processedRefs);
  }, [references]);

  const handleOpenModal = (caseStudy) => {
    console.log('Opening modal with case study:', caseStudy);
    setSelectedCaseStudy(caseStudy);
    setModalOpen(true);
  };

  const handleCloseModal = () => {
    setModalOpen(false);
  };

  return (
    <Box>
      <Typography variant="h2" component="h2" gutterBottom>
        Your Campaign Advice
      </Typography>

      <QueryContainer>
        <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 1 }}>
          Your question:
        </Typography>
        <Typography variant="body1" color="primary.main" sx={{ fontSize: '1.1rem' }}>
          {query}
        </Typography>
      </QueryContainer>

      <ModelInfoChip 
        label={
          modelType === 'cost-effective' 
          ? "Using fast mode with Claude 3.5 Haiku" 
          : "Using detailed mode with Claude 3.7 Sonnet"
        }
      />

      <AdviceContainer>
        <ReactMarkdown components={components}>
          {advice}
        </ReactMarkdown>
      </AdviceContainer>

      {displayReferences.length > 0 && (
        <ReferencesContainer>
          <Typography variant="h3" component="h3" sx={{ mb: 2 }}>
            Case Studies Referenced
          </Typography>
          
          <Grid container spacing={2}>
            {displayReferences.map((ref, index) => (
              <Grid item xs={12} md={6} key={ref.id || `ref-${index}`}>
                <ReferenceCard onClick={() => handleOpenModal(ref)}>
                  <CardContent sx={{ 
                    display: 'flex', 
                    alignItems: 'flex-start',
                    width: '100%',
                    py: 1.5
                  }}>
                    <Box sx={{ 
                      color: 'primary.main', 
                      fontSize: '1.5rem', 
                      mr: 1.5,
                      mt: 0.5
                    }}>
                      📋
                    </Box>
                    <Box sx={{ flexGrow: 1 }}>
                      <Typography variant="subtitle1" sx={{ mb: 0.5, fontWeight: 500 }}>
                        {ref.campaign_name}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {ref.organization}
                      </Typography>
                    </Box>
                    <IconButton 
                      size="small" 
                      color="primary" 
                      aria-label="view case study"
                      sx={{ ml: 1 }}
                    >
                      <OpenInNewIcon fontSize="small" />
                    </IconButton>
                  </CardContent>
                </ReferenceCard>
              </Grid>
            ))}
          </Grid>
        </ReferencesContainer>
      )}

      <CaseStudyModal 
        open={modalOpen} 
        onClose={handleCloseModal}
        caseStudy={selectedCaseStudy}
      />
    </Box>
  );
};

export default AdviceContent;