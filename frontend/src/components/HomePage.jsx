import React from 'react';
import Header from './Header';
import HeroSection from './HeroSection';
import StatsSection from './StatsSection';
import HowItWorks from './HowItWorks';
import PopularTrades from './PopularTrades';
import ReviewsSection from './ReviewsSection';
import TradespeopleCTA from './TradespeopleCTA';
import AppSection from './AppSection';
import Footer from './Footer';

const HomePage = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <HeroSection />
      <StatsSection />
      <div style={{backgroundColor: 'red', padding: '20px', margin: '20px'}}>
        <h2>DEBUG: Before HowItWorks</h2>
      </div>
      <HowItWorks />
      <div style={{backgroundColor: 'blue', padding: '20px', margin: '20px', color: 'white'}}>
        <h2>DEBUG: Before PopularTrades</h2>
      </div>
      <PopularTrades />
      <div style={{backgroundColor: 'green', padding: '20px', margin: '20px', color: 'white'}}>
        <h2>DEBUG: Before ReviewsSection</h2>
      </div>
      <ReviewsSection />
      <div style={{backgroundColor: 'orange', padding: '20px', margin: '20px'}}>
        <h2>DEBUG: Before TradespeopleCTA</h2>
      </div>
      <TradespeopleCTA />
      <div style={{backgroundColor: 'purple', padding: '20px', margin: '20px', color: 'white'}}>
        <h2>DEBUG: After TradespeopleCTA, Before AppSection</h2>
      </div>
      <AppSection />
      <Footer />
    </div>
  );
};

export default HomePage;