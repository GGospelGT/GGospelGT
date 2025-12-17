import React, { useEffect, useState } from 'react';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { Link } from 'react-router-dom';
import { policiesAPI } from '../api/wallet';

const SectionBar = ({ children }) => (
  <div className="rounded-md bg-green-600 text-white px-4 py-2 font-semibold mb-3">{children}</div>
);

const SubSectionBar = ({ children, id }) => (
  <div id={id} className="rounded-md bg-green-100 text-green-900 px-4 py-2 font-semibold mb-3">{children}</div>
);

const PrivacyPage = () => {
  const [policy, setPolicy] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    let isMounted = true;
    (async () => {
      try {
        const res = await policiesAPI.getPolicyByType('privacy_policy');
        const data = res?.policy || res;
        if (isMounted) {
          setPolicy(data || null);
        }
      } catch (e) {
        if (isMounted) {
          setError(e?.response?.data?.detail || 'Unable to load policy content');
        }
      } finally {
        if (isMounted) setLoading(false);
      }
    })();
    return () => { isMounted = false; };
  }, []);

  const effective = policy?.effective_date ? new Date(policy.effective_date) : null;
  const updated = policy?.updated_at ? new Date(policy.updated_at) : null;

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <div className="container mx-auto px-4 py-10">
        <div className="max-w-6xl mx-auto bg-white rounded-xl shadow-sm border p-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">{policy?.title || 'Privacy Policy'}</h1>
          <div className="text-sm text-gray-600 mb-6">
            {effective && <span className="mr-4">Effective: {effective.toLocaleDateString()}</span>}
            {updated && <span>Last updated: {updated.toLocaleDateString()}</span>}
          </div>
          {loading ? (
            <div className="text-gray-700">Loading policy…</div>
          ) : error ? (
            <div className="text-red-600">
              {error}. Please see our{' '}
              <Link to="/cookie-policy" className="text-green-600 hover:text-green-700 underline">Cookie Policy</Link>
              {' '}and{' '}
              <Link to="/contact" className="text-green-600 hover:text-green-700 underline">Contact page</Link>.
            </div>
          ) : (
            <div className="text-gray-700 whitespace-pre-wrap">{policy?.content}</div>
          )}
        </div>
      </div>
      <Footer />
    </div>
  );
};

export default PrivacyPage;