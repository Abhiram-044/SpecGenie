"use client"

import { ReactNode, useEffect, useState } from "react"
import { useRouter, usePathname } from "next/navigation"
import { isTokenValid } from "@/lib/auth"

interface ProtectedRouteProps {
  children: ReactNode
}

export default function ProtectedRoute({ children }: ProtectedRouteProps) {
  const router = useRouter()
  const pathname = usePathname()

  const [isValid, setIsValid] = useState<boolean | null>(null)

  useEffect(() => {
    const valid = isTokenValid()
    setIsValid(valid)

    if (!valid) {
      router.replace(`/login`)
    }
  }, [router, pathname])

  if (isValid === null) return null

  return <>{children}</>
}