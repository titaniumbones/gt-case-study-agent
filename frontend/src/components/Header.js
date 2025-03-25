import React from 'react';
import { Box, Typography } from '@mui/material';
import { styled } from '@mui/material/styles';

const Logo = styled('div')(({ theme }) => ({
  marginBottom: '0.5rem',
  display: 'flex',
  justifyContent: 'center',
}));

const LogoImage = styled('img')({
  height: '60px',
  width: 'auto',
});

const Header = () => {
  return (
    <Box component="header" sx={{ 
      display: 'flex', 
      flexDirection: 'column', 
      alignItems: 'center',
      mb: 3
    }}>
      <Logo>
        <LogoImage 
          src="https://www.givingtuesday.org/wp-content/uploads/2021/02/red-heart.png"
          alt="GivingTuesday Heart Logo" 
        />
      </Logo>
      <Typography variant="h1" component="h1" sx={{ 
        textAlign: 'center',
        my: 1,
      }}>
        GivingTuesday Campaign Advisor
      </Typography>
    </Box>
  );
};

export default Header;