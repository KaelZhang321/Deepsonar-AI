import React from 'react';
import { Navbar } from './Navbar';
import { Hero } from './Hero';
import { Features } from './Features';
import { Process } from './Process';
import { Footer } from './Footer';

export const HomePage: React.FC = () => {
  return (
    <>
      <Navbar />
      <main>
        <Hero />
        <Features />
        <Process />
      </main>
      <Footer />
    </>
  );
};
