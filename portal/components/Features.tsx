import React from 'react';
import { Globe, Cpu, FileText, ArrowUpRight, Database, Share2, Activity, BarChart3, ShieldCheck } from 'lucide-react';
import { Link } from 'react-router-dom';
import { Reveal } from './ui/Reveal';
import { ResponsiveContainer, AreaChart, Area, XAxis, Tooltip, CartesianGrid } from 'recharts';

// Mock Data for Charts
const chartData = [
  { name: 'Mon', risk: 400, opportunity: 240 },
  { name: 'Tue', risk: 300, opportunity: 139 },
  { name: 'Wed', risk: 200, opportunity: 980 },
  { name: 'Thu', risk: 278, opportunity: 390 },
  { name: 'Fri', risk: 189, opportunity: 480 },
  { name: 'Sat', risk: 239, opportunity: 380 },
  { name: 'Sun', risk: 349, opportunity: 430 },
];

export const Features: React.FC = () => {
  return (
    <section id="features" className="py-32 px-6 relative overflow-hidden">
      {/* Background Gradients */}
      <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-brand-secondary/10 rounded-full blur-[120px] -z-10"></div>
      
      <div className="max-w-7xl mx-auto">
        <Reveal>
          <div className="mb-20 text-center md:text-left">
            <h2 className="text-4xl md:text-5xl font-bold mb-6 tracking-tight">
              不仅仅是聚合器，<br />
              <span className="bg-clip-text text-transparent bg-gradient-to-r from-slate-400 to-slate-600">
                更是您的全自动化数据分析师。
              </span>
            </h2>
            <p className="text-xl text-slate-400 max-w-2xl leading-relaxed">
              DeepSonar 深入互联网的每一个角落，识别潜在风险与机遇，为您交付包含趋势预测与数据洞察的高质量报告。
            </p>
          </div>
        </Reveal>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 auto-rows-[minmax(400px,auto)]">
          
          {/* Card 1: Data Capture */}
          <Reveal className="md:col-span-2 row-span-1 h-full w-full">
            <div className="h-full rounded-3xl p-8 md:p-10 bg-brand-card/30 border border-white/5 relative overflow-hidden group hover:border-brand-accent/20 transition-all duration-500 hover:shadow-2xl hover:shadow-brand-accent/5">
              <div className="absolute inset-0 bg-gradient-to-br from-brand-accent/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-700"></div>
              
              <div className="relative z-10 flex flex-col h-full justify-between">
                <div>
                  <div className="w-14 h-14 rounded-2xl bg-brand-card border border-white/10 flex items-center justify-center mb-8 shadow-inner group-hover:scale-110 transition-transform duration-500">
                    <Globe className="w-7 h-7 text-brand-accent" />
                  </div>
                  <h3 className="text-3xl font-bold mb-4 text-white">全域情报捕获</h3>
                  <p className="text-slate-400 text-lg leading-relaxed max-w-md mb-8">
                    全网监听，不留死角。自定义追踪源覆盖全球主流财经媒体、社交平台及垂直行业论坛。
                  </p>
                  <Link 
                    to="/data-capture"
                    className="inline-flex items-center gap-2 text-white/70 hover:text-brand-accent transition-colors font-medium group/link"
                  >
                    了解更多 <ArrowUpRight className="w-4 h-4 group-hover/link:translate-x-0.5 group-hover/link:-translate-y-0.5 transition-transform" />
                  </Link>
                </div>

                {/* Floating Elements Animation */}
                <div className="mt-8 flex gap-4 overflow-hidden mask-linear-fade">
                    <div className="glass px-4 py-2 rounded-full flex items-center gap-2 text-xs text-slate-300 animate-float" style={{animationDelay: '0s'}}>
                        <Database className="w-3 h-3 text-emerald-400" /> 招投标
                    </div>
                     <div className="glass px-4 py-2 rounded-full flex items-center gap-2 text-xs text-slate-300 animate-float" style={{animationDelay: '2s'}}>
                        <Share2 className="w-3 h-3 text-blue-400" /> 社交舆情
                    </div>
                     <div className="glass px-4 py-2 rounded-full flex items-center gap-2 text-xs text-slate-300 animate-float" style={{animationDelay: '4s'}}>
                        <Activity className="w-3 h-3 text-orange-400" /> 实时财报
                    </div>
                </div>
              </div>
              
              {/* Decorative Blur */}
               <div className="absolute -bottom-20 -right-20 w-64 h-64 bg-brand-accent/10 blur-[80px] rounded-full group-hover:bg-brand-accent/20 transition-colors duration-700"></div>
            </div>
          </Reveal>

          {/* Card 2: AI Processing */}
          <Reveal className="md:col-span-1 row-span-1 h-full w-full" delay={0.2}>
            <div className="h-full rounded-3xl p-8 bg-brand-card/30 border border-white/5 relative overflow-hidden group hover:border-brand-secondary/20 transition-all duration-500 flex flex-col hover:shadow-2xl hover:shadow-brand-secondary/5">
              <div className="absolute inset-0 bg-gradient-to-t from-brand-secondary/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-700"></div>
              
              <div className="relative z-10 mb-8">
                <div className="w-14 h-14 rounded-2xl bg-brand-card border border-white/10 flex items-center justify-center mb-8 shadow-inner group-hover:scale-110 transition-transform duration-500">
                  <Cpu className="w-7 h-7 text-brand-secondary" />
                </div>
                <h3 className="text-2xl font-bold mb-4 text-white">AI 深度清洗</h3>
                <p className="text-slate-400 text-sm leading-relaxed mb-6">
                  利用 LLM 剔除噪音，自动识别营销软文与虚假信息，还原事件真相。
                </p>
                <Link 
                  to="/ai-processing"
                  className="inline-flex items-center gap-2 text-white/70 hover:text-brand-secondary transition-colors text-sm font-medium group/link"
                >
                  深度关联技术 <ArrowUpRight className="w-4 h-4 group-hover/link:translate-x-0.5 group-hover/link:-translate-y-0.5 transition-transform" />
                </Link>
              </div>

               {/* Process Visual */}
               <div className="flex-1 bg-black/20 rounded-xl border border-white/5 p-4 relative overflow-hidden flex flex-col items-center justify-center gap-3 group-hover:border-brand-secondary/20 transition-colors">
                  <div className="w-full flex justify-center gap-1">
                     <span className="w-1 h-4 bg-red-500/20 rounded-full animate-pulse"></span>
                     <span className="w-1 h-8 bg-brand-secondary/40 rounded-full animate-[pulse_1.5s_infinite]"></span>
                     <span className="w-1 h-5 bg-brand-secondary/60 rounded-full animate-[pulse_1s_infinite]"></span>
                     <span className="w-1 h-10 bg-brand-secondary rounded-full animate-[pulse_2s_infinite]"></span>
                  </div>
                   
                   <div className="w-full h-10 bg-brand-secondary/10 border border-brand-secondary/30 rounded flex items-center justify-center text-brand-secondary text-xs font-mono tracking-wider">
                      <ShieldCheck className="w-3 h-3 mr-2" />
                      VERIFIED
                   </div>
               </div>
            </div>
          </Reveal>

          {/* Card 3: Strategic Reporting */}
           <Reveal className="md:col-span-3 row-span-1 w-full" delay={0.4}>
            <div className="h-full rounded-3xl p-8 md:p-12 bg-brand-card/30 border border-white/5 relative overflow-hidden group hover:border-sky-500/20 transition-all duration-500 flex flex-col md:flex-row items-center gap-12 hover:shadow-2xl hover:shadow-sky-500/5">
               
               <div className="md:w-1/3 relative z-10">
                  <div className="w-14 h-14 rounded-2xl bg-brand-card border border-white/10 flex items-center justify-center mb-8 shadow-inner group-hover:scale-110 transition-transform duration-500">
                    <FileText className="w-7 h-7 text-sky-400" />
                  </div>
                  <h3 className="text-3xl font-bold mb-4 text-white">结构化决策报告</h3>
                  <p className="text-slate-400 text-lg leading-relaxed mb-8">
                    自动生成 PDF/HTML 格式的深度周报。包含关键数据趋势、SWOT 分析初稿及 AI 辅助的行动建议。
                  </p>
                  <div className="flex items-center gap-6">
                    <Link 
                      to="/report-generation"
                      className="text-sky-400 flex items-center gap-2 text-sm font-semibold hover:text-sky-300 transition-colors group/link"
                    >
                      生成逻辑 <ArrowUpRight className="w-4 h-4 group-hover/link:translate-x-0.5 group-hover/link:-translate-y-0.5 transition-transform" />
                    </Link>
                    <Link 
                      to="/reports"
                      className="text-slate-500 flex items-center gap-2 text-sm font-medium hover:text-white transition-colors"
                    >
                      查看样本库
                    </Link>
                  </div>
               </div>

               {/* Chart Mockup */}
               <div className="md:w-2/3 w-full h-[300px] relative z-10 bg-black/40 rounded-2xl border border-white/10 p-6 shadow-2xl overflow-hidden group-hover:border-sky-500/20 transition-colors">
                  <div className="flex justify-between items-start mb-6">
                      <div>
                        <h4 className="text-sm font-semibold text-slate-200">综合趋势分析</h4>
                        <p className="text-xs text-slate-500 mt-1">Real-time Data Aggregation</p>
                      </div>
                      <div className="px-2 py-1 rounded bg-sky-500/10 text-sky-400 text-xs font-mono">LIVE</div>
                  </div>
                  <div className="h-[200px] w-full">
                    <ResponsiveContainer width="100%" height="100%">
                      <AreaChart data={chartData}>
                        <defs>
                          <linearGradient id="colorOpp" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#38bdf8" stopOpacity={0.2}/>
                            <stop offset="95%" stopColor="#38bdf8" stopOpacity={0}/>
                          </linearGradient>
                          <linearGradient id="colorRisk" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#ef4444" stopOpacity={0.2}/>
                            <stop offset="95%" stopColor="#ef4444" stopOpacity={0}/>
                          </linearGradient>
                        </defs>
                        <XAxis dataKey="name" stroke="#475569" fontSize={10} tickLine={false} axisLine={false} dy={10} />
                        <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                        <Tooltip 
                            contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px', fontSize: '12px' }} 
                            cursor={{ stroke: 'rgba(255,255,255,0.1)' }}
                        />
                        <Area type="monotone" dataKey="opportunity" stroke="#38bdf8" strokeWidth={2} fill="url(#colorOpp)" />
                        <Area type="monotone" dataKey="risk" stroke="#ef4444" strokeWidth={2} fill="url(#colorRisk)" />
                      </AreaChart>
                    </ResponsiveContainer>
                  </div>
               </div>
            </div>
          </Reveal>

        </div>
      </div>
    </section>
  );
};