import React from 'react';
import { ArrowLeft, FileText, Download, Calendar, BarChart3, PieChart, TrendingUp, FileSpreadsheet, Presentation, CheckCircle2 } from 'lucide-react';
import { Link } from 'react-router-dom';
import { Reveal } from './ui/Reveal';

export const ReportGenerationPage: React.FC = () => {
  const reportTypes = [
    {
      icon: Calendar,
      title: '日报 & 周报',
      description: '每日/每周自动生成行业动态摘要，包含关键事件、数据趋势和重要变化',
      features: ['自动定时推送', '个性化内容', '多维度统计'],
      color: 'sky'
    },
    {
      icon: BarChart3,
      title: '趋势分析报告',
      description: '基于历史数据的趋势预测和模式识别，帮助您把握市场走向',
      features: ['数据可视化', '预测建模', '异常检测'],
      color: 'purple'
    },
    {
      icon: PieChart,
      title: 'SWOT分析',
      description: 'AI辅助生成企业或项目的优势、劣势、机会和威胁分析',
      features: ['智能评估', '竞对比较', '战略建议'],
      color: 'amber'
    },
    {
      icon: TrendingUp,
      title: '投资研究报告',
      description: '深度的行业研究和投资机会分析，支持投资决策',
      features: ['估值模型', '风险评估', '收益预测'],
      color: 'rose'
    }
  ];

  const reportFormats = [
    {
      icon: FileText,
      format: 'PDF',
      description: '专业排版，适合打印和分发',
      use: '正式汇报'
    },
    {
      icon: FileSpreadsheet,
      format: 'Excel',
      description: '数据表格，支持二次分析',
      use: '数据分析'
    },
    {
      icon: Presentation,
      format: 'PPT',
      description: '可视化呈现，用于演示',
      use: '会议演示'
    },
    {
      icon: BarChart3,
      format: 'HTML',
      description: '在线查看，交互式图表',
      use: '在线分享'
    }
  ];

  const reportFeatures = [
    {
      title: '结构化内容',
      description: '标准化的报告框架，包含执行摘要、详细分析、数据附录等完整章节，确保信息传达的专业性和完整性。'
    },
    {
      title: '数据可视化',
      description: '自动生成图表、趋势线、热力图等可视化元素，让复杂数据一目了然，提升报告的可读性和说服力。'
    },
    {
      title: 'AI智能撰写',
      description: '基于数据自动生成分析文本，包括关键发现、洞察总结和战略建议，节省大量人工撰写时间。'
    },
    {
      title: '定制化模板',
      description: '支持企业品牌定制，可设置公司logo、配色方案、报告样式，保持品牌调性的一致性。'
    },
    {
      title: '多语言支持',
      description: '一键生成中英文版本，适配国际化需求，AI自动翻译并调整语言表达习惯。'
    },
    {
      title: '版本管理',
      description: '自动保存历史版本，支持对比查看，追踪数据变化和分析演进过程。'
    }
  ];

  const useCases = [
    {
      scenario: '早会决策',
      time: '每日 08:00',
      content: '前一日行业动态摘要 + 关键数据变化 + 今日关注点'
    },
    {
      scenario: '周度复盘',
      time: '每周一 09:00',
      content: '本周重大事件回顾 + 市场趋势分析 + 下周展望'
    },
    {
      scenario: '月度汇报',
      time: '每月 1 日',
      content: '月度业绩总结 + KPI达成情况 + 问题与建议'
    },
    {
      scenario: '专题研究',
      time: '按需生成',
      content: '深度行业研究 + 竞品分析 + 战略建议'
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
        <div className="absolute inset-0 bg-gradient-to-b from-sky-500/10 via-transparent to-transparent"></div>
        <div className="absolute top-20 left-1/2 -translate-x-1/2 w-[600px] h-[600px] bg-sky-600/20 blur-[120px] rounded-full"></div>
        
        <div className="max-w-7xl mx-auto relative z-10">
          <Reveal>
            <div className="text-center mb-16">
              <div className="inline-flex items-center gap-3 px-4 py-2 rounded-full bg-sky-500/20 border border-sky-500/30 mb-6">
                <FileText className="w-5 h-5 text-sky-400" />
                <span className="text-sm font-medium text-sky-300">决策报告生成</span>
              </div>
              <h1 className="text-5xl md:text-6xl font-bold mb-6">
                <span className="gradient-text">所见即结论</span>
              </h1>
              <p className="text-xl text-slate-400 max-w-3xl mx-auto leading-relaxed">
                自动生成 PDF/HTML 格式的深度日报、周报。包含关键数据趋势图、<br />
                SWOT 分析初稿及 AI 辅助的战略建议，直接服务于您的早会决策。
              </p>
            </div>
          </Reveal>

          {/* Report Types */}
          <Reveal delay={0.2}>
            <div className="mb-20">
              <h2 className="text-3xl font-bold mb-12 text-center">
                <span className="gradient-text">报告类型</span>
              </h2>
              <div className="grid md:grid-cols-2 gap-6">
                {reportTypes.map((type, index) => {
                  const Icon = type.icon;
                  const colorClasses = {
                    sky: 'bg-sky-500/20 border-sky-500/30 text-sky-400',
                    purple: 'bg-purple-500/20 border-purple-500/30 text-purple-400',
                    amber: 'bg-amber-500/20 border-amber-500/30 text-amber-400',
                    rose: 'bg-rose-500/20 border-rose-500/30 text-rose-400'
                  }[type.color];

                  return (
                    <div key={index} className="glass rounded-2xl p-8 border border-slate-800 hover:border-slate-600 transition-all group">
                      <div className="flex items-start gap-4 mb-4">
                        <div className={`w-12 h-12 rounded-xl ${colorClasses} border flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-transform`}>
                          <Icon className="w-6 h-6" />
                        </div>
                        <div className="flex-1">
                          <h3 className="text-xl font-bold mb-2">{type.title}</h3>
                          <p className="text-slate-400 mb-4">{type.description}</p>
                          <div className="flex flex-wrap gap-2">
                            {type.features.map((feature, i) => (
                              <span key={i} className="px-3 py-1 rounded-full bg-slate-900 text-xs text-slate-300 border border-slate-800">
                                {feature}
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

          {/* Report Formats */}
          <Reveal delay={0.3}>
            <div className="mb-20">
              <h2 className="text-3xl font-bold mb-12 text-center">
                <span className="gradient-text">输出格式</span>
              </h2>
              <div className="grid md:grid-cols-4 gap-6">
                {reportFormats.map((format, index) => {
                  const Icon = format.icon;
                  return (
                    <div key={index} className="text-center glass rounded-2xl p-6 border border-slate-800 hover:border-sky-500/50 transition-all group">
                      <div className="w-16 h-16 mx-auto mb-4 rounded-xl bg-sky-500/20 border border-sky-500/30 flex items-center justify-center group-hover:scale-110 transition-transform">
                        <Icon className="w-8 h-8 text-sky-400" />
                      </div>
                      <h4 className="font-bold mb-2 text-lg">{format.format}</h4>
                      <p className="text-sm text-slate-400 mb-2">{format.description}</p>
                      <div className="text-xs text-slate-500">{format.use}</div>
                    </div>
                  );
                })}
              </div>
            </div>
          </Reveal>

          {/* Features Grid */}
          <Reveal delay={0.4}>
            <div className="mb-20">
              <h2 className="text-3xl font-bold mb-12 text-center">
                <span className="gradient-text">核心功能</span>
              </h2>
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                {reportFeatures.map((feature, index) => (
                  <div key={index} className="glass rounded-2xl p-6 border border-slate-800 hover:border-sky-500/50 transition-all">
                    <div className="flex items-start gap-3 mb-3">
                      <CheckCircle2 className="w-5 h-5 text-sky-400 flex-shrink-0 mt-0.5" />
                      <h3 className="font-bold text-lg">{feature.title}</h3>
                    </div>
                    <p className="text-slate-400 text-sm leading-relaxed">{feature.description}</p>
                  </div>
                ))}
              </div>
            </div>
          </Reveal>

          {/* Use Cases */}
          <Reveal delay={0.5}>
            <div className="mb-20">
              <h2 className="text-3xl font-bold mb-12 text-center">
                <span className="gradient-text">典型应用场景</span>
              </h2>
              <div className="glass rounded-2xl p-8 border border-slate-800">
                <div className="grid md:grid-cols-2 gap-6">
                  {useCases.map((useCase, index) => (
                    <div key={index} className="flex items-start gap-4 p-6 rounded-xl bg-slate-950/50 border border-slate-800">
                      <div className="flex-shrink-0">
                        <Calendar className="w-6 h-6 text-sky-400" />
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center justify-between mb-2">
                          <h4 className="font-bold">{useCase.scenario}</h4>
                          <span className="text-xs text-slate-500 font-mono">{useCase.time}</span>
                        </div>
                        <p className="text-sm text-slate-400">{useCase.content}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </Reveal>

          {/* CTA */}
          <Reveal delay={0.6}>
            <div className="text-center glass rounded-2xl p-12 border border-slate-800">
              <h3 className="text-3xl font-bold mb-4">
                <span className="gradient-text">让AI成为您的分析师</span>
              </h3>
              <p className="text-lg text-slate-400 mb-8 max-w-2xl mx-auto">
                每天早上醒来，专业报告已经准备就绪，直接用于决策
              </p>
              <div className="flex flex-col sm:flex-row gap-4 items-center justify-center">
                <Link 
                  to="/reports"
                  className="inline-flex items-center gap-2 px-8 py-4 bg-white text-black rounded-full font-semibold text-lg hover:bg-slate-200 transition-all"
                >
                  <Download className="w-5 h-5" />
                  查看报告样本
                </Link>
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
