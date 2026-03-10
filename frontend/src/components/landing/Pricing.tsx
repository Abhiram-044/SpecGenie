"use client";

import React, { useState } from "react";
import { Check, X } from "lucide-react";

interface PricingFeatureProps {
  included: boolean;
  text: string;
  highlight?: boolean;
}

const PricingFeature: React.FC<PricingFeatureProps> = ({
  included,
  text,
  highlight = false,
}) => {
  return (
    <li className="flex items-start">
      <div
        className={`flex-shrink-0 h-5 w-5 rounded-full flex items-center justify-center mt-0.5 ${
          included
            ? highlight
              ? "bg-indigo-500/20 text-indigo-400"
              : "bg-gray-800 text-gray-400"
            : "bg-gray-800/50 text-gray-600"
        }`}
      >
        {included ? <Check className="h-3 w-3" /> : <X className="h-3 w-3" />}
      </div>

      <span className={`ml-3 ${included ? "text-gray-300" : "text-gray-500"}`}>
        {text}
      </span>
    </li>
  );
};

const Pricing: React.FC = () => {
  const [isAnnual, setIsAnnual] = useState<boolean>(false);

  return (
    <section id="pricing" className="py-20 md:py-32 relative overflow-hidden">
      {/* Background */}
      <div className="absolute inset-0 bg-gradient-to-b from-gray-950 to-gray-900 z-0" />
      <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-indigo-500/50 to-transparent" />

      <div className="container mx-auto px-4 md:px-6 relative z-10">
        {/* Header */}
        <div className="text-center mb-16">
          <div className="inline-block px-3 py-1 mb-6 rounded-full bg-gray-800 border border-gray-700">
            <span className="text-sm font-medium text-indigo-400">
              Affordable Plans
            </span>
          </div>

          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Choose the Perfect Plan for Your Needs
          </h2>

          <p className="text-xl text-gray-400 max-w-3xl mx-auto">
            Whether you're just starting your job search or applying to multiple
            positions, we have a plan that fits your needs.
          </p>

          {/* Toggle */}
          <div className="mt-8 inline-flex items-center bg-gray-800 p-1 rounded-full">
            <button
              className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${
                !isAnnual
                  ? "bg-indigo-600 text-white"
                  : "text-gray-400 hover:text-white"
              }`}
              onClick={() => setIsAnnual(false)}
            >
              Monthly
            </button>

            <button
              className={`px-4 py-2 rounded-full text-sm font-medium transition-all ${
                isAnnual
                  ? "bg-indigo-600 text-white"
                  : "text-gray-400 hover:text-white"
              }`}
              onClick={() => setIsAnnual(true)}
            >
              Annual <span className="text-xs opacity-75">(-20%)</span>
            </button>
          </div>
        </div>

        {/* Pricing Cards */}
        <div className="grid md:grid-cols-2 gap-8 max-w-5xl mx-auto">
          {/* Free */}
          <div className="bg-gray-900/50 border border-gray-800 rounded-2xl overflow-hidden">
            <div className="p-6 md:p-8">
              <div className="flex justify-between items-start mb-6">
                <div>
                  <h3 className="text-2xl font-bold mb-2">Free</h3>
                  <p className="text-gray-400">
                    Perfect for occasional job seekers
                  </p>
                </div>

                <div className="bg-gray-800 px-3 py-1 rounded-full text-sm">
                  Limited
                </div>
              </div>

              <div className="mb-6">
                <div className="text-4xl font-bold">$0</div>
                <div className="text-gray-400">Forever free</div>
              </div>

              <a
                href="#"
                className="block w-full py-3 px-4 bg-gray-800 hover:bg-gray-700 transition-colors rounded-lg text-center font-medium mb-8"
              >
                Try For Free
              </a>

              <ul className="space-y-4">
                <PricingFeature included text="3 credits per day" />
                <PricingFeature included text="Resume personalization" />
                <PricingFeature included text="Cover letter generation" />
                <PricingFeature included text="48-hour document retention" />
                <PricingFeature included={false} text="Unlimited editing" />
                <PricingFeature
                  included={false}
                  text="Parallel job applications"
                />
                <PricingFeature
                  included={false}
                  text="Advanced layout options"
                />
                <PricingFeature included={false} text="Priority support" />
              </ul>
            </div>
          </div>

          {/* PRO */}
          <div className="bg-gradient-to-b from-indigo-900/30 to-purple-900/30 border border-indigo-700/30 rounded-2xl overflow-hidden relative">
            <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-indigo-500 to-purple-500" />

            <div className="p-6 md:p-8">
              <div className="flex justify-between items-start mb-6">
                <div>
                  <h3 className="text-2xl font-bold mb-2">PRO</h3>
                  <p className="text-gray-400">For serious job hunters</p>
                </div>

                <div className="bg-gradient-to-r from-indigo-600 to-purple-600 px-3 py-1 rounded-full text-sm">
                  Popular
                </div>
              </div>

              <div className="mb-6">
                <div className="text-4xl font-bold">
                  {isAnnual ? "$12.99" : "$15.99"}
                  <span className="text-xl font-normal text-gray-400">
                    /month
                  </span>
                </div>

                <div className="text-gray-400">
                  {isAnnual
                    ? "Billed annually ($155.88)"
                    : "Billed monthly"}
                </div>
              </div>

              <button
                className="block w-full py-3 px-4 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 transition-all rounded-lg text-center font-medium mb-8 cursor-not-allowed"
                disabled
              >
                Coming Soon
              </button>

              <ul className="space-y-4">
                <PricingFeature included text="10+ credits per day" highlight />
                <PricingFeature included text="Resume personalization" />
                <PricingFeature included text="Cover letter generation" />
                <PricingFeature
                  included
                  text="7-day document retention"
                  highlight
                />
                <PricingFeature included text="Unlimited editing" highlight />
                <PricingFeature
                  included
                  text="Parallel job applications"
                  highlight
                />
                <PricingFeature
                  included
                  text="Advanced layout options"
                  highlight
                />
                <PricingFeature included text="Priority support" highlight />
              </ul>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Pricing;