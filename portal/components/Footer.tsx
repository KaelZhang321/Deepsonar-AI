import React from 'react';
import { Radar, Github, Twitter, Linkedin, ArrowUpRight } from 'lucide-react';
import { Link } from 'react-router-dom';

export const Footer: React.FC = () => {
  return (
    <footer className="bg-black border-t border-white/10 pt-20 pb-10 px-6 relative overflow-hidden">
      <div className="absolute top-0 left-0 w-full h-px bg-gradient-to-r from-transparent via-white/10 to-transparent"></div>
      
      <div className="max-w-7xl mx-auto relative z-10">
        <div className="grid grid-cols-1 md:grid-cols-12 gap-12 mb-20">
          <div className="md:col-span-5">
            <div className="flex items-center gap-3 mb-8">
              <div className="p-2 rounded-xl bg-brand-accent/10 border border-brand-accent/20">
                 <Radar className="w-6 h-6 text-brand-accent" />
              </div>
              <span className="text-2xl font-bold text-white tracking-tight">DeepSonar</span>
            </div>
            <p className="text-slate-400 max-w-sm mb-8 leading-relaxed">
              重构商业情报获取方式。
              <br/>
              利用下一代 AI 代理网络，为具有战略眼光的企业提供全流程自动化的决策支持。
            </p>
            <div className="flex gap-4">
              <a href="#" className="p-3 rounded-full bg-white/5 border border-white/5 hover:bg-white/10 hover:border-white/10 transition-all text-slate-400 hover:text-white">
                <Twitter className="w-5 h-5" />
              </a>
              <a href="#" className="p-3 rounded-full bg-white/5 border border-white/5 hover:bg-white/10 hover:border-white/10 transition-all text-slate-400 hover:text-white">
                <Github className="w-5 h-5" />
              </a>
              <a href="#" className="p-3 rounded-full bg-white/5 border border-white/5 hover:bg-white/10 hover:border-white/10 transition-all text-slate-400 hover:text-white">
                <Linkedin className="w-5 h-5" />
              </a>
            </div>
          </div>

          <div className="md:col-span-2 md:col-start-7">
            <h4 className="text-white font-bold mb-8">产品</h4>
            <ul className="space-y-4 text-sm text-slate-400">
              <li><Link to="/data-capture" className="hover:text-brand-accent transition-colors block py-1">全域情报捕获</Link></li>
              <li><Link to="/ai-processing" className="hover:text-brand-accent transition-colors block py-1">AI 深度关联</Link></li>
              <li><Link to="/report-generation" className="hover:text-brand-accent transition-colors block py-1">决策报告生成</Link></li>
              <li><Link to="/pricing" className="hover:text-brand-accent transition-colors block py-1">价格方案</Link></li>
              <li><Link to="/reports" className="hover:text-brand-accent transition-colors block py-1">报告样本库</Link></li>
            </ul>
          </div>

          <div className="md:col-span-2">
            <h4 className="text-white font-bold mb-8">资源</h4>
            <ul className="space-y-4 text-sm text-slate-400">
              <li><a href="#" className="hover:text-brand-accent transition-colors block py-1">开发文档</a></li>
              <li><a href="#" className="hover:text-brand-accent transition-colors block py-1">API 参考</a></li>
              <li><a href="#" className="hover:text-brand-accent transition-colors block py-1">系统状态</a></li>
              <li><a href="#" className="hover:text-brand-accent transition-colors block py-1">更新日志</a></li>
            </ul>
          </div>

           <div className="md:col-span-2">
            <h4 className="text-white font-bold mb-8">公司</h4>
            <ul className="space-y-4 text-sm text-slate-400">
              <li><a href="#" className="hover:text-brand-accent transition-colors block py-1">关于我们</a></li>
              <li><a href="#" className="hover:text-brand-accent transition-colors block py-1">招贤纳士</a></li>
              <li><a href="#" className="hover:text-brand-accent transition-colors block py-1">联系我们</a></li>
              <li><a href="#" className="hover:text-brand-accent transition-colors block py-1">法律条款</a></li>
            </ul>
          </div>
        </div>

        <div className="pt-8 border-t border-white/5 flex flex-col md:flex-row justify-between items-center gap-4 text-xs text-slate-600">
          <p>© 2024 DeepSonar Intelligence Inc.</p>
          <div className="flex items-center gap-2 group cursor-pointer hover:text-slate-400 transition-colors">
            <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div>
            All Systems Operational
          </div>
        </div>
      </div>
    </footer>
  );
};