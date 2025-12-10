import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { HomePage } from './components/HomePage';
import { ReportSample } from './components/ReportSample';
import { DataCapturePage } from './components/DataCapturePage';
import { AIProcessingPage } from './components/AIProcessingPage';
import { ReportGenerationPage } from './components/ReportGenerationPage';
import { PricingPage } from './components/PricingPage';
import { ApplyTrialPage } from './components/ApplyTrialPage';
import { AboutPage } from './components/AboutPage';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-black text-white selection:bg-brand-accent/30 selection:text-brand-accent font-sans">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/reports" element={<ReportSample />} />
          <Route path="/data-capture" element={<DataCapturePage />} />
          <Route path="/ai-processing" element={<AIProcessingPage />} />
          <Route path="/report-generation" element={<ReportGenerationPage />} />
          <Route path="/pricing" element={<PricingPage />} />
          <Route path="/apply" element={<ApplyTrialPage />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;