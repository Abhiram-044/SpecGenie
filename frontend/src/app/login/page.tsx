"use client"

import { useState } from "react"
import Link from "next/link"
import { User, Lock, Linkedin, FileText, EyeClosed, Eye, Mail } from "lucide-react"
import toast, { Toaster } from "react-hot-toast"
import { useRouter } from "next/navigation"
import { login } from "@/services/auth/authAPI"

type LoginMethod = "email" | "username"

export default function Login() {
  const router = useRouter()

  const [method, setMethod] = useState<LoginMethod>("email")
  const [eUser, setEUser] = useState<string>("")
  const [password, setPassword] = useState<string>("")
  const [showPassword, setShowPassword] = useState<boolean>(false)

  const togglePasswordVisibility = () => setShowPassword((prev) => !prev)

  const handleEUserLogin = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (method === "email") {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!eUser || !emailRegex.test(eUser)) {
        toast.error("Please enter a valid email address", {
          style: { border: "1px solid #ff0000", backgroundColor: "rgba(251, 44, 54, 0.1)", color: "#fb2c36" }
        });
        return;
      }
    } else if (eUser.length < 3) {
      toast.error("Username must be at least 3 characters", {
        style: { border: "1px solid #ff0000", backgroundColor: "rgba(251, 44, 54, 0.1)", color: "#fb2c36" }
      });
      return;
    }

    const loginPromise = login(eUser, password);

    toast.promise(
      loginPromise,
      {
        loading: "Logging In...",
        success: "Successfully logged in! Redirecting...",
        error: (err) => err.message,
      },
      {
        style: { minWidth: '250px' },
        loading: {
          style: {
            border: "1px solid #3b82f6",
            backgroundColor: "rgba(59, 130, 246, 0.1)",
            color: "#3b82f6",
          },
        },
        success: {
          duration: 5000,
          style: {
            border: "1px solid rgba(47, 200, 122, 0.5)",
            backgroundColor: "rgba(47, 200, 122, 0.1)",
            color: "#2fc87a",
          },
        },
        error: {
          style: {
            border: "1px solid rgba(251, 44, 54, 0.5)",
            backgroundColor: "rgba(251, 44, 54, 0.1)",
            color: "#fb2c36",
          },
        },
      }
    );

    try {
      await loginPromise;
      setTimeout(() => {
        router.push("/onboarding");
      }, 2000);
    } catch (err) {
      console.error("Login Error:", err);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 bg-gray-950">
      <Toaster position="bottom-right" reverseOrder={false} />

      <div className="max-w-md w-full space-y-8">
        <div className="text-center">
          <div className="flex justify-center">
            <FileText className="h-12 w-12 text-indigo-500" />
          </div>
          <h2 className="mt-6 text-3xl font-bold text-white">Welcome back</h2>
          <p className="mt-2 text-sm text-gray-400">
            Don't have an account?{" "}
            <Link href="/signup" className="text-indigo-400 hover:text-indigo-300">
              Sign up
            </Link>
          </p>
        </div>

        {/* --- TABS SECTION --- */}
        <div className="flex p-1 bg-gray-900 rounded-lg border border-gray-800">
          <button
            onClick={() => { setMethod("email"); setEUser(""); }}
            className={`flex-1 py-2 text-sm font-medium rounded-md transition-all ${method === "email" ? "bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow" : "text-gray-400 hover:text-gray-200"
              }`}
          >
            Email
          </button>
          <button
            onClick={() => { setMethod("username"); setEUser(""); }}
            className={`flex-1 py-2 text-sm font-medium rounded-md transition-all ${method === "username" ? "bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow" : "text-gray-400 hover:text-gray-200"
              }`}
          >
            Username
          </button>
        </div>

        <form className="mt-4 space-y-6" onSubmit={handleEUserLogin}>
          <div className="space-y-4">
            {/* DYNAMIC INPUT FIELD */}
            <div>
              <label htmlFor="identifier" className="sr-only">
                {method === "email" ? "Email address" : "Username"}
              </label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  {method === "email" ? (
                    <Mail className="h-5 w-5 text-gray-400" />
                  ) : (
                    <User className="h-5 w-5 text-gray-400" />
                  )}
                </div>
                <input
                  id="identifier"
                  type={method === "email" ? "email" : "text"}
                  required
                  value={eUser}
                  onChange={(e) => setEUser(e.target.value)}
                  className="appearance-none block w-full px-3 py-2 pl-10 border border-gray-700 rounded-lg bg-gray-900 placeholder-gray-400 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-colors"
                  placeholder={method === "email" ? "name@company.com" : "Enter your username"}
                />
              </div>
            </div>

            {/* PASSWORD FIELD */}
            <div>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Lock className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  autoComplete="current-password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="appearance-none block w-full px-3 py-2 pl-10 pr-10 border border-gray-700 rounded-lg bg-gray-900 placeholder-gray-400 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  placeholder="Password"
                />
                <button
                  type="button"
                  onClick={togglePasswordVisibility}
                  className="absolute inset-y-0 right-3 flex items-center text-gray-400 hover:text-gray-200"
                >
                  {showPassword ? <Eye className="h-5 w-5" /> : <EyeClosed className="h-5 w-5" />}
                </button>
              </div>
            </div>
          </div>

          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <input
                id="remember-me"
                type="checkbox"
                className="h-4 w-4 rounded border-gray-700 bg-gray-900 text-indigo-600 focus:ring-indigo-500"
              />
              <label htmlFor="remember-me" className="ml-2 text-sm text-gray-400">
                Remember me
              </label>
            </div>
            <div className="text-sm">
              <Link href="#" className="text-indigo-400 hover:text-indigo-300">
                Forgot password?
              </Link>
            </div>
          </div>

          <button
            type="submit"
            className="w-full py-2 px-4 rounded-lg text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors shadow-lg"
          >
            Sign In
          </button>

          <div className="relative">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-gray-700"></div>
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-2 bg-gray-950 text-gray-400">Or continue with</span>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <button
              type="button"
              className="flex justify-center items-center py-2 px-4 border border-gray-700 rounded-lg bg-gray-900 text-sm text-gray-300 hover:bg-gray-800 transition-colors"
            >
              <img className="h-5 w-5 mr-2" src="https://www.svgrepo.com/show/475656/google-color.svg" alt="Google" />
              Google
            </button>
            <button
              type="button"
              className="flex justify-center items-center py-2 px-4 border border-gray-700 rounded-lg bg-gray-900 text-sm text-gray-300 hover:bg-gray-800 transition-colors"
            >
              <Linkedin className="h-5 w-5 text-[#0A66C2] mr-2" />
              LinkedIn
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}