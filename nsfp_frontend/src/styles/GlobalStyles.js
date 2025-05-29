// src/styles/GlobalStyles.js
import { createGlobalStyle } from 'styled-components';

const GlobalStyles = createGlobalStyle`
  :root {
    --primary: #1e88e5;
    --secondary: #1565c0;
    --accent: #ff9800;
    --light: #f5f5f5;
    --dark: #212121;
    --success: #4caf50;
    --error: #f44336;
    --warning: #ffc107;
    
    --spacing-xs: 4px;
    --spacing-sm: 8px;
    --spacing-md: 16px;
    --spacing-lg: 24px;
    --spacing-xl: 32px;
    
    --border-radius: 8px;
    --box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  }
  
  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }
  
  body {
    font-family: 'Inter', sans-serif;
    background-color: #f9f9f9;
    color: var(--dark);
    line-height: 1.6;
  }
  
  a {
    text-decoration: none;
    color: inherit;
  }
  
  button {
    cursor: pointer;
    font-family: inherit;
    border: none;
    background: none;
  }
  
  input, textarea, select {
    font-family: inherit;
    border: 1px solid #ddd;
    border-radius: var(--border-radius);
    padding: var(--spacing-sm);
  }
`;

export default GlobalStyles;