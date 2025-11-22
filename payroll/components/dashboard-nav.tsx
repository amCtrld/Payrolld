"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { Button } from "@/components/ui/button"

export default function DashboardNav() {
  const pathname = usePathname()

  const handleLogout = () => {
    console.log("Nav: Logging out...") // Debug
    localStorage.removeItem("token")
    localStorage.removeItem("user")
    // Clear cookies
    document.cookie = "token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT"
    window.location.href = "/login"
  }

  const navItems = [
    { href: "/dashboard", label: "Dashboard" },
    { href: "/employees", label: "Employees" },
    { href: "/payroll", label: "Payroll" },
    { href: "/payslips", label: "Payslips" },
    { href: "/analytics", label: "Analytics" },
  ]

  return (
    <aside className="w-64 bg-gray-900 text-white">
      <div className="p-6">
        <h2 className="text-xl font-bold">Payroll System</h2>
      </div>
      <nav className="space-y-2 px-4">
        {navItems.map((item) => (
          <Link key={item.href} href={item.href}>
            <Button variant={pathname === item.href ? "default" : "ghost"} className="w-full justify-start">
              {item.label}
            </Button>
          </Link>
        ))}
      </nav>
      <div className="absolute bottom-4 left-4 right-4">
        <Button onClick={handleLogout} variant="destructive" className="w-full">
          Logout
        </Button>
      </div>
    </aside>
  )
}
