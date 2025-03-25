import React from 'react';
import { Box, Typography } from '@mui/material';
import { styled } from '@mui/material/styles';

const BannerRoot = styled(Box)(({ theme }) => ({
  margin: '-25px -25px 20px -25px',
  background: `linear-gradient(120deg, ${theme.palette.primary.main}, ${theme.palette.text.primary})`,
  borderRadius: '12px 12px 0 0',
  padding: '25px',
  color: 'white',
  textAlign: 'center',
}));

const BannerInner = styled(Box)({
  maxWidth: '600px',
  margin: '0 auto',
});

const Banner = ({ title, subtitle }) => {
  return (
    <BannerRoot>
      <BannerInner>
        <Typography 
          variant="h2" 
          component="h2" 
          sx={{ 
            color: 'white',
            margin: '0 0 8px 0',
            fontSize: '1.8rem',
          }}
        >
          {title}
        </Typography>
        <Typography 
          variant="body1" 
          sx={{ 
            margin: 0,
            opacity: 0.9,
            fontSize: '1.1rem',
          }}
        >
          {subtitle}
        </Typography>
      </BannerInner>
    </BannerRoot>
  );
};

export default Banner;