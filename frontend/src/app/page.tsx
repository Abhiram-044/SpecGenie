import HeroSection from "@/components/landing/HeroSection"
import HowItWorks from "@/components/landing/HowItWorks"
import Features from "@/components/landing/Features"
import Pricing from "@/components/landing/Pricing"
import Referral from "@/components/landing/Referral"
import FAQ from "@/components/landing/FAQ"
import Footer from "@/components/landing/Footer"

export default function Home() {
  return (
    <main>
      <HeroSection />
      <HowItWorks />
      <Features />
      <Pricing />
      <Referral />
      <FAQ />
      <Footer />
    </main>
  )
}