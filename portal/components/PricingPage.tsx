import React, { useState } from 'react';
import { ArrowLeft, Check, Sparkles, Zap, Crown, ArrowRight, HelpCircle, Plus } from 'lucide-react';
import { Link } from 'react-router-dom';
import { Reveal } from './ui/Reveal';

export const PricingPage: React.FC = () => {
  const [billingCycle, setBillingCycle] = useState<'monthly' | 'yearly'>('monthly');

  const pricingPlans = [
    {
      name: 'Starter',
      nameCN: '入门版',
      subtitle: '为个人创作者和自由职业者打造',
      icon: Sparkles,
      price: { monthly: 999, yearly: 9990 },
      features: [
        '10个数据源监控',
        '每日简报生成',
        '7天数据回溯',
        '基础市场情绪分析',
        'Web端访问',
      ],
      highlight: false,
      color: 'blue',
    },
    {
      name: 'Pro',
      nameCN: '专业版',
      subtitle: '快速成长的初创团队的最佳选择',
      icon: Zap,
      price: { monthly: 2999, yearly: 29990 },
      features: [
        '50个数据源监控',
        '每日日报 + 每周深度周报',
        '30天数据回溯',
        'AI 深度关联分析',
        '多渠道推送 (Email, Slack)',
        'API 访问权限 (10k/月)',
        '优先邮件支持',
        '自定义报告模板',
      ],
      highlight: true,
      popular: true,
      color: 'indigo',
    },
    {
      name: 'Enterprise',
      nameCN: '企业版',
      subtitle: '针对大型组织的全方位定制方案',
      icon: Crown,
      price: { monthly: 9999, yearly: 99990 },
      features: [
        '无限数据源监控',
        '全类型报告 (含战略咨询)',
        '永久数据保存',
        '私有化模型微调',
        '全渠道推送 + 专属 webhook',
        '无限 API 访问',
        '1v1 专属客户经理',
        '私有化部署支持',
        'SSO 单点登录',
      ],
      highlight: false,
      color: 'amber',
    },
  ];

  const addons = [
    { title: '额外数据源包', price: '¥100', unit: '/月/个', description: '突破套餐限制，按需扩展监控范围' },
    { title: '存储扩容包', price: '¥50', unit: '/月/10GB', description: '为您的海量历史数据提供更多空间' },
    { title: '高频 API 包', price: '¥199', unit: '/月/10k次', description: '满足高频次数据调用需求' },
    { title: '定制功能开发', price: '定制', unit: '', description: '专属需求分析与功能落地服务' },
  ];

  const faqs = [
    { question: '如何确定哪个套餐最适合我？', answer: '这主要取决于您的团队规模和监控需求。如果您是个人使用，入门版足矣；如果您是成长型团队，需要深度分析和API，专业版性价比最高；对于有复杂定制和安全需求的大型企业，企业版是不二之选。' },
    { question: '我可以随时更改套餐吗？', answer: '没问题。您可以随时升级您的套餐，差价将按比例折算。如果您选择降级，更改将在当前计费周期结束后生效。' },
    { question: '年付套餐具体能省多少？', answer: '选择年付方案，您将获得约 17% 的折扣，这相当于免费使用了 两个月 的服务。对于长期使用的用户来说非常划算。' },
    { question: '试用期结束后会发生什么？', answer: '14天免费试用结束后，如果您未绑定支付方式，您的账户将自动降级为免费受限版本。您的数据会保留30天，期间您可以随时订阅付费套餐恢复完整功能。' },
    { question: '数据安全得到保障了吗？', answer: '绝对安全。DeepSonar 采用企业级加密标准 (AES-256) 存储您的数据，并严格遵守 GDPR 等隐私法规。您的数据完全属于您，我们绝不会将其用于其他商业用途。' },
  ];

  return (
    <div className="min-h-screen bg-brand-dark text-white overflow-hidden relative selection:bg-brand-accent/30">
      {/* Background */}
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute top-[-10%] left-[-10%] w-[1000px] h-[1000px] bg-indigo-600/10 blur-[150px] rounded-full mix-blend-screen opacity-30 animate-pulse-slow" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[800px] h-[800px] bg-sky-600/10 blur-[150px] rounded-full mix-blend-screen opacity-20 animate-pulse-slow delay-1000" />
        <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20 brightness-100 contrast-150" />
      </div>

      {/* Header */}
      <div className="fixed top-0 w-full z-50 border-b border-white/5 bg-black/50 backdrop-blur-xl supports-[backdrop-filter]:bg-black/20">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center gap-4">
          <Link to="/" className="flex items-center gap-2 text-slate-400 hover:text-white transition-colors group text-sm font-medium">
            <ArrowLeft className="w-4 h-4 group-hover:-translate-x-1 transition-transform" />
            <span>返回首页</span>
          </Link>
        </div>
      </div>

      <div className="relative z-10 pt-40 pb-32 px-6">
        <div className="max-w-5xl mx-auto">
          {/* Hero */}
          <Reveal>
            <div className="text-center mb-20">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 text-xs font-semibold mb-6 tracking-wide uppercase">
                Pricing Plans
              </div>
              <h1 className="text-5xl md:text-7xl font-bold mb-8 tracking-tight">
                <span className="bg-clip-text text-transparent bg-gradient-to-b from-white via-white to-slate-500">
                  选择适合您的
                </span>
                <br />
                <span className="bg-clip-text text-transparent bg-gradient-to-r from-indigo-400 to-sky-400">
                  智能情报引擎
                </span>
              </h1>
              <p className="text-xl text-slate-400 max-w-2xl mx-auto leading-relaxed font-light">
                无论是个人探索还是企业决策，DeepSonar 都能为您提供最具价值的市场洞察。无隐藏费用，透明定价。
              </p>
            </div>
          </Reveal>

          {/* Billing Switch */}
          <Reveal delay={0.2} overflow="visible">
            <div className="flex justify-center mb-24">
              <div className="relative inline-flex bg-slate-900/50 p-1.5 rounded-full border border-white/10 backdrop-blur-sm">
                <div
                  className={`absolute top-1.5 bottom-1.5 rounded-full bg-indigo-600 shadow-lg shadow-indigo-900/50 transition-all duration-500 ease-out z-0 ${
                    billingCycle === 'monthly' ? 'left-1.5 w-[100px]' : 'left-[106px] w-[100px]'
                  }`}
                />
                <button
                  onClick={() => setBillingCycle('monthly')}
                  className={`relative z-10 px-6 py-2 rounded-full text-sm font-semibold transition-colors duration-300 w-[100px] text-center ${
                    billingCycle === 'monthly' ? 'text-white' : 'text-slate-400 hover:text-white'
                  }`}
                >
                  月付
                </button>
                <button
                  onClick={() => setBillingCycle('yearly')}
                  className={`relative z-10 px-6 py-2 rounded-full text-sm font-semibold transition-colors duration-300 w-[100px] text-center flex items-center justify-center gap-1 ${
                    billingCycle === 'yearly' ? 'text-white' : 'text-slate-400 hover:text-white'
                  }`}
                >
                  年付
                </button>
                <div className="absolute -top-3 -right-12 px-2.5 py-0.5 bg-emerald-500 text-black text-[10px] font-bold rounded-full transform rotate-6 border border-emerald-400 shadow-[0_0_10px_rgba(16,185,129,0.4)]">
                  省 17%
                </div>
              </div>
            </div>
          </Reveal>

          {/* Pricing Cards */}
          <div className="grid md:grid-cols-3 gap-8 items-start mb-32">
            {pricingPlans.map((plan, index) => {
              const Icon = plan.icon;
              const price = billingCycle === 'monthly' ? plan.price.monthly : plan.price.yearly;
              const period = billingCycle === 'monthly' ? '/月' : '/年';
              const isPopular = !!plan.popular;
              return (
                <Reveal key={index} delay={index * 0.1} overflow="visible">
                  <div className={`relative group transition-all duration-300 ${isPopular ? '-mt-4' : ''}`}>
                    {isPopular && (
                      <div className="absolute -inset-[1px] bg-gradient-to-b from-indigo-500 to-sky-500 rounded-[22px] opacity-100 blur-[1px]" />
                    )}
                    {isPopular && (
                      <div className="absolute -inset-4 bg-indigo-500/20 rounded-[30px] opacity-0 group-hover:opacity-100 blur-xl transition-opacity duration-700" />
                    )}
                    <div className={`relative h-full bg-[#0a0a0a]/90 backdrop-blur-xl border ${isPopular ? 'border-transparent' : 'border-white/10 hover:border-white/20'} rounded-2xl p-8 flex flex-col`}>
                      {isPopular && (
                        <div className="absolute top-0 left-1/2 -translate-x-1/2 -translate-y-1/2 px-4 py-1 bg-gradient-to-r from-indigo-500 to-sky-500 text-white text-xs font-bold rounded-full shadow-lg shadow-indigo-900/50 uppercase tracking-wider">
                          Most Popular
                        </div>
                      )}
                      <div className="mb-8">
                        <div className={`w-12 h-12 rounded-xl mb-6 flex items-center justify-center ${
                          isPopular ? 'bg-gradient-to-br from-indigo-500/20 to-sky-500/20 text-indigo-400' : 'bg-slate-800/50 text-slate-400'
                        }`}>
                          <Icon className="w-6 h-6" />
                        </div>
                        <h3 className="text-2xl font-bold flex items-center gap-2 mb-2">
                          {plan.name} <span className="text-lg font-normal text-slate-500">| {plan.nameCN}</span>
                        </h3>
                        <p className="text-sm text-slate-400 h-10">{plan.subtitle}</p>
                      </div>
                      <div className="mb-8 p-4 rounded-xl bg-white/5 border border-white/5">
                        <div className="flex items-baseline gap-1">
                          <span className="text-4xl font-bold tracking-tight">¥{price.toLocaleString()}</span>
                          <span className="text-sm text-slate-500 font-medium">{period}</span>
                        </div>
                        {billingCycle === 'yearly' && (
                          <div className="mt-1 text-xs text-emerald-400 font-medium flex items-center gap-1">
                            <Check className="w-3 h-3" /> 年付立省 ¥{Math.round(price * 0.17).toLocaleString()}
                          </div>
                        )}
                      </div>
                      <div className="flex-1">
                        <div className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-4">Features</div>
                        <ul className="space-y-4 mb-8">
                          {plan.features.map((feature, i) => (
                            <li key={i} className="flex items-start gap-3 text-sm text-slate-300">
                              <Check className={`w-4 h-4 flex-shrink-0 mt-0.5 ${isPopular ? 'text-indigo-400' : 'text-slate-500'}`} />
                              <span>{feature}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                      <button
                        className={`w-full py-4 rounded-xl font-bold transition-all flex items-center justify-center gap-2 group/btn ${
                          isPopular ? 'bg-white text-black hover:bg-indigo-50' : 'bg-white/10 text-white hover:bg-white/20'
                        }`}
                      >
                        开始使用
                        <ArrowRight className="w-4 h-4 group-hover/btn:translate-x-1 transition-transform" />
                      </button>
                    </div>
                  </div>
                </Reveal>
              );
            })}
          </div>

          {/* Add‑ons Section */}
          <Reveal delay={0.4}>
            <section className="mb-32">
              <div className="text-center mb-16">
                <h2 className="text-3xl font-bold mb-4">增值服务</h2>
                <p className="text-slate-400">为特别需求准备的灵活性扩展</p>
              </div>
              <div className="max-w-5xl mx-auto flex justify-center">
                <div className="grid md:grid-cols-4 gap-6 w-full justify-items-center">
                  {addons.map((addon, index) => (
                    <div
                      key={index}
                      className="group relative bg-white/[0.02] border border-white/10 hover:border-indigo-500/30 rounded-2xl p-6 text-center transition-all duration-300 hover:-translate-y-1 hover:bg-white/[0.04] w-full flex flex-col items-center"
                    >
                      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-16 h-[1px] bg-gradient-to-r from-transparent via-indigo-500/50 to-transparent group-hover:via-indigo-400 transition-colors" />
                      <div className="w-10 h-10 mx-auto rounded-full bg-slate-900 border border-white/10 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform text-slate-400 group-hover:text-indigo-400">
                        <Plus className="w-5 h-5" />
                      </div>
                      <h4 className="font-bold mb-2 text-slate-200">{addon.title}</h4>
                      <div className="mb-3 flex items-baseline justify-center gap-[2px]">
                        <span className="text-xl font-bold text-indigo-400">{addon.price}</span>
                        <span className="text-xs text-slate-500">{addon.unit}</span>
                      </div>
                      <p className="text-xs text-slate-500 leading-relaxed group-hover:text-slate-400 transition-colors">{addon.description}</p>
                    </div>
                  ))}
                </div>
              </div>
            </section>
          </Reveal>

          {/* FAQ Section */}
          <Reveal delay={0.5}>
            <section className="mb-32">
              <div className="max-w-5xl mx-auto text-center mb-12">
                <div className="w-12 h-12 mx-auto rounded-xl bg-slate-900 border border-white/10 flex items-center justify-center mb-6 text-slate-400">
                  <HelpCircle className="w-6 h-6" />
                </div>
                <h2 className="text-3xl font-bold mb-4">常见问题</h2>
                <p className="text-slate-400">这里有您可能关心的问题的所有答案</p>
              </div>
              <div className="space-y-4">
                {faqs.map((faq, index) => (
                  <details key={index} className="group bg-white/[0.02] border border-white/5 hover:border-white/10 rounded-2xl overflow-hidden transition-all duration-300 open:bg-white/[0.04] open:border-indigo-500/20" id={`faq-${index}`}>
                    <summary className="px-8 py-6 font-medium cursor-pointer flex items-center justify-center gap-4 text-slate-300 hover:text-white transition-colors select-none text-center relative">
                      <span className="text-lg">{faq.question}</span>
                      <div className="absolute right-8 top-1/2 -translate-y-1/2 w-8 h-8 rounded-full bg-white/5 flex items-center justify-center group-hover:bg-white/10 transition-colors">
                        <ArrowRight className="w-4 h-4 group-open:rotate-90 transition-transform duration-300 text-slate-500 group-open:text-indigo-400" />
                      </div>
                    </summary>
                    <div className="px-8 pb-8 pt-0 text-slate-400 leading-relaxed text-center border-t border-transparent group-open:border-white/5 group-open:pt-6 animate-in fade-in slide-in-from-top-2 duration-300 max-w-2xl mx-auto">
                      {faq.answer}
                    </div>
                  </details>
                ))}
              </div>
            </section>
          </Reveal>

          {/* Bottom CTA */}
          <Reveal delay={0.6}>
            <div className="mt-32 text-center pb-20">
              <p className="text-slate-500 mb-6 font-medium">还没有准备好付费？</p>
              <Link to="/" className="inline-flex items-center gap-2 text-indigo-400 hover:text-indigo-300 transition-colors border-b border-indigo-500/30 hover:border-indigo-400 pb-0.5">
                联系我们的销售团队进行咨询 <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
          </Reveal>
        </div>
      </div>
    </div>
  );
};
