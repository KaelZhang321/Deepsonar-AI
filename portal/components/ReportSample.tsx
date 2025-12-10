import React from 'react';
import { ArrowLeft, Download, FileText, Calendar, Building2, TrendingUp, Eye } from 'lucide-react';
import { Link } from 'react-router-dom';
import { Reveal } from './ui/Reveal';

export const ReportSample: React.FC = () => {
  const sampleReports = [
    {
      id: 1,
      title: '新能源汽车行业深度分析报告',
      date: '2024年11月',
      company: '某科技集团',
      category: '行业研究',
      pages: 68,
      highlights: [
        '市场规模达到1.2万亿元，同比增长42%',
        '头部企业市占率提升至65%',
        '技术创新推动成本下降18%',
        '预计未来3年复合增长率35%'
      ],
      previewUrl: '/file/NEV_Industry_Analysis.html',
      downloadUrl: '/doc/NEV_Industry_Analysis.pdf'
    },
    {
      id: 2,
      title: '人工智能赛道投资机会分析',
      date: '2024年10月',
      company: '某投资机构',
      category: '投资分析',
      pages: 52,
      highlights: [
        'AI芯片市场年增长率达58%',
        '大模型应用场景快速拓展',
        '投资回报率平均提升23%',
        '重点关注垂直领域应用'
      ],
      previewUrl: '/file/AI_Investment_Dashboard.html',
      downloadUrl: '/doc/AI_Investment_Dashboard.pdf'
    },
    {
      id: 3,
      title: '生物医药创新企业竞争力研究',
      date: '2024年9月',
      company: '某医药集团',
      category: '竞争分析',
      pages: 75,
      highlights: [
        'R&D投入占比达15-20%',
        '创新药管线平均8-12个',
        '临床成功率提升至28%',
        '国际化布局加速推进'
      ],
      previewUrl: '/file/Biopharma_Competitiveness_Report.html',
      downloadUrl: '/doc/Biopharma_Competitiveness_Report.pdf'
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
          <h1 className="text-sm font-semibold text-white/50">报告样本</h1>
        </div>
      </div>

      {/* Main Content */}
      <div className="pt-32 pb-20 px-6">
        <div className="max-w-7xl mx-auto">
          {/* Page Title */}
          <Reveal>
            <div className="text-center mb-16">
              <h2 className="text-4xl md:text-5xl font-bold mb-4">
                <span className="gradient-text">深度研报样本展示</span>
              </h2>
              <p className="text-lg text-slate-400 max-w-2xl mx-auto">
                基于全网数据采集与AI深度分析，为您提供专业、全面的行业洞察报告
              </p>
            </div>
          </Reveal>

          {/* Reports Grid */}
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {sampleReports.map((report, index) => (
              <Reveal key={report.id} delay={0.1 * index}>
                <div className="glass rounded-2xl p-6 border border-slate-800 hover:border-brand-accent/50 transition-all group">
                  {/* Report Header */}
                  <div className="flex items-start justify-between mb-4">
                    <div className="p-3 rounded-lg bg-brand-accent/10 border border-brand-accent/30">
                      <FileText className="w-6 h-6 text-brand-accent" />
                    </div>
                    <span className="px-3 py-1 rounded-full bg-slate-800 text-xs font-medium text-slate-300 border border-slate-700">
                      {report.category}
                    </span>
                  </div>

                  {/* Report Title */}
                  <h3 className="text-xl font-bold mb-3 text-white group-hover:text-brand-accent transition-colors">
                    {report.title}
                  </h3>

                  {/* Meta Info */}
                  <div className="space-y-2 mb-4 text-sm text-slate-400">
                    <div className="flex items-center gap-2">
                      <Building2 className="w-4 h-4" />
                      <span>{report.company}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Calendar className="w-4 h-4" />
                      <span>{report.date}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <FileText className="w-4 h-4" />
                      <span>{report.pages} 页</span>
                    </div>
                  </div>

                  {/* Highlights */}
                  <div className="mb-6">
                    <div className="flex items-center gap-2 mb-3">
                      <TrendingUp className="w-4 h-4 text-brand-accent" />
                      <span className="text-sm font-semibold text-slate-300">核心亮点</span>
                    </div>
                    <ul className="space-y-2">
                      {report.highlights.map((highlight, i) => (
                        <li key={i} className="text-sm text-slate-400 flex items-start gap-2">
                          <span className="text-brand-accent mt-1">•</span>
                          <span>{highlight}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  {/* Action Buttons */}
                  <div className="flex gap-3">
                    <a 
                      href={report.downloadUrl}
                      download={report.downloadUrl.split('/').pop()}
                      className="flex-1 flex items-center justify-center gap-2 px-4 py-3 rounded-lg border border-slate-700 hover:bg-slate-800 hover:border-slate-600 transition-all group/btn"
                    >
                      <Download className="w-4 h-4 text-slate-400 group-hover/btn:text-white transition-colors" />
                      <span className="text-sm font-medium text-slate-300 group-hover/btn:text-white">下载</span>
                    </a>
                    <a 
                      href={report.previewUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex-1 flex items-center justify-center gap-2 px-4 py-3 rounded-lg bg-slate-800 hover:bg-slate-700 hover:text-brand-accent transition-all group/btn"
                    >
                      <Eye className="w-4 h-4 group-hover/btn:text-brand-accent transition-colors" />
                      <span className="text-sm font-medium">查看</span>
                    </a>
                  </div>
                </div>
              </Reveal>
            ))}
          </div>

          {/* CTA Section */}
          <Reveal delay={0.4}>
            <div className="mt-20 text-center glass rounded-2xl p-12 border border-slate-800">
              <h3 className="text-3xl font-bold mb-4">
                <span className="gradient-text">需要定制化深度研报？</span>
              </h3>
              <p className="text-lg text-slate-400 mb-8 max-w-2xl mx-auto">
                我们的AI团队可以根据您的具体需求，为您量身打造专业的行业分析报告
              </p>
              <div className="flex flex-col sm:flex-row gap-4 items-center justify-center">
                <button className="px-8 py-4 bg-white text-black rounded-full font-semibold text-lg hover:bg-slate-200 transition-all">
                  联系我们
                </button>
                <Link 
                  to="/"
                  className="px-8 py-4 rounded-full border border-slate-700 text-slate-300 font-semibold text-lg hover:bg-slate-800 hover:border-slate-600 transition-all"
                >
                  了解更多
                </Link>
              </div>
            </div>
          </Reveal>
        </div>
      </div>
    </div>
  );
};
