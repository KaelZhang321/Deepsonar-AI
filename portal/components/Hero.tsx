import React from 'react';
import { ArrowRight, ChevronDown, Play, Sparkles } from 'lucide-react';
import { Link } from 'react-router-dom';
import { Reveal } from './ui/Reveal';


export const Hero: React.FC = () => {
  return (
    <section className="relative min-h-screen flex flex-col justify-center items-center overflow-hidden px-6 pt-20">
      
      {/* Dynamic Background */}
      <div className="absolute inset-0 z-0">
        <div className="hero-glow-bg animate-pulse-slow opacity-60"></div>
        <div className="absolute top-0 inset-x-0 h-px bg-gradient-to-r from-transparent via-white/10 to-transparent"></div>
        <div className="absolute bottom-0 w-full h-[300px] bg-gradient-to-t from-brand-dark to-transparent"></div>
        {/* Grid Pattern */}
        <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.02)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.02)_1px,transparent_1px)] bg-[size:60px_60px] [mask-image:radial-gradient(ellipse_at_center,black_50%,transparent_90%)]"></div>
      </div>

      <div className="relative z-10 max-w-6xl mx-auto text-center flex flex-col items-center">
        <Reveal>
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-brand-accent/20 bg-brand-accent/5 mb-8 backdrop-blur-md hover:border-brand-accent/40 transition-colors cursor-default">
            <Sparkles className="w-4 h-4 text-brand-accent animate-pulse" />
            <span className="text-sm font-semibold text-brand-accent tracking-wide uppercase">DeepSonar Intelligence V2.0</span>
          </div>
        </Reveal>

        <Reveal delay={0.1}>
          <h1 className="text-6xl md:text-8xl lg:text-9xl font-bold tracking-tighter mb-8 leading-[1.1] md:leading-[1.05]">
            <span className="bg-clip-text text-transparent bg-gradient-to-b from-white via-white to-slate-400">重构商业信息的</span>
            <span className="bg-clip-text text-transparent bg-gradient-to-r from-brand-accent via-brand-secondary to-pink-500 block mt-2 pb-4">
              获取与分析方式
            </span>
          </h1>
        </Reveal>

        <Reveal delay={0.2}>
          <p className="text-xl md:text-2xl text-slate-400 max-w-3xl mx-auto mb-12 font-light leading-relaxed">
            专为具有战略眼光的企业打造。利用下一代 AI 代理网络，<br className="hidden md:block"/>
            实现从<span className="text-slate-200 font-medium">全网情报捕获</span>到<span className="text-slate-200 font-medium">深度决策研报</span>的全流程自动化。
          </p>
        </Reveal>

        <Reveal delay={0.3}>
          <div className="flex flex-col sm:flex-row gap-5 items-center justify-center">
            <button className="group relative px-8 py-4 bg-white text-brand-dark rounded-full font-bold text-lg hover:shadow-[0_0_40px_-10px_rgba(99,102,241,0.5)] transition-all transform hover:-translate-y-1 active:scale-95 overflow-hidden">
              <span className="relative z-10 flex items-center gap-2">
                立即开始探索
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </span>
              <div className="absolute inset-0 bg-gradient-to-r from-brand-accent/20 to-brand-secondary/20 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            </button>

          </div>
        </Reveal>

        {/* Dashboard Preview / Floating UI */}
        <Reveal delay={0.5} width="100%">
          <div className="mt-20 relative w-full aspect-[16/9] max-w-5xl mx-auto rounded-xl border border-white/10 bg-brand-card/50 backdrop-blur-sm overflow-hidden shadow-2xl shadow-brand-accent/10 group">
             {/* Mockup UI Elements */}
             <div className="absolute inset-0 bg-gradient-to-b from-brand-accent/5 to-transparent opacity-50"></div>
             
             {/* Top Bar */}
             <div className="h-12 border-b border-white/5 flex items-center px-4 gap-2">
                <div className="flex gap-2">
                  <div className="w-3 h-3 rounded-full bg-red-500/50"></div>
                  <div className="w-3 h-3 rounded-full bg-yellow-500/50"></div>
                  <div className="w-3 h-3 rounded-full bg-green-500/50"></div>
                </div>
                <div className="flex-1 text-center text-xs text-slate-500 font-mono">dashboard.deepsonar.ai</div>
             </div>

             {/* Content Area Placeholder */}
             <div className="p-8 grid grid-cols-3 gap-6 h-full font-mono text-sm">
                <div className="col-span-1 border border-white/5 rounded-lg bg-white/5 p-4 animate-pulse-slow">
                   <div className="h-4 w-24 bg-brand-accent/20 rounded mb-4"></div>
                   <div className="h-2 w-full bg-white/5 rounded mb-2"></div>
                   <div className="h-2 w-3/4 bg-white/5 rounded"></div>
                </div>
                <div className="col-span-2 border border-white/5 rounded-lg bg-white/5 p-4 relative overflow-hidden">
                   <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent -translate-x-full group-hover:animate-[shimmer_2s_infinite]"></div>
                   <div className="flex justify-between mb-8">
                     <div className="h-4 w-32 bg-brand-secondary/20 rounded"></div>
                     <div className="h-4 w-12 bg-white/10 rounded"></div>
                   </div>
                   <div className="space-y-3">
                     <div className="h-24 w-full bg-gradient-to-br from-brand-accent/10 to-transparent rounded-lg border border-brand-accent/20"></div>
                     <div className="h-24 w-full bg-gradient-to-br from-brand-secondary/10 to-transparent rounded-lg border border-brand-secondary/20"></div>
                   </div>
                </div>
             </div>
          </div>
        </Reveal>
      </div>

      {/* Scroll Indicator */}
      <div className="absolute bottom-10 left-1/2 -translate-x-1/2 animate-bounce opacity-30 hover:opacity-100 transition-opacity cursor-pointer">
        <ChevronDown className="w-8 h-8 text-white" />
      </div>
    </section>
  );
};