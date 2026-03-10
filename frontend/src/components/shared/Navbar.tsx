"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  FileText,
  X,
  Menu,
  Crown,
  LogOut,
  User,
  ChevronDown,
  ChevronUp,
  Settings,
} from "lucide-react";

// import { onboardingStore } from "@/stores/onboardingStore";

const Navbar: React.FC = () => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const pathname = usePathname();

  const isAuthPage = ["/login", "/signup", "/create-account"].includes(
    pathname
  );

  const isOnboardingPage = pathname.startsWith("/onboarding");

  const isLoggedIn = [
    "/dashboard",
    "/onboarding",
    "/generate/resume",
    "/generate/cover-letter",
    "/resume-editor",
  ].includes(pathname);

//   const { originalData } = onboardingStore();

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10);
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  if (isAuthPage) return null;

  const handleLogout = () => {
    localStorage.clear();
    window.location.href = "/";
  };

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const ProfileDropdownMenu = (
    <div className="bg-gray-900 absolute right-0 mt-2 w-64 rounded-lg shadow-lg flex flex-col space-y-4 z-50 p-4 border-gray-600 border">
      <div className="space-x-2 px-4 py-1">
        {/* <h2 className="font-bold text-lg">{originalData?.name}</h2> */}
        {/* <h4 className="text-base text-gray-400">{originalData?.email}</h4> */}
      </div>

      <hr className="text-gray-400" />

      <div className="flex items-center space-x-2 px-4 py-1 cursor-pointer hover:bg-gray-800 rounded">
        <Settings className="h-4 w-4" />
        <span>Manage Profile Data</span>
      </div>

      <div
        className="flex items-center space-x-2 px-4 py-1 cursor-pointer hover:bg-gray-800 rounded"
        onClick={handleLogout}
      >
        <LogOut className="h-4 w-4 text-red-500" />
        <span className="text-red-500">Logout</span>
      </div>
    </div>
  );

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        isScrolled
          ? "bg-gray-900/95 backdrop-blur-sm py-4 shadow-md"
          : "bg-transparent py-6"
      }`}
    >
      <div className="container mx-auto px-4 md:px-6 flex items-center justify-between">
        <Link
          href={isLoggedIn ? "/dashboard" : "/"}
          className="flex flex-row items-center space-x-2"
        >
          <FileText className="h-8 w-8 text-indigo-500" />
          <span className="text-xl font-bold">ResumeX</span>
        </Link>

        {/* Desktop Nav */}
        {!isOnboardingPage && (
          <nav className="hidden md:flex flex-row items-center space-x-8 relative">
            {isLoggedIn ? (
              <>
                <button
                  disabled
                  className="flex items-center space-x-2 px-4 py-2 bg-gradient-to-r from-yellow-600 to-orange-600 rounded-full cursor-not-allowed"
                >
                  <Crown className="h-4 w-4" />
                  <span className="text-sm font-medium">Upgrade to PRO</span>
                </button>

                <div className="relative">
                  <button onClick={toggleMenu}>
                    <span className="flex items-center space-x-2 p-1 rounded-full hover:bg-gray-800 transition-colors cursor-pointer">
                      <div className="w-10 h-10 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full flex items-center justify-center">
                        <User className="h-5 w-5 text-white" />
                      </div>

                      {isMenuOpen ? (
                        <ChevronUp className="h-4 w-4 text-gray-400" />
                      ) : (
                        <ChevronDown className="h-4 w-4 text-gray-400" />
                      )}
                    </span>
                  </button>

                  {isMenuOpen && (
                    <div className="hidden md:block absolute right-0 top-full">
                      {ProfileDropdownMenu}
                    </div>
                  )}
                </div>
              </>
            ) : (
              <>
                <a
                  href="#how-it-works"
                  className="text-gray-300 hover:text-white transition-colors"
                >
                  How It Works
                </a>

                <a
                  href="#features"
                  className="text-gray-300 hover:text-white transition-colors"
                >
                  Features
                </a>

                <a
                  href="#pricing"
                  className="text-gray-300 hover:text-white transition-colors"
                >
                  Pricing
                </a>

                <a
                  href="#faq"
                  className="text-gray-300 hover:text-white transition-colors"
                >
                  FAQ
                </a>

                <Link
                  href="/login"
                  className="py-2 px-4 rounded-full bg-indigo-600 hover:bg-indigo-700 transition-colors"
                >
                  Sign In
                </Link>

                <Link
                  href="/signup"
                  className="py-2 px-4 rounded-full bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700"
                >
                  Get Started Free
                </Link>
              </>
            )}
          </nav>
        )}

        {/* Mobile Menu Button */}
        {!isOnboardingPage && (
          <button className="md:hidden" onClick={toggleMenu}>
            {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        )}
      </div>

      {/* Mobile Nav */}
      {isMenuOpen && (
        <nav className="md:hidden bg-gray-900 absolute top-full left-0 right-0 p-4 shadow-lg flex flex-col space-y-4">
          {isLoggedIn ? (
            <>
              <div className="space-x-2 px-4 py-1">
                {/* <h2 className="font-bold text-lg">{originalData?.name}</h2> */}
                <h4 className="text-base text-gray-400">
                  {/* {originalData?.email} */}
                </h4>
              </div>

              <button
                disabled
                className="flex items-center space-x-2 px-4 py-2 bg-gradient-to-r from-yellow-600 to-orange-600 rounded-full cursor-not-allowed w-fit"
              >
                <Crown className="h-4 w-4" />
                <span className="text-sm font-medium">Upgrade to PRO</span>
              </button>

              <hr className="text-gray-400" />

              <div className="flex items-center space-x-2 px-4 py-1 cursor-pointer hover:bg-gray-800 rounded">
                <Settings className="h-4 w-4" />
                <span>Manage Profile Data</span>
              </div>

              <div
                className="flex items-center space-x-2 px-4 py-1 cursor-pointer hover:bg-gray-800 rounded"
                onClick={handleLogout}
              >
                <LogOut className="h-4 w-4 text-red-500" />
                <span className="text-red-500">Logout</span>
              </div>
            </>
          ) : (
            <>
              <a href="#how-it-works" className="text-gray-300 py-2 px-4">
                How It Works
              </a>

              <a href="#features" className="text-gray-300 py-2 px-4">
                Features
              </a>

              <a href="#pricing" className="text-gray-300 py-2 px-4">
                Pricing
              </a>

              <a href="#faq" className="text-gray-300 py-2 px-4">
                FAQ
              </a>

              <Link
                href="/login"
                className="py-2 px-4 rounded-full bg-indigo-600 text-center"
              >
                Sign In
              </Link>

              <Link
                href="/signup"
                className="py-2 px-4 rounded-full bg-gradient-to-r from-indigo-600 to-purple-600 text-center"
              >
                Get Started Free
              </Link>
            </>
          )}
        </nav>
      )}
    </header>
  );
};

export default Navbar;