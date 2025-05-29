// src/components/Button.jsx
import styled from 'styled-components';

const Button = styled.button`
  background-color: ${({ primary }) => primary ? 'var(--primary)' : 'white'};
  color: ${({ primary }) => primary ? 'white' : 'var(--dark)'};
  border: ${({ outline }) => outline ? '1px solid var(--primary)' : 'none'};
  padding: ${({ size }) => 
    size === 'lg' ? '12px 24px' : 
    size === 'sm' ? '6px 12px' : '8px 16px'};
  border-radius: var(--border-radius);
  font-weight: 600;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  
  &:hover {
    background-color: ${({ primary }) => primary ? 'var(--secondary)' : '#f5f5f5'};
    transform: translateY(-2px);
    box-shadow: var(--box-shadow);
  }
  
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
`;

export default Button;