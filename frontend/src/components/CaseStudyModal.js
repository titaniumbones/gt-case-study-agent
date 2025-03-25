import React from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  IconButton,
  Typography,
  Button,
  Box
} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import ReactMarkdown from 'react-markdown';

const styles = {
  dialogTitle: {
    m: 0,
    p: 2,
    bgcolor: 'primary.main',
    color: 'white',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  closeButton: {
    color: 'white',
  },
  content: {
    py: 2,
    px: 3,
  },
  sectionTitle: {
    color: 'primary.main',
    fontWeight: 600,
    fontSize: '1.1rem',
    mt: 2,
    mb: 1,
  },
  organization: {
    fontWeight: 500,
    fontSize: '0.95rem',
    mt: 1,
    color: 'text.secondary',
  },
};

// Helper function to safely format the case study content
const formatCaseStudyContent = (content) => {
  if (!content || typeof content !== 'string') {
    return "No detailed content available for this case study.";
  }
  
  try {
    // Split the content by sections based on markdown headings
    const sections = content.split(/(?=## )/);
    
    return sections.map((section, index) => (
      <Box key={`section-${index}`} sx={{ mb: index === 0 ? 2 : 3 }}>
        <ReactMarkdown>{section}</ReactMarkdown>
      </Box>
    ));
  } catch (error) {
    console.error("Error formatting case study content:", error);
    return "Error displaying case study content.";
  }
};

const CaseStudyModal = ({ open, onClose, caseStudy }) => {
  // Guard against null or invalid caseStudy
  if (!caseStudy) {
    return null;
  }

  // Extract properties with fallbacks
  const campaignName = caseStudy.campaign_name || "Unknown Campaign";
  const organization = caseStudy.organization || "Unknown Organization";
  const content = caseStudy.content || "";

  return (
    <Dialog 
      open={open} 
      onClose={onClose}
      maxWidth="md"
      fullWidth
      aria-labelledby="case-study-dialog-title"
    >
      <DialogTitle sx={styles.dialogTitle} id="case-study-dialog-title">
        <Typography variant="h6" component="div">
          {campaignName}
        </Typography>
        <IconButton 
          aria-label="close" 
          onClick={onClose}
          sx={styles.closeButton}
        >
          <CloseIcon />
        </IconButton>
      </DialogTitle>
      
      <DialogContent dividers sx={styles.content}>
        <Typography variant="subtitle1" sx={styles.organization}>
          {organization}
        </Typography>
        
        <Box sx={{ mt: 2 }}>
          {formatCaseStudyContent(content)}
        </Box>
      </DialogContent>
      
      <DialogActions>
        <Button onClick={onClose} color="primary">Close</Button>
      </DialogActions>
    </Dialog>
  );
};

export default CaseStudyModal;