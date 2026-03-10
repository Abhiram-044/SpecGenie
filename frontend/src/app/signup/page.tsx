"use client";

import { useState } from "react";
import Link from "next/link";
import { Mail, Linkedin, FileText } from "lucide-react";
import { registerInitiate } from "@/services/auth/authAPI";
import toast, { Toaster } from "react-hot-toast";
import { useRouter } from "next/navigation";

export default function Signup() {
    const [email, setEmail] = useState<string>("");
    const [loading, setLoading] = useState<boolean>(false);

    const router = useRouter();

    const handleMagicLink = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();

        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!email || !emailRegex.test(email)) {
            toast.error("Please enter a valid email address", {
                style: {
                    border: "1px solid #ff0000",
                    backgroundColor: "rgba(251, 44, 54, 0.1)",
                    color: "#fb2c36",
                },
            });
            return;
        }

        setLoading(true);

        // Create the promise call
        const initiatePromise = registerInitiate(email);

        toast.promise(
            initiatePromise,
            {
                loading: "Sending Magic Link...",
                success: "Magic link sent! Redirecting...",
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
                    duration: 3000,
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
            await initiatePromise;
            // Successful? Navigate to the next step
            setTimeout(() => {
                router.push("/create-account");
            }, 2000);
        } catch (err) {
            console.error("Magic link request failed:", err);
        } finally {
            setLoading(false);
        }
    };

    const handleGoogleSignup = () => {
        console.log("Google signup clicked");
    };

    const handleLinkedInSignup = () => {
        console.log("LinkedIn signup clicked");
    };

    return (
        <div className="min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
            <Toaster position="bottom-right" reverseOrder={false} />

            <div className="max-w-md w-full space-y-8">
                {/* Header */}
                <div className="text-center">
                    <div className="flex justify-center">
                        <FileText className="h-12 w-12 text-indigo-500" />
                    </div>

                    <h2 className="mt-6 text-3xl font-bold">Create your account</h2>

                    <p className="mt-2 text-sm text-gray-400">
                        Already have an account?{" "}
                        <Link
                            href="/login"
                            className="text-indigo-400 hover:text-indigo-300"
                        >
                            Sign in
                        </Link>
                    </p>
                </div>

                {/* Form */}
                <form className="mt-8 space-y-6" onSubmit={handleMagicLink}>
                    {/* Email */}
                    <div>
                        <label htmlFor="email" className="sr-only">
                            Email address
                        </label>

                        <div className="relative">
                            <div className="absolute z-1 inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                                <Mail className="h-5 w-5 text-gray-400" />
                            </div>

                            <input
                                id="email"
                                name="email"
                                type="text"
                                autoComplete="email"
                                required
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                className="appearance-none block w-full px-3 py-2 pl-10 border border-gray-700 rounded-lg bg-gray-900 placeholder-gray-400 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
                                placeholder="Email address"
                            />
                        </div>
                    </div>

                    {/* Submit */}
                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full flex justify-center py-2 px-4 border border-transparent rounded-lg text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:ring-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        {loading ? "Sending..." : "Send Magic Link"}
                    </button>

                    {/* Divider */}
                    <div className="relative">
                        <div className="absolute inset-0 flex items-center">
                            <div className="w-full border-t border-gray-700"></div>
                        </div>

                        <div className="relative flex justify-center text-sm">
                            <span className="px-2 bg-gray-950 text-gray-400">
                                Or continue with
                            </span>
                        </div>
                    </div>

                    {/* OAuth Buttons */}
                    <div className="grid grid-cols-2 gap-3">
                        <button
                            type="button"
                            onClick={handleGoogleSignup}
                            className="w-full inline-flex justify-center py-2 px-4 border border-gray-700 rounded-lg bg-gray-900 text-sm text-gray-300 hover:bg-gray-800"
                        >
                            <img
                                className="h-5 w-5"
                                src="https://www.svgrepo.com/show/475656/google-color.svg"
                                alt="Google"
                            />
                            <span className="ml-2">Google</span>
                        </button>

                        <button
                            type="button"
                            onClick={handleLinkedInSignup}
                            className="w-full inline-flex justify-center py-2 px-4 border border-gray-700 rounded-lg bg-gray-900 text-sm text-gray-300 hover:bg-gray-800"
                        >
                            <Linkedin className="h-5 w-5 text-[#0A66C2]" />
                            <span className="ml-2">LinkedIn</span>
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}