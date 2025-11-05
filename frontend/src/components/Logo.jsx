import React from 'react';
import logoLight from '../assets/logo-light.svg';
import logoDark from '../assets/logo-dark.svg';

const Logo = ({ size = 'medium', variant = 'light', className = '' }) => {
  const sizes = {
    small: { container: 'px-2 py-1', image: 'h-6' },
    medium: { container: 'px-3 py-2', image: 'h-8' },
    large: { container: 'px-4 py-3', image: 'h-10' }
  };

  const currentSize = sizes[size] || sizes.medium;
  const src = variant === 'dark' ? logoDark : logoLight;

  return (
    <div
      className={`flex items-center rounded-lg ${currentSize.container} ${className}`}
      style={{ backgroundColor: variant === 'dark' ? '#121E3C' : 'transparent' }}
    >
      <img
        src={src}
        alt="ServiceHub logo"
        className={`${currentSize.image}`}
      />
    </div>
  );
};

export default Logo;