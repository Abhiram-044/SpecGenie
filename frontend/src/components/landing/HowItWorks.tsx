import {
  FileText,
  Search,
  CheckCircle,
  Download,
  LucideIcon,
} from "lucide-react"

type Step = {
  icon: LucideIcon
  title: string
  description: string
}

const steps: Step[] = [
  {
    icon: FileText,
    title: "Upload Job Description",
    description:
      "Paste any job description or upload a PDF. Our AI instantly analyzes the requirements.",
  },
  {
    icon: Search,
    title: "AI Analysis",
    description:
      "Our AI identifies key skills, requirements, and priorities from the job posting.",
  },
  {
    icon: CheckCircle,
    title: "Tailored Generation",
    description:
      "Get a custom resume and cover letter highlighting your relevant experience and skills.",
  },
  {
    icon: Download,
    title: "Download & Apply",
    description:
      "Download your polished documents in PDF format, ready to submit to employers.",
  },
]

type StepItemProps = {
  icon: LucideIcon
  title: string
  description: string
}

function StepItem({ icon: Icon, title, description }: StepItemProps) {
  return (
    <div className="flex items-start space-x-4">
      <div className="flex-shrink-0 w-12 h-12 bg-indigo-500/20 rounded-full flex items-center justify-center text-indigo-400">
        <Icon className="h-6 w-6" />
      </div>

      <div>
        <h3 className="text-xl font-semibold mb-2">{title}</h3>
        <p className="text-gray-400">{description}</p>
      </div>
    </div>
  )
}

export default function HowItWorks() {
  return (
    <section
      id="how-it-works"
      className="py-20 md:py-32 relative overflow-hidden"
    >
      {/* Background */}
      <div className="absolute inset-0 bg-gradient-to-b from-gray-950 to-gray-900 z-0"></div>

      <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-indigo-500/50 to-transparent"></div>

      <div className="container mx-auto px-4 md:px-6 relative z-10">

        {/* Heading */}
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            How ResumeX Works
          </h2>

          <p className="text-xl text-gray-400 max-w-3xl mx-auto">
            Our AI-powered platform streamlines your job application process with a simple four-step flow
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-16 max-w-6xl mx-auto items-center">

          {/* Steps */}
          <div className="space-y-12">
            {steps.map((step, index) => (
              <StepItem key={index} {...step} />
            ))}
          </div>

          {/* Illustration */}
          <div className="relative">

            <div className="absolute -top-40 -right-40 w-80 h-80 bg-indigo-500/10 rounded-full blur-3xl"></div>
            <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-purple-500/10 rounded-full blur-3xl"></div>

            <div className="relative bg-gray-900/50 rounded-2xl p-6 border border-gray-800/50 shadow-xl transform hover:scale-105 transition-transform duration-300">

              <div className="space-y-4">

                <div className="h-12 bg-gray-800/50 rounded-lg w-3/4"></div>

                <div className="h-4 bg-gray-800/50 rounded w-1/2"></div>
                <div className="h-4 bg-gray-800/50 rounded w-2/3"></div>

                <div className="h-32 bg-indigo-500/10 rounded-lg border border-indigo-500/20 p-4">

                  <div className="h-4 bg-indigo-500/20 rounded w-3/4 mb-3"></div>
                  <div className="h-4 bg-indigo-500/20 rounded w-1/2 mb-3"></div>
                  <div className="h-4 bg-indigo-500/20 rounded w-2/3"></div>

                </div>

              </div>

            </div>

            <div className="absolute bottom-4 right-4 transform translate-x-1/4 translate-y-1/4">

              <div className="bg-gray-900/50 rounded-2xl p-4 border border-gray-800/50 shadow-xl w-64 transform -rotate-6">

                <div className="space-y-3">

                  <div className="h-3 bg-gray-800/50 rounded w-3/4"></div>
                  <div className="h-3 bg-gray-800/50 rounded w-1/2"></div>
                  <div className="h-3 bg-gray-800/50 rounded w-2/3"></div>

                </div>

              </div>

            </div>

          </div>

        </div>
      </div>
    </section>
  )
}