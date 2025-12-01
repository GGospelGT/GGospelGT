import React, { useEffect, useState } from 'react';
import apiClient from '../../api/client';
import { walletAPI, adminAPI } from '../../api/wallet';

const PaymentProofImage = ({ filename, isAdmin = false, className = '', alt = 'Payment proof' }) => {
  const [src, setSrc] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    let isMounted = true;
    setSrc('');
    setError('');

    if (!filename) {
      setError('No file provided');
      return;
    }

    const url = isAdmin
      ? adminAPI.getPaymentProofBase64Url(filename)
      : walletAPI.getPaymentProofBase64Url(filename);

    apiClient
      .get(url)
      .then((resp) => {
        const b64 = resp?.data?.image_base64;
        if (!b64) {
          throw new Error('Base64 not returned');
        }
        if (isMounted) {
          setSrc(`data:image/jpeg;base64,${b64}`);
        }
      })
      .catch((e) => {
        if (isMounted) {
          setError('Failed to load image');
        }
        console.warn('PaymentProofImage error:', e?.response?.data || e?.message);
      });

    return () => { isMounted = false; };
  }, [filename, isAdmin]);

  if (error) {
    return (
      <div className={`flex items-center justify-center bg-gray-100 text-gray-500 border rounded ${className}`} style={{height: '5rem'}}>
        Payment proof unavailable
      </div>
    );
  }

  if (!src) {
    return (
      <div className={`animate-pulse bg-gray-100 border rounded ${className}`} style={{height: '5rem'}} />
    );
  }

  return (
    <img
      src={src}
      alt={alt}
      className={className}
      onClick={() => window.open(src, '_blank')}
    />
  );
};

export default PaymentProofImage;