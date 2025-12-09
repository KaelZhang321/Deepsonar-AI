import React, { useState } from 'react';
import { Mail, Send, ArrowRight, CheckCircle, Building, User, FileText } from 'lucide-react';
import { Link } from 'react-router-dom';
import { Reveal } from './ui/Reveal';
import emailjs from '@emailjs/browser';

export const ApplyTrialPage: React.FC = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    organization: '',
    title: '',
    useCase: 'market_analysis',
    message: ''
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      console.log('Sending email with data:', formData);
      
      const result = await emailjs.send(
        'service_e6s226n',
        'template_tyo9h3m',
        {
          from_name: formData.name,
          from_email: formData.email,
          organization: formData.organization,
          title: formData.title,
          use_case: formData.useCase,
          message: formData.message
        },
        {
          publicKey: 'i_hYRlzXiP6p3jDFe'
        }
      );

      console.log('EmailJS response:', result);
      
      if (result.status === 200) {
        setSubmitted(true);
      } else {
        console.error('Unexpected status:', result);
        alert('Failed to send application. Please try again.');
      }
    } catch (error) {
      console.error('Error submitting form:', error);
      // More detailed error logging
      if (error instanceof Error) {
        console.error('Error message:', error.message);
        console.error('Error stack:', error.stack);
      }
      alert('An error occurred. Please try again later.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div className="min-h-screen bg-brand-dark text-white relative selection:bg-brand-accent/30 overflow-hidden">
      {/* Background Elements */}
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute top-[-10%] right-[-5%] w-[800px] h-[800px] bg-indigo-600/10 blur-[150px] rounded-full mix-blend-screen opacity-30 animate-pulse-slow" />
        <div className="absolute bottom-[-10%] left-[-10%] w-[800px] h-[800px] bg-cyan-600/10 blur-[150px] rounded-full mix-blend-screen opacity-20 animate-pulse-slow delay-1000" />
        <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20 brightness-100 contrast-150" />
      </div>

      {/* Navbar Placeholder (Back Button) */}
      <div className="fixed top-0 w-full z-50 px-6 py-6">
        <Link to="/" className="inline-flex items-center gap-2 text-slate-400 hover:text-white transition-colors bg-black/20 backdrop-blur-md px-4 py-2 rounded-full border border-white/5 hover:border-white/10 group">
          <ArrowRight className="w-4 h-4 rotate-180 group-hover:-translate-x-1 transition-transform" />
          <span className="text-sm font-medium">返回首页</span>
        </Link>
      </div>

      <div className="relative z-10 pt-32 pb-20 px-6 max-w-7xl mx-auto flex flex-col md:flex-row gap-16 items-start">
        {/* Left Side: Info */}
        <div className="flex-1 sticky top-32">
          <Reveal>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-brand-accent/10 border border-brand-accent/20 text-brand-accent text-xs font-semibold mb-6 tracking-wide uppercase">
              Free Trial Application
            </div>
            <h1 className="text-5xl md:text-6xl font-bold tracking-tight mb-6 leading-tight">
              开启您的 <br />
              <span className="bg-clip-text text-transparent bg-gradient-to-r from-white via-indigo-200 to-cyan-200">
                智能情报之旅
              </span>
            </h1>
            <p className="text-lg text-slate-400 mb-10 leading-relaxed max-w-lg">
              体验 DeepSonar 强大的全域情报捕获与深度决策分析能力。提交申请后，我们的专家团队将在 24 小时内为您开通企业级试用权限。
            </p>
            
            <div className="space-y-6">
              <div className="flex items-center gap-4 p-4 rounded-2xl bg-white/5 border border-white/5 backdrop-blur-sm">
                <div className="w-12 h-12 rounded-xl bg-indigo-500/20 flex items-center justify-center text-indigo-400">
                  <Building className="w-6 h-6" />
                </div>
                <div>
                  <h3 className="font-semibold text-white">企业级部署</h3>
                  <p className="text-sm text-slate-400">支持私有化部署与定制模型微调</p>
                </div>
              </div>
              <div className="flex items-center gap-4 p-4 rounded-2xl bg-white/5 border border-white/5 backdrop-blur-sm">
                <div className="w-12 h-12 rounded-xl bg-cyan-500/20 flex items-center justify-center text-cyan-400">
                  <User className="w-6 h-6" />
                </div>
                <div>
                  <h3 className="font-semibold text-white">1v1 专家支持</h3>
                  <p className="text-sm text-slate-400">专属客户经理协助您完成系统配置</p>
                </div>
              </div>
            </div>
          </Reveal>
        </div>

        {/* Right Side: Form */}
        <div className="flex-1 w-full max-w-xl">
          <Reveal delay={0.2}>
            <div className="bg-[#0a0a0a]/80 backdrop-blur-xl border border-white/10 p-8 md:p-10 rounded-3xl shadow-2xl relative overflow-hidden group">
               {/* Glow Effect */}
               <div className="absolute -inset-1 bg-gradient-to-br from-indigo-500/20 via-transparent to-cyan-500/20 opacity-0 group-hover:opacity-100 blur-xl transition-opacity duration-700 pointer-events-none" />

              {submitted ? (
                <div className="text-center py-20 flex flex-col items-center animate-in fade-in zoom-in duration-500">
                  <div className="w-20 h-20 bg-green-500/10 text-green-400 rounded-full flex items-center justify-center mb-6">
                    <CheckCircle className="w-10 h-10" />
                  </div>
                  <h3 className="text-2xl font-bold text-white mb-4">申请已提交</h3>
                  <p className="text-slate-400 mb-8 max-w-sm">
                    我们已收到您的申请。我们的团队将在 24 小时内审核并在通过后联系您。
                  </p>
                  <button 
                    onClick={() => {
                        setSubmitted(false); // Reset form
                        setFormData({...formData, message: ''}); 
                    }}
                    className="text-indigo-400 hover:text-indigo-300 font-medium flex items-center gap-2 transition-colors"
                  >
                    重新提交或返回 <ArrowRight className="w-4 h-4" />
                  </button>
                </div>
              ) : (
                <form onSubmit={handleSubmit} className="space-y-6 relative z-10">
                  <div className="text-center mb-8">
                     <h2 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400">填写申请信息</h2>
                  </div>

                  <div className="grid md:grid-cols-2 gap-6">
                    <div className="space-y-2">
                      <label className="text-sm font-semibold text-slate-300 ml-1">姓名</label>
                      <input 
                        type="text" 
                        name="name" 
                        required 
                        value={formData.name}
                        onChange={handleChange}
                        className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500/50 focus:bg-white/10 transition-all font-medium"
                        placeholder="您的称呼"
                      />
                    </div>
                    <div className="space-y-2">
                       <label className="text-sm font-semibold text-slate-300 ml-1">职位</label>
                       <input 
                        type="text" 
                        name="title" 
                        value={formData.title}
                        onChange={handleChange}
                        className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500/50 focus:bg-white/10 transition-all font-medium"
                        placeholder="例如：市场总监"
                      />
                    </div>
                  </div>

                  <div className="space-y-2">
                    <label className="text-sm font-semibold text-slate-300 ml-1">工作邮箱</label>
                    <div className="relative">
                      <Mail className="absolute left-4 top-3.5 w-5 h-5 text-slate-500" />
                      <input 
                        type="email" 
                        name="email" 
                        required 
                        value={formData.email}
                        onChange={handleChange}
                        className="w-full bg-white/5 border border-white/10 rounded-xl pl-12 pr-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500/50 focus:bg-white/10 transition-all font-medium"
                        placeholder="name@company.com"
                      />
                    </div>
                  </div>

                  <div className="space-y-2">
                     <label className="text-sm font-semibold text-slate-300 ml-1">所属机构/公司</label>
                     <input 
                        type="text" 
                        name="organization" 
                        required 
                        value={formData.organization}
                        onChange={handleChange}
                        className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500/50 focus:bg-white/10 transition-all font-medium"
                        placeholder="请输入公司全称"
                      />
                  </div>

                  <div className="space-y-2">
                    <label className="text-sm font-semibold text-slate-300 ml-1">主要用途</label>
                    <div className="relative">
                        <FileText className="absolute left-4 top-3.5 w-5 h-5 text-slate-500" />
                        <select 
                            name="useCase" 
                            value={formData.useCase}
                            onChange={handleChange}
                            className="w-full bg-white/5 border border-white/10 rounded-xl pl-12 pr-4 py-3 text-white focus:outline-none focus:border-indigo-500/50 focus:bg-white/10 transition-all font-medium appearance-none cursor-pointer"
                        >
                            <option value="market_analysis" className="bg-[#0a0a0a]">市场宏观分析</option>
                            <option value="competitor_tracking" className="bg-[#0a0a0a]">竞争对手追踪</option>
                            <option value="risk_monitoring" className="bg-[#0a0a0a]">舆情风险监测</option>
                            <option value="investment_research" className="bg-[#0a0a0a]">投资决策研报</option>
                            <option value="other" className="bg-[#0a0a0a]">其他定制需求</option>
                        </select>
                        <div className="absolute right-4 top-4 border-l-4 border-t-4 border-transparent border-t-slate-500 pointer-events-none"></div>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <label className="text-sm font-semibold text-slate-300 ml-1">留言 (选填)</label>
                    <textarea 
                        name="message" 
                        rows={4}
                        value={formData.message}
                        onChange={handleChange}
                        className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500/50 focus:bg-white/10 transition-all font-medium resize-none"
                        placeholder="请简单描述您的具体需求..."
                    />
                  </div>

                  <button 
                    type="submit" 
                    disabled={isSubmitting}
                    className="w-full py-4 rounded-xl bg-gradient-to-r from-brand-accent to-brand-secondary text-white font-bold text-lg hover:shadow-[0_0_20px_rgba(99,102,241,0.5)] transition-all transform hover:-translate-y-1 active:scale-95 disabled:opacity-70 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                  >
                    {isSubmitting ? (
                        <>正在处理...</>
                    ) : (
                        <>
                           提交申请 <Send className="w-5 h-5 ml-1" />
                        </>
                    )}
                  </button>
                  <p className="text-center text-xs text-slate-500 mt-4">
                    我们会严格保密您的信息
                  </p>
                </form>
              )}
            </div>
          </Reveal>
        </div>
      </div>
    </div>
  );
};
