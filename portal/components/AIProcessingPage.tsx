import React from 'react';
import { ArrowLeft, Cpu, Brain, Network, Sparkles, Zap, Filter, LinkIcon, AlertCircle } from 'lucide-react';
import { Link } from 'react-router-dom';
import { Reveal } from './ui/Reveal';

export const AIProcessingPage: React.FC = () => {
  const capabilities = [
    {
      icon: Filter,
      title: '智能去重去噪',
      description: '利用语义分析技术，自动识别并过滤重复内容和营销软文，保留真正有价值的信息。',
      metrics: ['99%去重准确率', '90%噪音过滤', '实时处理']
    },
    {
      icon: LinkIcon,
      title: '事件关联分析',
      description: '通过知识图谱技术，将分散的信息点串联成完整的事件脉络，发现隐藏的关联关系。',
      metrics: ['多维度关联', '时序分析', '因果推理']
    },
    {
      icon: Brain,
      title: '语义深度理解',
      description: '基于大语言模型，深度理解文本语义、情感倾向和关键要素，提取结构化信息。',
      metrics: ['实体识别', '情感分析', '要素提取']
    },
    {
      icon: Sparkles,
      title: '智能标注分类',
      description: '自动对信息进行主题分类、重要性评级和标签标注，构建结构化的信息体系。',
      metrics: ['100+分类维度', '5级重要性', '自动打标']
    }
  ];

  const aiModels = [
    {
      name: 'GPT-4 Turbo',
      usage: '文本理解与生成',
      performance: '高精度'
    },
    {
      name: 'BERT',
      usage: '语义相似度计算',
      performance: '高效率'
    },
    {
      name: 'Knowledge Graph',
      usage: '关系抽取与推理',
      performance: '高关联'
    },
    {
      name: 'Custom LLM',
      usage: '垂直领域专用',
      performance: '高准确'
    }
  ];

  const processingSteps = [
    {
      step: '01',
      title: '数据预处理',
      description: '清洗原始数据，标准化格式，去除无效信息'
    },
    {
      step: '02',
      title: '语义分析',
      description: 'NLP技术解析文本，提取关键实体和关系'
    },
    {
      step: '03',
      title: '智能关联',
      description: '构建知识图谱，发现事件间的隐藏联系'
    },
    {
      step: '04',
      title: '结果输出',
      description: '生成结构化、可视化的分析结果'
    }
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
        <div className="absolute inset-0 bg-gradient-to-b from-emerald-500/10 via-transparent to-transparent"></div>
        <div className="absolute top-20 left-1/2 -translate-x-1/2 w-[600px] h-[600px] bg-emerald-600/20 blur-[120px] rounded-full"></div>
        
        <div className="max-w-7xl mx-auto relative z-10">
          <Reveal>
            <div className="text-center mb-16">
              <div className="inline-flex items-center gap-3 px-4 py-2 rounded-full bg-emerald-500/20 border border-emerald-500/30 mb-6">
                <Cpu className="w-5 h-5 text-emerald-400" />
                <span className="text-sm font-medium text-emerald-300">AI 深度关联</span>
              </div>
              <h1 className="text-5xl md:text-6xl font-bold mb-6">
                <span className="gradient-text">告别信息噪音</span>
              </h1>
              <p className="text-xl text-slate-400 max-w-3xl mx-auto leading-relaxed">
                利用 LLM 大模型能力，自动去重、通过上下文理解剔除营销软文，<br />
                并将分散的信息点串联成完整的事件脉络。
              </p>
            </div>
          </Reveal>

          {/* Processing Flow */}
          <Reveal delay={0.2}>
            <div className="mb-20">
              <h2 className="text-3xl font-bold mb-12 text-center">
                <span className="gradient-text">AI处理流程</span>
              </h2>
              <div className="grid md:grid-cols-4 gap-6">
                {processingSteps.map((item, index) => (
                  <div key={index} className="relative">
                    <div className="glass rounded-2xl p-6 border border-slate-800 hover:border-emerald-500/50 transition-all h-full">
                      <div className="text-5xl font-bold text-emerald-500/20 mb-4">{item.step}</div>
                      <h3 className="text-xl font-bold mb-2">{item.title}</h3>
                      <p className="text-slate-400 text-sm">{item.description}</p>
                    </div>
                    {index < processingSteps.length - 1 && (
                      <div className="hidden md:block absolute top-1/2 -right-3 w-6 h-px bg-gradient-to-r from-emerald-500/50 to-transparent"></div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          </Reveal>

          {/* Core Capabilities */}
          <Reveal delay={0.3}>
            <div className="mb-20">
              <h2 className="text-3xl font-bold mb-12 text-center">
                <span className="gradient-text">核心能力</span>
              </h2>
              <div className="grid md:grid-cols-2 gap-6">
                {capabilities.map((cap, index) => {
                  const Icon = cap.icon;
                  return (
                    <div key={index} className="glass rounded-2xl p-8 border border-slate-800 hover:border-emerald-500/50 transition-all group">
                      <div className="flex items-start gap-4 mb-4">
                        <div className="w-12 h-12 rounded-xl bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-transform">
                          <Icon className="w-6 h-6 text-emerald-400" />
                        </div>
                        <div className="flex-1">
                          <h3 className="text-xl font-bold mb-2">{cap.title}</h3>
                          <p className="text-slate-400 leading-relaxed mb-4">{cap.description}</p>
                          <div className="flex flex-wrap gap-2">
                            {cap.metrics.map((metric, i) => (
                              <span key={i} className="px-3 py-1 rounded-full bg-slate-900 text-xs text-emerald-400 border border-slate-800">
                                {metric}
                              </span>
                            ))}
                          </div>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </Reveal>

          {/* AI Models */}
          <Reveal delay={0.4}>
            <div className="mb-20">
              <h2 className="text-3xl font-bold mb-12 text-center">
                <span className="gradient-text">AI模型矩阵</span>
              </h2>
              <div className="glass rounded-2xl p-8 border border-slate-800">
                <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
                  {aiModels.map((model, index) => (
                    <div key={index} className="text-center">
                      <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-gradient-to-br from-emerald-500/20 to-cyan-500/20 border border-emerald-500/30 flex items-center justify-center">
                        <Network className="w-8 h-8 text-emerald-400" />
                      </div>
                      <h4 className="font-bold mb-2">{model.name}</h4>
                      <p className="text-sm text-slate-400 mb-2">{model.usage}</p>
                      <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 text-xs text-emerald-400">
                        <Zap className="w-3 h-3" />
                        {model.performance}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </Reveal>

          {/* CTA */}
          <Reveal delay={0.5}>
            <div className="text-center glass rounded-2xl p-12 border border-slate-800">
              <div className="flex items-center justify-center gap-2 text-emerald-400 mb-4">
                <AlertCircle className="w-6 h-6" />
                <span className="text-sm font-semibold">AI驱动的智能分析</span>
              </div>
              <h3 className="text-3xl font-bold mb-4">
                <span className="gradient-text">让数据说人话</span>
              </h3>
              <p className="text-lg text-slate-400 mb-8 max-w-2xl mx-auto">
                从海量信息中提炼真知灼见，为您的决策提供可靠依据
              </p>
              <div className="flex flex-col sm:flex-row gap-4 items-center justify-center">
                <button className="px-8 py-4 bg-white text-black rounded-full font-semibold text-lg hover:bg-slate-200 transition-all">
                  预约演示
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
