import { createTheme } from '@mui/material/styles';

// GivingTuesday colors from the original SCSS
const gtColors = {
  red: '#E43F23',
  blue: '#2E64AD',
  black: '#231F20',
  lightGray: '#F5F5F5',
  midGray: '#E5E5E5',
  darkGray: '#666666',
};

// Create a theme with the GivingTuesday palette
const theme = createTheme({
  palette: {
    primary: {
      main: gtColors.blue,
      contrastText: '#fff',
    },
    secondary: {
      main: gtColors.red,
      contrastText: '#fff',
    },
    text: {
      primary: gtColors.black,
      secondary: gtColors.darkGray,
    },
    background: {
      default: gtColors.lightGray,
      paper: '#fff',
    },
    grey: {
      100: gtColors.lightGray,
      200: gtColors.midGray,
      600: gtColors.darkGray,
    },
  },
  typography: {
    fontFamily: "'Open Sans', 'Roboto', 'Helvetica', 'Arial', sans-serif",
    h1: {
      fontFamily: "'Montserrat', 'Roboto', 'Helvetica', 'Arial', sans-serif",
      fontWeight: 700,
      letterSpacing: '-0.02em',
      fontSize: '2.2rem',
      color: gtColors.blue,
    },
    h2: {
      fontFamily: "'Montserrat', 'Roboto', 'Helvetica', 'Arial', sans-serif",
      fontWeight: 700,
      letterSpacing: '-0.02em',
      fontSize: '1.6rem',
    },
    h3: {
      fontFamily: "'Montserrat', 'Roboto', 'Helvetica', 'Arial', sans-serif",
      fontWeight: 700,
      letterSpacing: '-0.02em',
      fontSize: '1.3rem',
      color: gtColors.blue,
    },
    button: {
      fontFamily: "'Montserrat', 'Roboto', 'Helvetica', 'Arial', sans-serif",
      fontWeight: 600,
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 6,
          padding: '12px 24px',
          textTransform: 'none',
        },
        containedPrimary: {
          '&:hover': {
            backgroundColor: gtColors.red,
          },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            '&:hover fieldset': {
              borderColor: gtColors.blue,
            },
            '&.Mui-focused fieldset': {
              borderColor: gtColors.blue,
              boxShadow: `0 0 0 2px rgba(46, 100, 173, 0.2)`,
            },
          },
        },
      },
    },
    MuiCheckbox: {
      styleOverrides: {
        root: {
          color: gtColors.blue,
          '&.Mui-checked': {
            color: gtColors.blue,
          },
        },
      },
    },
  },
});

export default theme;