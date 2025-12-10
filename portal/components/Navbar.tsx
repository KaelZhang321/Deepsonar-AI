import React, { useState, useEffect } from 'react';
import { Radar, Menu, X, ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';

export const Navbar: React.FC = () => {
  const [scrolled, setScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const navLinks = [
    { name: '产品特性', href: '#features' },
    { name: '工作原理', href: '#process' },
    { name: '解决方案', href: '#solutions' },
    { name: '报告样本', href: '/reports', isRoute: true },
    { name: '价格', href: '/pricing', isRoute: true },
    { name: '关于我们', href: '/about', isRoute: true },
  ];

  return (
    <nav 
      className={`fixed top-0 w-full z-50 transition-all duration-300 border-b ${
        scrolled 
          ? 'bg-brand-dark/80 backdrop-blur-md border-white/5 py-4' 
          : 'bg-transparent border-transparent py-6'
      }`}
    >
      <div className="max-w-7xl mx-auto px-6 h-full flex justify-between items-center">
        {/* Logo */}
        <div className="flex items-center gap-3 group cursor-pointer">
          <div className="relative flex items-center justify-center">
            <div className="absolute inset-0 bg-brand-accent/20 rounded-full blur-md group-hover:bg-brand-accent/40 transition-all duration-500" />
            <div className="relative p-2 rounded-xl bg-brand-card border border-white/10 group-hover:border-brand-accent/30 transition-all duration-500">
              <Radar className="w-6 h-6 text-brand-accent group-hover:rotate-12 transition-transform duration-500" />
            </div>
          </div>
          <span className="text-xl font-bold tracking-tight text-white group-hover:text-transparent group-hover:bg-clip-text group-hover:bg-gradient-to-r group-hover:from-brand-accent group-hover:to-brand-secondary transition-all duration-300">
            DeepSonar
          </span>
        </div>

        {/* Desktop Links */}
        <div className="hidden md:flex items-center gap-1">
          {navLinks.map((link) => (
            link.isRoute ? (
              <Link
                key={link.name}
                to={link.href}
                className="px-4 py-2 text-sm font-medium text-slate-400 hover:text-white transition-colors hover:bg-white/5 rounded-full"
              >
                {link.name}
              </Link>
            ) : (
              <a 
                key={link.name} 
                href={link.href} 
                className="px-4 py-2 text-sm font-medium text-slate-400 hover:text-white transition-colors hover:bg-white/5 rounded-full"
              >
                {link.name}
              </a>
            )
          ))}
        </div>

        {/* CTA Buttons */}
        <div className="hidden md:flex items-center gap-3">
          <a 
            href="http://www.deepsonar.com.cn/login/" 
            className="px-4 py-2.5 rounded-full border border-white/20 text-white text-sm font-medium hover:bg-white/10 hover:border-white/40 transition-all"
          >
            登录
          </a>
          <Link to="/apply" className="group relative px-5 py-2.5 rounded-full bg-white text-brand-dark text-sm font-bold overflow-hidden transition-transform hover:scale-105 active:scale-95">
            <span className="relative z-10 flex items-center gap-2">
              申请试用 <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </span>
            <div className="absolute inset-0 bg-gradient-to-r from-brand-accent to-brand-secondary opacity-0 group-hover:opacity-10 transition-opacity duration-300" />
          </Link>
        </div>

        {/* Mobile Toggle */}
        <button 
          className="md:hidden p-2 text-slate-300 hover:text-white hover:bg-white/10 rounded-lg transition-colors"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
        >
          {mobileMenuOpen ? <X /> : <Menu />}
        </button>
      </div>

      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <div className="absolute top-full left-0 w-full h-[calc(100vh-80px)] bg-brand-dark/95 backdrop-blur-xl border-t border-white/10 p-6 flex flex-col gap-6 md:hidden animate-in slide-in-from-top-4 duration-300">
          <div className="flex flex-col gap-2">
            {navLinks.map((link) => (
              link.isRoute ? (
                <Link
                  key={link.name}
                  to={link.href}
                  className="text-lg font-medium text-slate-400 hover:text-white py-3 px-4 rounded-xl hover:bg-white/5 transition-all"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  {link.name}
                </Link>
              ) : (
                <a 
                  key={link.name} 
                  href={link.href}
                  className="text-lg font-medium text-slate-400 hover:text-white py-3 px-4 rounded-xl hover:bg-white/5 transition-all"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  {link.name}
                </a>
              )
            ))}
          </div>
          <div className="mt-auto border-t border-white/10 pt-6 flex flex-col gap-4">
            <a href="http://www.deepsonar.com.cn/login/" className="w-full py-3 text-slate-300 hover:text-white font-medium text-center block">
              登录账户
            </a>
            <Link 
              to="/apply"
              className="w-full py-3.5 rounded-xl bg-white text-brand-dark font-bold hover:bg-brand-accent hover:text-white transition-colors flex items-center justify-center gap-2"
              onClick={() => setMobileMenuOpen(false)}
            >
              立即开始 <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        </div>
      )}
    </nav>
  );
};