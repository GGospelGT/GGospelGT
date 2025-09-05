import React from 'react';
import { Card, CardContent } from './ui/card';
import { Star, MapPin } from 'lucide-react';

const ReviewsSection = () => {
  const reviews = [
    {
      name: 'Sarah Johnson',
      location: 'London',
      rating: 5,
      job: 'Kitchen renovation',
      review: 'Absolutely fantastic work! The tradesperson was professional, punctual, and delivered exactly what was promised. Highly recommend.',
      date: '2 days ago',
      avatar: 'SJ'
    },
    {
      name: 'Michael Brown',
      location: 'Manchester',
      rating: 5,
      job: 'Bathroom installation',
      review: 'Excellent service from start to finish. Great communication throughout the project and finished to a very high standard.',
      date: '1 week ago',
      avatar: 'MB'
    },
    {
      name: 'Emma Wilson',
      location: 'Birmingham',
      rating: 5,
      job: 'Garden landscaping',
      review: 'Transformed our garden completely! The attention to detail was amazing and the final result exceeded our expectations.',
      date: '2 weeks ago',
      avatar: 'EW'
    },
    {
      name: 'David Smith',
      location: 'Leeds',
      rating: 5,
      job: 'Roof repair',
      review: 'Quick response to our emergency roof leak. Professional work and fair pricing. Will definitely use again for future projects.',
      date: '3 weeks ago',
      avatar: 'DS'
    }
  ];

  const renderStars = (rating) => {
    return Array.from({ length: 5 }, (_, index) => (
      <Star
        key={index}
        size={16}
        className={index < rating ? 'text-yellow-400 fill-current' : 'text-gray-300'}
      />
    ));
  };

  return (
    <section className="py-16 bg-gray-50">
      <div className="container mx-auto px-4">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-12">
            <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
              Millions of genuine reviews
            </h2>
            <p className="text-xl text-gray-600">
              Reviews on MyBuilder are written by customers like you.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {reviews.map((review, index) => (
              <Card key={index} className="bg-white hover:shadow-lg transition-shadow duration-300">
                <CardContent className="p-6">
                  <div className="flex items-center mb-4">
                    <div className="w-10 h-10 bg-green-600 rounded-full flex items-center justify-center text-white font-semibold mr-3">
                      {review.avatar}
                    </div>
                    <div>
                      <h4 className="font-semibold text-gray-900">{review.name}</h4>
                      <div className="flex items-center text-sm text-gray-500">
                        <MapPin size={12} className="mr-1" />
                        {review.location}
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center mb-2">
                    <div className="flex mr-2">
                      {renderStars(review.rating)}
                    </div>
                    <span className="text-sm text-gray-500">{review.date}</span>
                  </div>

                  <p className="text-sm font-medium text-gray-700 mb-2">
                    {review.job}
                  </p>

                  <p className="text-sm text-gray-600 line-clamp-4">
                    "{review.review}"
                  </p>
                </CardContent>
              </Card>
            ))}
          </div>

          <div className="text-center mt-12">
            <p className="text-gray-600 mb-6">
              Join thousands of satisfied homeowners who found their perfect tradesperson on MyBuilder
            </p>
            <div className="flex flex-wrap justify-center gap-2 text-sm text-gray-500">
              <span className="bg-white px-3 py-1 rounded-full">⭐ 4.8/5 average rating</span>
              <span className="bg-white px-3 py-1 rounded-full">🔒 Verified reviews</span>
              <span className="bg-white px-3 py-1 rounded-full">✅ Quality guaranteed</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default ReviewsSection;