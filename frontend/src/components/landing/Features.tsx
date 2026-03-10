import {
  FileText,
  Edit,
  BarChart,
  Clock,
  Award,
  Link,
  LucideIcon,
} from "lucide-react"

type Feature = {
  icon: LucideIcon
  title: string
  description: string
  highlighted?: boolean
}

const features: Feature[] = [
  {
    icon: FileText,
    title: "Resume Personalization",
    description:
      "Automatically highlight relevant skills and experiences based on job descriptions.",
    highlighted: true,
  },
  {
    icon: Edit,
    title: "Cover Letter Generation",
    description:
      "Create compelling cover letters that showcase your fit for each specific role.",
    highlighted: true,
  },
  {
    icon: Clock,
    title: "Daily Credit System",
    description:
      "Get 3 free credits daily to generate resumes. PRO users receive 10+ credits for multiple applications.",
  },
  {
    icon: Award,
    title: "PRO Exclusive Features",
    description:
      "Unlock advanced features like retry options and priority queue for faster processing and extended storage.",
    highlighted: true,
  },
  {
    icon: BarChart,
    title: "Success Analytics",
    description:
      "Track your application performance and optimize your resume based on data.",
  },
  {
    icon: Link,
    title: "Job Link Parsing",
    description:
      "Coming soon: Paste a job URL and we'll automatically extract all relevant details.",
  },
]

type FeatureCardProps = {
  icon: LucideIcon
  title: string
  description: string
  highlighted?: boolean
}

function FeatureCard({
  icon: Icon,
  title,
  description,
  highlighted,
}: FeatureCardProps) {
  return (
    <div
      className={`rounded-xl p-6 md:p-8 h-full bg-gray-900/50 border border-gray-800 
      transform transition-all duration-300 hover:scale-105 hover:shadow-xl 
      ${highlighted ? "relative" : ""}`}
    >
      {highlighted && (
        <div className="absolute -top-3 -right-3 bg-gradient-to-r from-indigo-600 to-purple-600 rounded-full px-3 py-1 text-xs font-medium">
          Popular
        </div>
      )}

      <div className="bg-indigo-600/20 rounded-full h-12 w-12 flex items-center justify-center mb-6">
        <Icon size={22} />
      </div>

      <h3 className="text-xl font-semibold mb-3">{title}</h3>
      <p className="text-gray-400">{description}</p>
    </div>
  )
}

export default function Features() {
  return (
    <section
      id="features"
      className="py-20 md:py-32 relative overflow-hidden"
    >
      {/* Background */}
      <div className="absolute inset-0 bg-gradient-to-b from-gray-900 to-gray-950 z-0"></div>

      {/* Purple line */}
      <div className="absolute top-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-purple-500/50 to-transparent"></div>

      {/* Glow effects */}
      <div className="absolute -top-40 -right-40 w-80 h-80 bg-purple-500/5 rounded-full blur-3xl"></div>
      <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-indigo-500/5 rounded-full blur-3xl"></div>

      <div className="container mx-auto px-4 md:px-6 relative z-10">
        <div className="text-center mb-16">
          <div className="inline-block px-3 py-1 mb-6 rounded-full bg-gray-800 border border-gray-700">
            <span className="text-sm font-medium text-purple-400">
              Powerful Features
            </span>
          </div>

          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Everything You Need to Land Your Dream Job
          </h2>

          <p className="text-xl text-gray-400 max-w-3xl mx-auto">
            ResumeX provides all the tools you need to customize your resume
            for each application and maximize your chances of getting hired.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {features.map((feature, index) => (
            <FeatureCard key={index} {...feature} />
          ))}
        </div>
      </div>
    </section>
  )
}