import React from 'react';
import { ArrowLeft, Globe, Database, Share2, Activity, Rss, Map, TrendingUp, CheckCircle } from 'lucide-react';
import { Link } from 'react-router-dom';
import { Reveal } from './ui/Reveal';

export const DataCapturePage: React.FC = () => {
  const dataSources = [
    {
      icon: Database,
      title: '招投标平台',
      description: '实时追踪全国各地招投标信息，捕获商业机会',
      coverage: '覆盖3000+招标网站',
      color: 'emerald'
    },
    {
      icon: Share2,
      title: '社交媒体',
      description: '监控微博、Twitter等平台的品牌舆情和用户反馈',
      coverage: '支持10+主流平台',
      color: 'blue'
    },
    {
      icon: Activity,
      title: '财经资讯',
      description: '聚合财报、公告、研报等专业金融数据',
      coverage: '5000+上市公司',
      color: 'orange'
    },
    {
      icon: Rss,
      title: '行业媒体',
      description: '垂直领域的专业媒体和行业报告',
      coverage: '1000+垂直媒体',
      color: 'purple'
    },
    {
      icon: Map,
      title: '政策法规',
      description: '政府网站、法规库的政策变化追踪',
      coverage: '全国省市政府',
      color: 'cyan'
    },
    {
      icon: TrendingUp,
      title: '市场数据',
      description: '股价、汇率、大宗商品等实时市场数据',
      coverage: '全球市场覆盖',
      color: 'pink'
    }
  ];

  const features = [
    {
      title: '智能爬虫集群',
      description: '分布式爬虫架构，7x24小时不间断采集，自动处理反爬机制，确保数据获取的稳定性和完整性。'
    },
    {
      title: '实时监控预警',
      description: '关键词、企业、事件的实时监控，重要信息第一时间推送，不错过任何关键商业信号。'
    },
    {
      title: '定制化追踪',
      description: '根据您的行业和关注点，定制专属的数据源和追踪规则，让信息采集更加精准高效。'
    },
    {
      title: '结构化存储',
      description: '采集的数据自动清洗、分类、标注，存储为结构化格式，便于后续分析和检索。'
    }
  ];

  const stats = [
    { value: '50亿+', label: '日均数据量' },
    { value: '10000+', label: '数据源覆盖' },
    { value: '99.9%', label: '服务可用性' },
    { value: '<5秒', label: '实时响应' }
  ];

  return (
    <div className="min-h-screen bg-brand-dark text-white selection:bg-brand-accent/30">
      {/* Header */}
      <div className="fixed top-0 w-full z-50 glass border-b border-white/5 bg-brand-dark/50 backdrop-blur-xl">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center gap-4">
          <Link 
            to="/" 
            className="flex items-center gap-2 text-slate-400 hover:text-white transition-colors group text-sm font-medium"
          >
            <ArrowLeft className="w-4 h-4 group-hover:-translate-x-1 transition-transform" />
            <span>返回首页</span>
          </Link>
        </div>
      </div>

      {/* Hero Section */}
      <div className="pt-32 pb-20 px-6 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-b from-brand-accent/5 via-transparent to-transparent"></div>
        <div className="absolute top-20 left-1/2 -translate-x-1/2 w-[600px] h-[600px] bg-brand-accent/10 blur-[120px] rounded-full animate-pulse-slow"></div>
        
        <div className="max-w-7xl mx-auto relative z-10">
          <Reveal>
            <div className="text-center mb-16">
              <div className="inline-flex items-center gap-3 px-4 py-2 rounded-full bg-indigo-500/20 border border-indigo-500/30 mb-6">
                <Globe className="w-5 h-5 text-indigo-400" />
                <span className="text-sm font-medium text-indigo-300">全域情报捕获</span>
              </div>
              <h1 className="text-5xl md:text-6xl font-bold mb-6">
                <span className="gradient-text">不只是搜索，更是全网监听</span>
              </h1>
              <p className="text-xl text-slate-400 max-w-3xl mx-auto leading-relaxed">
                支持自定义追踪上市公司财报、行业垂直媒体、招投标网站及社交舆论。<br />
                您关心的每一个信号，我们都不会错过。
              </p>
            </div>
          </Reveal>

          {/* Stats */}
          <Reveal delay={0.2}>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-20">
              {stats.map((stat, index) => (
                <div key={index} className="text-center glass rounded-2xl p-6 border border-slate-800">
                  <div className="text-3xl md:text-4xl font-bold text-indigo-400 mb-2">{stat.value}</div>
                  <div className="text-sm text-slate-500">{stat.label}</div>
                </div>
              ))}
            </div>
          </Reveal>

          {/* Data Sources Grid */}
          <Reveal delay={0.3}>
            <div className="mb-20">
              <h2 className="text-3xl font-bold mb-12 text-center">
                <span className="gradient-text">全域数据源覆盖</span>
              </h2>
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                {dataSources.map((source, index) => {
                  const Icon = source.icon;
                  const colorClasses = {
                    emerald: 'bg-emerald-500/20 border-emerald-500/30 text-emerald-400',
                    blue: 'bg-blue-500/20 border-blue-500/30 text-blue-400',
                    orange: 'bg-orange-500/20 border-orange-500/30 text-orange-400',
                    purple: 'bg-purple-500/20 border-purple-500/30 text-purple-400',
                    cyan: 'bg-cyan-500/20 border-cyan-500/30 text-cyan-400',
                    pink: 'bg-pink-500/20 border-pink-500/30 text-pink-400'
                  }[source.color];

                  return (
                    <div key={index} className="glass rounded-2xl p-6 border border-slate-800 hover:border-slate-600 transition-all group">
                      <div className={`w-12 h-12 rounded-xl ${colorClasses} border flex items-center justify-center mb-4 group-hover:scale-110 transition-transform`}>
                        <Icon className="w-6 h-6" />
                      </div>
                      <h3 className="text-xl font-bold mb-2">{source.title}</h3>
                      <p className="text-slate-400 mb-3 text-sm">{source.description}</p>
                      <div className="text-xs text-slate-500 font-mono">{source.coverage}</div>
                    </div>
                  );
                })}
              </div>
            </div>
          </Reveal>

          {/* Features */}
          <Reveal delay={0.4}>
            <div className="mb-20">
              <h2 className="text-3xl font-bold mb-12 text-center">
                <span className="gradient-text">核心能力</span>
              </h2>
              <div className="grid md:grid-cols-2 gap-6">
                {features.map((feature, index) => (
                  <div key={index} className="glass rounded-2xl p-8 border border-slate-800 hover:border-indigo-500/50 transition-all">
                    <div className="flex items-start gap-4">
                      <CheckCircle className="w-6 h-6 text-indigo-400 flex-shrink-0 mt-1" />
                      <div>
                        <h3 className="text-xl font-bold mb-2">{feature.title}</h3>
                        <p className="text-slate-400 leading-relaxed">{feature.description}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </Reveal>

          {/* CTA */}
          <Reveal delay={0.5}>
            <div className="text-center glass rounded-2xl p-12 border border-slate-800">
              <h3 className="text-3xl font-bold mb-4">
                <span className="gradient-text">立即体验全域情报捕获</span>
              </h3>
              <p className="text-lg text-slate-400 mb-8 max-w-2xl mx-auto">
                让AI帮您24小时监控全网信息，不错过任何商业机会
              </p>
              <div className="flex flex-col sm:flex-row gap-4 items-center justify-center">
                <button className="px-8 py-4 bg-white text-black rounded-full font-semibold text-lg hover:bg-slate-200 transition-all">
                  免费试用
                </button>
                <Link 
                  to="/pricing"
                  className="px-8 py-4 rounded-full border border-slate-700 text-slate-300 font-semibold text-lg hover:bg-slate-800 hover:border-slate-600 transition-all"
                >
                  查看价格
                </Link>
              </div>
            </div>
          </Reveal>
        </div>
      </div>
    </div>
  );
};
