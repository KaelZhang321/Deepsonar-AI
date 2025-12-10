import React from 'react';
import { ArrowLeft, Building2, MapPin, Mail, Phone, Globe, Users, Target, Lightbulb, Shield } from 'lucide-react';
import { Link } from 'react-router-dom';
import { Reveal } from './ui/Reveal';

export const AboutPage: React.FC = () => {
  const values = [
    {
      icon: Target,
      title: '使命',
      description: '通过人工智能技术，让每一家企业都能拥有顶级的商业情报分析能力。'
    },
    {
      icon: Lightbulb,
      title: '愿景',
      description: '成为全球领先的 AI 商业智能服务提供商，重新定义企业决策方式。'
    },
    {
      icon: Users,
      title: '价值观',
      description: '以客户为中心、追求卓越、持续创新、诚信为本。'
    },
    {
      icon: Shield,
      title: '承诺',
      description: '保护客户数据安全，提供可靠、准确、及时的情报服务。'
    }
  ];

  return (
    <div className="min-h-screen bg-brand-dark text-white selection:bg-brand-accent/30">
      {/* Header with Back Button */}
      <div className="fixed top-0 w-full z-50 glass border-b border-white/5 bg-brand-dark/50 backdrop-blur-xl">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center gap-4">
          <Link 
            to="/" 
            className="flex items-center gap-2 text-slate-400 hover:text-white transition-colors group text-sm font-medium"
          >
            <ArrowLeft className="w-4 h-4 group-hover:-translate-x-1 transition-transform" />
            <span>返回首页</span>
          </Link>
          <div className="h-4 w-px bg-white/10"></div>
          <h1 className="text-sm font-semibold text-white/50">关于我们</h1>
        </div>
      </div>

      {/* Main Content */}
      <div className="pt-32 pb-20 px-6">
        <div className="max-w-7xl mx-auto">
          {/* Page Title */}
          <Reveal>
            <div className="text-center mb-16">
              <h2 className="text-4xl md:text-5xl font-bold mb-4">
                <span className="gradient-text">关于深纳数据</span>
              </h2>
              <p className="text-lg text-slate-400 max-w-2xl mx-auto">
                用 AI 重构商业情报，让数据驱动每一个决策
              </p>
            </div>
          </Reveal>

          {/* Company Introduction */}
          <Reveal delay={0.1}>
            <div className="glass rounded-2xl p-8 md:p-12 border border-slate-800 mb-12">
              <div className="flex items-center gap-4 mb-6">
                <div className="p-3 rounded-lg bg-brand-accent/10 border border-brand-accent/30">
                  <Building2 className="w-6 h-6 text-brand-accent" />
                </div>
                <h3 className="text-2xl font-bold text-white">公司简介</h3>
              </div>
              <div className="prose prose-invert max-w-none">
                <p className="text-slate-300 leading-relaxed mb-4">
                  深纳数据（DeepSonar）是一家专注于人工智能商业情报分析的科技公司，致力于为企业提供全流程自动化的决策支持服务。
                </p>
                <p className="text-slate-300 leading-relaxed mb-4">
                  我们运用先进的 AI Agent 技术和大语言模型，从海量互联网数据中挖掘有价值的商业洞察，帮助企业快速了解市场动态、竞争格局和行业趋势，做出更明智的商业决策。
                </p>
                <p className="text-slate-300 leading-relaxed">
                  深纳数据的核心产品覆盖全域情报捕获、AI 深度关联分析、决策报告生成等多个环节，为金融投资、战略咨询、企业管理等领域的客户提供专业、高效的服务。
                </p>
              </div>
            </div>
          </Reveal>

          {/* Values Grid */}
          <Reveal delay={0.2}>
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
              {values.map((value, index) => (
                <div 
                  key={index}
                  className="glass rounded-xl p-6 border border-slate-800 hover:border-brand-accent/50 transition-all"
                >
                  <div className="p-3 rounded-lg bg-brand-accent/10 border border-brand-accent/30 w-fit mb-4">
                    <value.icon className="w-5 h-5 text-brand-accent" />
                  </div>
                  <h4 className="text-lg font-bold text-white mb-2">{value.title}</h4>
                  <p className="text-sm text-slate-400 leading-relaxed">{value.description}</p>
                </div>
              ))}
            </div>
          </Reveal>

          {/* Contact Information */}
          <Reveal delay={0.3}>
            <div className="glass rounded-2xl p-8 md:p-12 border border-slate-800">
              <h3 className="text-2xl font-bold text-white mb-8">联系我们</h3>
              <div className="grid md:grid-cols-2 gap-8">
                <div className="space-y-6">
                  <div className="flex items-start gap-4">
                    <div className="p-3 rounded-lg bg-slate-800 border border-slate-700">
                      <Building2 className="w-5 h-5 text-slate-400" />
                    </div>
                    <div>
                      <h4 className="text-sm font-semibold text-slate-300 mb-1">公司名称</h4>
                      <p className="text-white">天津市米蒙科技有限公司</p>
                    </div>
                  </div>
                  
                  <div className="flex items-start gap-4">
                    <div className="p-3 rounded-lg bg-slate-800 border border-slate-700">
                      <MapPin className="w-5 h-5 text-slate-400" />
                    </div>
                    <div>
                      <h4 className="text-sm font-semibold text-slate-300 mb-1">公司地址</h4>
                      <p className="text-white text-sm leading-relaxed">
                        天津市滨海高新区华苑产业区开华道22号5号楼西塔208室
                        <br />
                        <span className="text-slate-500 text-xs">
                          (入驻海琪(天津)商务秘书有限公司托管第67号)
                        </span>
                      </p>
                    </div>
                  </div>

                  <div className="flex items-start gap-4">
                    <div className="p-3 rounded-lg bg-slate-800 border border-slate-700">
                      <Mail className="w-5 h-5 text-slate-400" />
                    </div>
                    <div>
                      <h4 className="text-sm font-semibold text-slate-300 mb-1">电子邮箱</h4>
                      <a href="mailto:contact@deepsonar.com.cn" className="text-brand-accent hover:underline">
                        contact@deepsonar.com.cn
                      </a>
                    </div>
                  </div>

                  <div className="flex items-start gap-4">
                    <div className="p-3 rounded-lg bg-slate-800 border border-slate-700">
                      <Globe className="w-5 h-5 text-slate-400" />
                    </div>
                    <div>
                      <h4 className="text-sm font-semibold text-slate-300 mb-1">官方网站</h4>
                      <a href="https://www.deepsonar.com.cn" className="text-brand-accent hover:underline">
                        www.deepsonar.com.cn
                      </a>
                    </div>
                  </div>
                </div>

                <div className="flex items-center justify-center">
                  <div className="text-center p-8 rounded-2xl bg-gradient-to-br from-brand-accent/10 to-transparent border border-brand-accent/20">
                    <div className="text-6xl mb-4">🔍</div>
                    <h4 className="text-xl font-bold text-white mb-2">DeepSonar</h4>
                    <p className="text-slate-400 text-sm">深纳数据 · 智见未来</p>
                  </div>
                </div>
              </div>
            </div>
          </Reveal>

          {/* CTA */}
          <Reveal delay={0.4}>
            <div className="mt-12 text-center">
              <Link 
                to="/apply"
                className="inline-flex items-center gap-2 px-8 py-4 bg-white text-black rounded-full font-semibold text-lg hover:bg-slate-200 transition-all"
              >
                申请免费试用
              </Link>
            </div>
          </Reveal>
        </div>
      </div>
    </div>
  );
};
