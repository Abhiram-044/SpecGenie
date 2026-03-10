import Link from "next/link"
import {
  FileText,
  Mail,
  Twitter,
  Linkedin,
  Github,
  LucideIcon,
} from "lucide-react"

type FooterLink = {
  label: string
  href: string
}

type SocialLink = {
  icon: LucideIcon
  href: string
}

const productLinks: FooterLink[] = [
  { label: "Features", href: "#" },
  { label: "Pricing", href: "#" },
  { label: "Testimonials", href: "#" },
  { label: "Help Center", href: "#" },
]

const companyLinks: FooterLink[] = [
  { label: "About", href: "#" },
  { label: "Blog", href: "#" },
  { label: "Careers", href: "#" },
  { label: "Contact", href: "#" },
]

const legalLinks: FooterLink[] = [
  { label: "Privacy Policy", href: "#" },
  { label: "Terms of Service", href: "#" },
  { label: "Cookie Policy", href: "#" },
  { label: "GDPR", href: "#" },
]

const socialLinks: SocialLink[] = [
  { icon: Twitter, href: "#" },
  { icon: Linkedin, href: "#" },
  { icon: Github, href: "#" },
  { icon: Mail, href: "#" },
]

function LinkColumn({
  title,
  links,
}: {
  title: string
  links: FooterLink[]
}) {
  return (
    <div>
      <h3 className="text-lg font-semibold mb-4">{title}</h3>

      <ul className="space-y-3">
        {links.map((link) => (
          <li key={link.label}>
            <Link
              href={link.href}
              className="text-gray-400 hover:text-white transition-colors"
            >
              {link.label}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default function Footer() {
  return (
    <footer className="bg-gray-950 border-t border-gray-900">
      <div className="container mx-auto px-4 md:px-6 pt-16 pb-8">
        
        {/* Top Section */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-12 mb-12">

          {/* Brand */}
          <div className="md:col-span-1">
            <Link
              href="/"
              className="flex items-center space-x-2 mb-6"
            >
              <FileText className="h-8 w-8 text-indigo-500" />
              <span className="text-xl font-bold">SpecGenie</span>
            </Link>

            <p className="text-gray-400 mb-6">
              AI-powered resume and cover letter platform that helps job seekers land their dream jobs faster.
            </p>

            <div className="flex space-x-4">
              {socialLinks.map(({ icon: Icon, href }, index) => (
                <Link
                  key={index}
                  href={href}
                  className="text-gray-400 hover:text-indigo-400 transition-colors"
                >
                  <Icon className="h-5 w-5" />
                </Link>
              ))}
            </div>
          </div>

          <LinkColumn title="Product" links={productLinks} />
          <LinkColumn title="Company" links={companyLinks} />
          <LinkColumn title="Legal" links={legalLinks} />

        </div>

        {/* Bottom Section */}
        <div className="pt-8 border-t border-gray-900 flex flex-col md:flex-row justify-between items-center">

          <p className="text-gray-500 text-sm mb-4 md:mb-0">
            © {new Date().getFullYear()} SpecGenie. All rights reserved.
          </p>

          <div className="flex space-x-6">
            <Link href="#" className="text-gray-500 hover:text-gray-400 text-sm">
              Privacy
            </Link>
            <Link href="#" className="text-gray-500 hover:text-gray-400 text-sm">
              Terms
            </Link>
            <Link href="#" className="text-gray-500 hover:text-gray-400 text-sm">
              Cookies
            </Link>
          </div>

        </div>
      </div>
    </footer>
  )
}