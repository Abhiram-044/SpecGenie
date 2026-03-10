import Link from "next/link"
import { ArrowRight } from "lucide-react"

export default function HeroSection() {
  return (
    <section className="pt-32 pb-24 md:pt-40 md:pb-32 relative overflow-hidden">

      {/* Background */}
      <div className="absolute inset-0 bg-gradient-to-b from-indigo-900/20 to-transparent z-0"></div>

      <div className="absolute top-1/4 -left-64 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl"></div>
      <div className="absolute bottom-1/3 -right-64 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl"></div>

      <div className="container mx-auto px-4 md:px-6 relative z-10">

        <div className="max-w-4xl mx-auto text-center">

          {/* Badge */}
          <div className="inline-block px-3 py-1 mb-6 rounded-full bg-gray-800 border border-gray-700">
            <span className="text-sm font-medium text-indigo-400">
              AI-Powered Resume Builder
            </span>
          </div>

          {/* Heading */}
          <h1 className="text-4xl md:text-6xl font-bold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-white to-gray-400">
            Tailored Resumes for Every Job – Powered by AI
          </h1>

          {/* Subtitle */}
          <p className="text-xl md:text-2xl text-gray-400 mb-10 leading-relaxed">
            Generate role-specific resumes in seconds using job descriptions.
            Let AI match your skills to each opportunity.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">

            <Link
              href="/signup"
              className="px-8 py-4 w-full sm:w-auto rounded-full bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-medium text-lg inline-flex items-center justify-center hover:from-indigo-700 hover:to-purple-700 transition-all transform hover:scale-105 focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-gray-900"
            >
              Get Started Free
              <ArrowRight className="ml-2 h-5 w-5" />
            </Link>

            <Link
              href="#how-it-works"
              className="px-8 py-4 w-full sm:w-auto rounded-full bg-gray-800 text-white font-medium text-lg hover:bg-gray-700 transition-all"
            >
              See How It Works
            </Link>

          </div>

          {/* Stats Box */}
          <div className="mt-16 p-1 bg-gradient-to-r from-indigo-500/20 via-purple-500/20 to-indigo-500/20 rounded-xl">

            <div className="bg-gray-900 rounded-lg p-4 md:p-8">

              <p className="text-gray-400 mb-4">
                Trusted by job seekers worldwide
              </p>

              <div className="flex flex-wrap justify-center gap-8 md:gap-16">

                <div className="text-white opacity-70 font-semibold">
                  1000+ Resumes
                </div>

                <div className="text-white opacity-70 font-semibold">
                  4.8/5 Rating
                </div>

                <div className="text-white opacity-70 font-semibold">
                  92% Success Rate
                </div>

              </div>

            </div>

          </div>

        </div>
      </div>
    </section>
  )
}