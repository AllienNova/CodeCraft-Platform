import React, { useState } from 'react';

const Pricing = () => {
  const [billingCycle, setBillingCycle] = useState('monthly');
  const [selectedPlan, setSelectedPlan] = useState('family');

  const plans = {
    monthly: [
      {
        id: 'starter',
        name: 'Starter',
        price: 19,
        description: 'Perfect for one child exploring coding',
        features: [
          '1 child account',
          'Access to age-appropriate tier',
          'Basic progress tracking',
          'Email support',
          'Mobile app access',
          'Basic parental dashboard'
        ],
        popular: false,
        cta: 'Start Free Trial'
      },
      {
        id: 'family',
        name: 'Family',
        price: 29,
        originalPrice: 57,
        description: 'Ideal for families with multiple children',
        features: [
          'Up to 3 child accounts',
          'All learning tiers included',
          'Advanced progress analytics',
          'Priority support',
          'Mobile + web access',
          'Comprehensive parental dashboard',
          'Sibling collaboration features',
          'Family achievement tracking'
        ],
        popular: true,
        cta: 'Start Free Trial',
        savings: 'Save $28/month'
      },
      {
        id: 'premium',
        name: 'Premium',
        price: 49,
        originalPrice: 87,
        description: 'Complete coding education experience',
        features: [
          'Up to 5 child accounts',
          'All learning tiers + advanced modules',
          'Real-time progress monitoring',
          'Dedicated support + live chat',
          'All platform access',
          'Advanced parental controls',
          'Custom learning paths',
          'One-on-one mentoring sessions',
          'Early access to new features',
          'Certification programs'
        ],
        popular: false,
        cta: 'Start Free Trial',
        savings: 'Save $38/month'
      }
    ],
    yearly: [
      {
        id: 'starter',
        name: 'Starter',
        price: 15,
        originalPrice: 19,
        yearlyPrice: 180,
        description: 'Perfect for one child exploring coding',
        features: [
          '1 child account',
          'Access to age-appropriate tier',
          'Basic progress tracking',
          'Email support',
          'Mobile app access',
          'Basic parental dashboard'
        ],
        popular: false,
        cta: 'Start Free Trial',
        savings: 'Save $48/year'
      },
      {
        id: 'family',
        name: 'Family',
        price: 22,
        originalPrice: 29,
        yearlyPrice: 264,
        description: 'Ideal for families with multiple children',
        features: [
          'Up to 3 child accounts',
          'All learning tiers included',
          'Advanced progress analytics',
          'Priority support',
          'Mobile + web access',
          'Comprehensive parental dashboard',
          'Sibling collaboration features',
          'Family achievement tracking'
        ],
        popular: true,
        cta: 'Start Free Trial',
        savings: 'Save $84/year'
      },
      {
        id: 'premium',
        name: 'Premium',
        price: 37,
        originalPrice: 49,
        yearlyPrice: 444,
        description: 'Complete coding education experience',
        features: [
          'Up to 5 child accounts',
          'All learning tiers + advanced modules',
          'Real-time progress monitoring',
          'Dedicated support + live chat',
          'All platform access',
          'Advanced parental controls',
          'Custom learning paths',
          'One-on-one mentoring sessions',
          'Early access to new features',
          'Certification programs'
        ],
        popular: false,
        cta: 'Start Free Trial',
        savings: 'Save $144/year'
      }
    ]
  };

  const currentPlans = plans[billingCycle];

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-blue-50 to-indigo-100">
      {/* Hero Section */}
      <section className="pt-20 pb-16 px-4">
        <div className="max-w-6xl mx-auto text-center">
          <h1 className="text-5xl md:text-6xl font-bold mb-6">
            <span className="bg-gradient-to-r from-purple-600 via-blue-600 to-indigo-600 bg-clip-text text-transparent">
              Simple, Transparent Pricing
            </span>
          </h1>
          <p className="text-xl text-gray-700 max-w-3xl mx-auto leading-relaxed mb-8">
            Choose the perfect plan for your family. All plans include a 7-day free trial 
            and can be cancelled anytime.
          </p>
          
          {/* Billing Toggle */}
          <div className="flex items-center justify-center mb-12">
            <span className={`mr-4 ${billingCycle === 'monthly' ? 'text-purple-600 font-semibold' : 'text-gray-600'}`}>
              Monthly
            </span>
            <button
              onClick={() => setBillingCycle(billingCycle === 'monthly' ? 'yearly' : 'monthly')}
              className="relative w-16 h-8 bg-gray-300 rounded-full transition-colors focus:outline-none"
            >
              <div className={`absolute top-1 left-1 w-6 h-6 bg-white rounded-full transition-transform ${
                billingCycle === 'yearly' ? 'transform translate-x-8 bg-purple-600' : ''
              }`}></div>
            </button>
            <span className={`ml-4 ${billingCycle === 'yearly' ? 'text-purple-600 font-semibold' : 'text-gray-600'}`}>
              Yearly
            </span>
            {billingCycle === 'yearly' && (
              <span className="ml-3 bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-semibold">
                Save up to 25%
              </span>
            )}
          </div>
        </div>
      </section>

      {/* Pricing Cards */}
      <section className="py-16 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="grid md:grid-cols-3 gap-8">
            {currentPlans.map((plan) => (
              <div
                key={plan.id}
                className={`relative bg-white rounded-2xl shadow-lg hover:shadow-xl transition-all transform hover:scale-105 ${
                  plan.popular ? 'ring-4 ring-purple-500 ring-opacity-50' : ''
                }`}
              >
                {plan.popular && (
                  <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                    <span className="bg-gradient-to-r from-purple-600 to-blue-600 text-white px-6 py-2 rounded-full text-sm font-semibold">
                      Most Popular
                    </span>
                  </div>
                )}
                
                <div className="p-8">
                  <h3 className="text-2xl font-bold text-gray-800 mb-2">{plan.name}</h3>
                  <p className="text-gray-600 mb-6">{plan.description}</p>
                  
                  <div className="mb-6">
                    <div className="flex items-baseline">
                      <span className="text-4xl font-bold text-gray-800">${plan.price}</span>
                      <span className="text-gray-600 ml-2">
                        /{billingCycle === 'monthly' ? 'month' : 'month'}
                      </span>
                    </div>
                    {plan.originalPrice && (
                      <div className="flex items-center mt-2">
                        <span className="text-lg text-gray-400 line-through mr-2">
                          ${plan.originalPrice}/month
                        </span>
                        <span className="text-green-600 font-semibold text-sm">
                          {plan.savings}
                        </span>
                      </div>
                    )}
                    {billingCycle === 'yearly' && (
                      <p className="text-sm text-gray-600 mt-2">
                        Billed annually (${plan.yearlyPrice}/year)
                      </p>
                    )}
                  </div>

                  <button
                    className={`w-full py-3 px-6 rounded-lg font-semibold transition-all mb-6 ${
                      plan.popular
                        ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white hover:shadow-lg'
                        : 'bg-gray-100 text-gray-800 hover:bg-gray-200'
                    }`}
                  >
                    {plan.cta}
                  </button>

                  <ul className="space-y-3">
                    {plan.features.map((feature, index) => (
                      <li key={index} className="flex items-center text-gray-700">
                        <span className="w-5 h-5 bg-green-100 rounded-full flex items-center justify-center mr-3 flex-shrink-0">
                          <span className="text-green-600 text-sm">✓</span>
                        </span>
                        {feature}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Value Proposition */}
      <section className="py-16 px-4 bg-white">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-12">
            <span className="bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
              Why CodeCraft is Worth Every Penny
            </span>
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-gradient-to-r from-green-500 to-emerald-500 rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-2xl text-white">💰</span>
              </div>
              <h3 className="text-xl font-bold text-gray-800 mb-4">Future Career Investment</h3>
              <p className="text-gray-600">
                Average software developer salary: $107,000+. Your investment today could lead to 
                a lifetime of high-earning potential.
              </p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-2xl text-white">⏰</span>
              </div>
              <h3 className="text-xl font-bold text-gray-800 mb-4">Time-Efficient Learning</h3>
              <p className="text-gray-600">
                Children learn 3x faster with CodeCraft compared to traditional methods. 
                More progress in less time.
              </p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center mx-auto mb-6">
                <span className="text-2xl text-white">🎯</span>
              </div>
              <h3 className="text-xl font-bold text-gray-800 mb-4">Comprehensive Solution</h3>
              <p className="text-gray-600">
                Replace multiple coding apps and tutoring sessions with one comprehensive platform 
                that grows with your child.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="py-16 px-4">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-12">
            <span className="bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
              Frequently Asked Questions
            </span>
          </h2>
          <div className="space-y-6">
            <div className="bg-white rounded-2xl p-6 shadow-lg">
              <h3 className="text-xl font-bold text-gray-800 mb-3">Can I change plans anytime?</h3>
              <p className="text-gray-600">
                Yes! You can upgrade, downgrade, or cancel your plan at any time. Changes take effect 
                immediately, and we'll prorate any billing adjustments.
              </p>
            </div>
            <div className="bg-white rounded-2xl p-6 shadow-lg">
              <h3 className="text-xl font-bold text-gray-800 mb-3">What happens after the free trial?</h3>
              <p className="text-gray-600">
                Your 7-day free trial gives you full access to all features. After the trial, you'll be 
                charged for your selected plan. You can cancel anytime during the trial with no charges.
              </p>
            </div>
            <div className="bg-white rounded-2xl p-6 shadow-lg">
              <h3 className="text-xl font-bold text-gray-800 mb-3">Is there a family discount?</h3>
              <p className="text-gray-600">
                Our Family and Premium plans already include significant discounts for multiple children. 
                The Family plan saves you $28/month compared to individual accounts.
              </p>
            </div>
            <div className="bg-white rounded-2xl p-6 shadow-lg">
              <h3 className="text-xl font-bold text-gray-800 mb-3">Do you offer refunds?</h3>
              <p className="text-gray-600">
                We offer a 30-day money-back guarantee. If you're not completely satisfied with CodeCraft, 
                we'll refund your payment, no questions asked.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Enterprise Section */}
      <section className="py-16 px-4 bg-gradient-to-r from-gray-800 to-gray-900">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl font-bold text-white mb-6">Enterprise & Schools</h2>
          <p className="text-xl text-gray-300 mb-8">
            Looking for a solution for your school, district, or organization? 
            We offer custom enterprise plans with volume discounts and additional features.
          </p>
          <div className="grid md:grid-cols-3 gap-6 mb-8">
            <div className="text-center">
              <span className="text-3xl mb-2 block">🏫</span>
              <h3 className="text-lg font-semibold text-white mb-2">Schools & Districts</h3>
              <p className="text-gray-400">Classroom management and curriculum integration</p>
            </div>
            <div className="text-center">
              <span className="text-3xl mb-2 block">👥</span>
              <h3 className="text-lg font-semibold text-white mb-2">Volume Licensing</h3>
              <p className="text-gray-400">Significant discounts for 50+ students</p>
            </div>
            <div className="text-center">
              <span className="text-3xl mb-2 block">📊</span>
              <h3 className="text-lg font-semibold text-white mb-2">Advanced Analytics</h3>
              <p className="text-gray-400">Detailed progress tracking and reporting</p>
            </div>
          </div>
          <button className="bg-white text-gray-800 px-8 py-4 rounded-full text-lg font-semibold hover:shadow-lg transition-all">
            Contact Sales Team
          </button>
        </div>
      </section>

      {/* Final CTA */}
      <section className="py-16 px-4 bg-gradient-to-r from-purple-600 to-blue-600">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl font-bold text-white mb-6">
            Start Your Child's Coding Journey Today
          </h2>
          <p className="text-xl text-purple-100 mb-8">
            Join 2,847+ families who've chosen CodeCraft for their children's future.
          </p>
          <button className="bg-white text-purple-600 px-8 py-4 rounded-full text-lg font-semibold hover:shadow-lg transition-all transform hover:scale-105 mr-4">
            Start FREE 7-Day Trial
          </button>
          <button className="border-2 border-white text-white px-8 py-4 rounded-full text-lg font-semibold hover:bg-white hover:text-purple-600 transition-all">
            View Demo
          </button>
          <p className="text-purple-200 mt-6">
            ✓ No Credit Card Required ✓ COPPA Compliant ✓ Cancel Anytime
          </p>
        </div>
      </section>
    </div>
  );
};

export default Pricing;

