import Navbar from "@/components/shared/Navbar";
import "./globals.css";

export const metadata = {
  title: "SpecGenie",
  description: "AI Resume Generator",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <div className="min-h-screen bg-gray-950 text-gray-100">
          <Navbar />
          {children}
        </div>
      </body>
    </html>
  );
}