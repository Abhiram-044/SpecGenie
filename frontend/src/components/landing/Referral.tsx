"use client";

import React from "react";
import { Share2, Gift } from "lucide-react";

const Referral: React.FC = () => {
  return (
    <section className="py-20 relative overflow-hidden">
      {/* Background */}
      <div className="absolute inset-0 bg-gradient-to-b from-gray-900 to-gray-950 z-0" />
      <div className="absolute top-1/4 -left-40 w-80 h-80 bg-purple-500/5 rounded-full blur-3xl" />
      <div className="absolute bottom-1/4 -right-40 w-80 h-80 bg-indigo-500/5 rounded-full blur-3xl" />

      <div className="container mx-auto px-4 md:px-6 relative z-10">
        <div className="bg-gradient-to-r from-gray-900 to-gray-800 border border-gray-700/50 rounded-2xl overflow-hidden shadow-xl max-w-4xl mx-auto">
          
          {/* Main Section */}
          <div className="p-8 md:p-12">
            <div className="flex flex-col md:flex-row items-center gap-8">

              {/* Icon */}
              <div className="bg-indigo-900/30 rounded-full p-6 flex-shrink-0">
                <Gift className="h-12 w-12 text-indigo-400" />
              </div>

              {/* Content */}
              <div className="flex-1">
                <h2 className="text-2xl md:text-3xl font-bold mb-3 text-center md:text-left">
                  Get More Free Credits
                </h2>

                <p className="text-gray-400 mb-6 text-center md:text-left">
                  Refer friends to ResumeX and earn 5 additional credits for each
                  friend who signs up. Share your referral link now.
                </p>

                {/* Referral Link */}
                <div className="flex flex-col sm:flex-row gap-4">
                  <div className="flex-1 bg-gray-800 rounded-lg p-3 flex items-center justify-between border border-gray-700">
                    <span className="text-sm text-gray-400 truncate">
                      resumex.ai/refer/your-unique-code
                    </span>

                    <button className="text-indigo-400 hover:text-indigo-300 transition-colors">
                      Copy
                    </button>
                  </div>

                  <button className="flex items-center justify-center bg-indigo-600 hover:bg-indigo-700 transition-colors rounded-lg px-5 py-3">
                    <Share2 className="h-5 w-5 mr-2" />
                    Share
                  </button>
                </div>
              </div>
            </div>
          </div>

          {/* Stats */}
          <div className="bg-gray-900 p-6 border-t border-gray-800">
            <div className="flex justify-center items-center space-x-6 text-center divide-x divide-gray-700">
              
              <div className="px-4">
                <div className="text-2xl font-bold text-white">2</div>
                <div className="text-sm text-gray-400">
                  Credits per referral
                </div>
              </div>

              <div className="px-4">
                <div className="text-2xl font-bold text-white">5 / Month</div>
                <div className="text-sm text-gray-400">
                  Referrals possible
                </div>
              </div>

              <div className="px-4">
                <div className="text-2xl font-bold text-white">Instant</div>
                <div className="text-sm text-gray-400">
                  Credit delivery
                </div>
              </div>

            </div>
          </div>

        </div>
      </div>
    </section>
  );
};

export default Referral;