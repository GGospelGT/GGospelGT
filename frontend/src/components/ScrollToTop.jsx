import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';

// Scroll to top on route changes. Helps when navigating from footer links
// so new content is visible without manual scrolling.
export default function ScrollToTop({ smooth = true }) {
  const location = useLocation();

  useEffect(() => {
    if (typeof window === 'undefined') return;
    try {
      const behavior = smooth ? 'smooth' : 'auto';
      window.scrollTo({ top: 0, left: 0, behavior });
    } catch {
      // Fallback for older browsers
      window.scrollTo(0, 0);
    }
  }, [location.pathname, location.search, location.hash]);

  return null;
}