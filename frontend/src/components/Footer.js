import React from 'react';
import { Box, Typography } from '@mui/material';

const Footer = () => {
  return (
    <Box component="footer" sx={{ 
      textAlign: 'center',
      color: 'grey.600',
      fontSize: '0.9rem',
      mt: 4, 
      py: 2
    }}>
      <Typography variant="body2">
        GivingTuesday Campaign Advisor &copy; {new Date().getFullYear()}
      </Typography>
    </Box>
  );
};

export default Footer;