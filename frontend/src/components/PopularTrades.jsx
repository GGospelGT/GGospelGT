import React from 'react';
import { Button } from './ui/button';
import { Card, CardContent } from './ui/card';
import { ArrowRight } from 'lucide-react';

const PopularTrades = () => {
  const trades = [
    {
      title: 'Gardening & Landscaping',
      description: 'Dreaming of a garden that captivates and soothes? Our detailed guides will provide pricing info and help you find the perfect gardener.',
      tradespeople: '12,543',
      image: '🌿',
      color: 'from-green-400 to-green-600'
    },
    {
      title: 'Painting & Decorating',
      description: 'Thinking about giving your space a fresh, new look? Our guides will not only provide pricing info but also connect you with skilled painters.',
      tradespeople: '18,721',
      image: '🎨',
      color: 'from-blue-400 to-blue-600'
    },
    {
      title: 'Plastering & Rendering',
      description: 'Are you interested in price information about a job in this service category? To give you an idea of costs, here are some recent projects.',
      tradespeople: '8,934',
      image: '🏗️',
      color: 'from-orange-400 to-orange-600'
    },
    {
      title: 'Plumbing',
      description: 'From leaky taps to full bathroom installations, find qualified plumbers for any job. Get quotes and compare reviews.',
      tradespeople: '15,678',
      image: '🔧',
      color: 'from-indigo-400 to-indigo-600'
    },
    {
      title: 'Electrical Work',
      description: 'Safe, certified electrical work from qualified electricians. From socket installations to full rewiring projects.',
      tradespeople: '11,234',
      image: '⚡',
      color: 'from-yellow-400 to-yellow-600'
    },
    {
      title: 'Carpentry & Joinery',
      description: 'Custom woodwork, fitted wardrobes, kitchen installations and more from skilled carpenters and joiners.',
      tradespeople: '9,876',
      image: '🪚',
      color: 'from-amber-400 to-amber-600'
    }
  ];

  return (
    <section className="py-16 bg-white">
      <div className="container mx-auto px-4">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
              Popular trades
            </h2>
            <p className="text-xl text-gray-600">
              Browse our most popular trade categories and find the right specialist for your project.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {trades.map((trade, index) => (
              <Card key={index} className="group hover:shadow-lg transition-all duration-300 cursor-pointer">
                <CardContent className="p-6">
                  <div className={`w-16 h-16 rounded-lg bg-gradient-to-r ${trade.color} flex items-center justify-center mb-4 text-2xl`}>
                    {trade.image}
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-3 group-hover:text-green-600 transition-colors">
                    {trade.title}
                  </h3>
                  <p className="text-gray-600 mb-4 line-clamp-3">
                    {trade.description}
                  </p>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-500">
                      {trade.tradespeople} tradespeople in UK
                    </span>
                    <Button variant="ghost" size="sm" className="text-green-600 hover:text-green-700 p-0">
                      View all <ArrowRight size={16} className="ml-1" />
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          <div className="text-center mt-12">
            <Button variant="outline" className="border-green-600 text-green-600 hover:bg-green-50">
              View all trade categories
            </Button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default PopularTrades;