
import Link from 'next/link'
import React from 'react'
import ThemeToggle from '../ThemeToggle'

export default function Header() {
  return (
    <header className="fixed top-0 z-50 w-full bg-black/90 backdrop-blur-sm">
      <div className="mx-auto max-w-screen-2xl px-4 sm:px-6 lg:px-8">
        <nav className="flex h-16 items-center justify-between">
          <Link 
            href="/" 
            className="text-2xl font-semibold text-white hover:text-gray-200 transition-colors"
          >
            Visitor Classification
          </Link>

          <ThemeToggle />
        </nav>
      </div>
    </header>
  )
}
