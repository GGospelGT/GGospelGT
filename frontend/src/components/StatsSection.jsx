import React from 'react';
import { Users, Star, Wrench } from 'lucide-react';
import { statsAPI } from '../api/services';
import { useAPI } from '../hooks/useAPI';

const StatsSection = () => {
  const { data: stats, loading, error } = useAPI(() => statsAPI.getStats());

  // Fallback data while loading or on error
  const defaultStats = [
    {
      icon: Users,
      number: '251,959',
      label: 'registered tradespeople',
      color: 'text-green-600'
    },
    {
      icon: Wrench,
      number: '40+',
      label: 'trade categories',
      color: 'text-orange-500'
    },
    {
      icon: Star,
      number: '2,630,834',
      label: 'customer reviews',
      color: 'text-yellow-500'
    }
  ];

  // Use real stats if available, otherwise use defaults
  const displayStats = stats ? [
    {
      icon: Users,
      number: stats.total_tradespeople.toLocaleString(),
      label: 'registered tradespeople',
      color: 'text-green-600'
    },
    {
      icon: Wrench,
      number: `${stats.total_categories}+`,
      label: 'trade categories',
      color: 'text-orange-500'
    },
    {
      icon: Star,
      number: stats.total_reviews.toLocaleString(),
      label: 'customer reviews',
      color: 'text-yellow-500'
    }
  ] : defaultStats;

  if (error) {
    console.warn('Failed to load stats, using defaults:', error);
  }

  return (
    <section className="py-12 bg-white">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto">
          {displayStats.map((stat, index) => {
            const IconComponent = stat.icon;
            return (
              <div key={index} className="text-center">
                <div className={`inline-flex items-center justify-center w-16 h-16 rounded-full bg-gray-100 mb-4 ${stat.color}`}>
                  <IconComponent size={32} />
                </div>
                <div className={`text-3xl font-bold text-gray-900 mb-2 ${loading ? 'animate-pulse bg-gray-200 rounded' : ''}`}>
                  {loading ? '...' : stat.number}
                </div>
                <div className="text-gray-600">
                  {stat.label}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};

export default StatsSection;