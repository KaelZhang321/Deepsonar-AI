import React from 'react';
import { Reveal } from './ui/Reveal';
import { Search, BrainCircuit, Send, ArrowRight } from 'lucide-react';

export const Process: React.FC = () => {
  const steps = [
    {
      icon: <Search className="w-6 h-6 text-white" />,
      title: "定义命题",
      desc: "设定您关注的商业命题、竞争对手或市场领域。",
      color: "from-brand-accent to-brand-secondary"
    },
    {
      icon: <BrainCircuit className="w-6 h-6 text-white" />,
      title: "智能推演",
      desc: "DeepSonar Agent 自动拆解任务，全网搜集线索并验证逻辑。",
      color: "from-blue-500 to-cyan-500"
    },
    {
      icon: <Send className="w-6 h-6 text-white" />,
      title: "交付洞察",
      desc: "定期接收精炼的决策日报，直接辅助战略制定。",
      color: "from-emerald-500 to-teal-500"
    }
  ];

  return (
    <section id="process" className="py-32 px-6 relative">
      <div className="max-w-7xl mx-auto">
        <Reveal className="mx-auto text-center mb-16">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-white/10 bg-white/5 mb-6">
            <span className="text-xs font-medium text-slate-300 tracking-wide uppercase">Workflow</span>
          </div>
          <h2 className="text-4xl md:text-5xl font-bold mb-6 tracking-tight">简单三步，<span className="gradient-accent">洞悉未来</span></h2>
          <p className="text-slate-400 text-lg">全自动化的情报流水线，每一步都由 AI 精把控</p>
        </Reveal>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 relative">
           {/* Connecting Line (Desktop) */}
           <div className="hidden md:block absolute top-[60px] left-[15%] right-[15%] h-[2px] bg-gradient-to-r from-brand-accent/20 via-brand-secondary/20 to-emerald-500/20"></div>

           {steps.map((step, idx) => (
             <Reveal key={idx} delay={idx * 0.2} className="relative group">
               <div className="relative flex flex-col items-center text-center p-6 rounded-3xl hover:bg-white/5 transition-colors duration-300">
                 
                 <div className={`w-28 h-28 rounded-[2rem] bg-gradient-to-br ${step.color} p-[1px] mb-8 relative z-10 shadow-[0_0_50px_-10px_rgba(56,189,248,0.3)] group-hover:scale-105 transition-transform duration-500`}>
                    <div className="w-full h-full bg-brand-dark rounded-[2rem] flex items-center justify-center relative overflow-hidden">
                      <div className={`absolute inset-0 bg-gradient-to-br ${step.color} opacity-10 group-hover:opacity-20 transition-opacity`}></div>
                      {step.icon}
                    </div>
                 </div>
                 
                 <h3 className="text-2xl font-bold text-white mb-3">{step.title}</h3>
                 <p className="text-slate-400 leading-relaxed max-w-xs">{step.desc}</p>

                 {/* Step Number Badge */}
                 <div className="absolute top-6 right-6 w-8 h-8 rounded-full bg-white/5 border border-white/10 flex items-center justify-center text-sm font-mono text-slate-500">
                    0{idx + 1}
                 </div>
               </div>
             </Reveal>
           ))}
        </div>
      </div>
    </section>
  );
};