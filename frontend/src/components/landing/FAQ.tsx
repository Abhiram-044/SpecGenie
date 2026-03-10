"use client";

import React, { useState } from "react";
import { ChevronDown, ChevronUp } from "lucide-react";

interface FAQItem {
  question: string;
  answer: string;
}

const faqs: FAQItem[] = [
  {
    question: "How does ResumeX customize my resume?",
    answer:
      "ResumeX uses advanced AI Agents to analyze job descriptions and identify key requirements, skills, and qualifications. It then tailors your resume by highlighting relevant experience and skills that match what employers are looking for, increasing your chances of getting past ATS systems and impressing hiring managers.",
  },
  {
    question: "How many resumes can I generate with the free plan?",
    answer:
      "The free plan gives you 3 credits per day, with each credit allowing you to generate one customized resume or cover letter. Your documents remain accessible for 48 hours, giving you time to download and use them.",
  },
  {
    question: "Is my personal data secure?",
    answer:
      "Yes, we take data security very seriously. All your personal information and resume data is encrypted and stored securely. We never share your data with third parties without your explicit consent, and we comply with all relevant data protection regulations.",
  },
  {
    question: "Can I edit the resumes after they're generated?",
    answer:
      "Basic editing is available on all plans. However, PRO users get access to advanced editing features, including the ability to retry specific sections, adjust formatting, and save multiple versions of their documents.",
  },
  {
    question: "What happens if I'm not satisfied with the result?",
    answer:
      "Free users can generate a new resume using another credit. PRO users have the ability to refine and retry specific sections of their resume without using additional credits, making the customization process more efficient.",
  },
  {
    question: "Does ResumeX help with cover letters too?",
    answer:
      "Absolutely! ResumeX can generate tailored cover letters that complement your resume and address specific requirements from the job description. Each cover letter counts as one credit, just like resumes.",
  },
];

const FAQ: React.FC = () => {
  const [openIndex, setOpenIndex] = useState<number | null>(0);

  const toggleQuestion = (index: number) => {
    setOpenIndex(openIndex === index ? null : index);
  };

  return (
    <section id="faq" className="py-20 md:py-32 relative overflow-hidden">
      {/* Background */}
      <div className="absolute inset-0 bg-gradient-to-b from-gray-950 to-gray-900 z-0" />
      <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-purple-500/50 to-transparent" />

      <div className="container mx-auto px-4 md:px-6 relative z-10">
        {/* Header */}
        <div className="text-center mb-16">
          <div className="inline-block px-3 py-1 mb-6 rounded-full bg-gray-800 border border-gray-700">
            <span className="text-sm font-medium text-purple-400">
              Help Center
            </span>
          </div>

          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Frequently Asked Questions
          </h2>

          <p className="text-xl text-gray-400 max-w-3xl mx-auto">
            Get answers to common questions about ResumeX and how it can help
            with your job search.
          </p>
        </div>

        {/* FAQ List */}
        <div className="max-w-3xl mx-auto">
          <div className="space-y-4">
            {faqs.map((faq, index) => (
              <div
                key={index}
                className="border border-gray-800 rounded-xl overflow-hidden bg-gray-900/50"
              >
                <button
                  className="w-full text-left px-6 py-5 flex justify-between items-center"
                  onClick={() => toggleQuestion(index)}
                >
                  <span className="font-medium text-lg">{faq.question}</span>

                  {openIndex === index ? (
                    <ChevronUp className="h-5 w-5 text-gray-400" />
                  ) : (
                    <ChevronDown className="h-5 w-5 text-gray-400" />
                  )}
                </button>

                {openIndex === index && (
                  <div className="px-6 pb-5">
                    <p className="text-gray-400">{faq.answer}</p>
                  </div>
                )}
              </div>
            ))}
          </div>

          {/* Support */}
          <div className="mt-12 text-center">
            <p className="text-gray-400 mb-4">Still have questions?</p>

            <a
              href="#"
              className="inline-flex items-center text-indigo-400 hover:text-indigo-300 transition-colors font-medium"
            >
              Contact our support team
            </a>
          </div>
        </div>
      </div>
    </section>
  );
};

export default FAQ;