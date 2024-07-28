'use client'
// components/NavBar.tsx
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { useState } from 'react';

const NavBar = () => {
  const pathname = usePathname();
  
  const navLinks = [
    { href: '/', label: 'Home' },
    { href: '/musicGenres', label: 'Music Genres' },
    { href: '/test', label: 'Test' },
    // { href: '/about', label: 'About' },
    // { href: '/posts', label: 'Posts' },
  ];

  const [isMenuOpen, setIsMenuOpen] = useState(false);
  
  return (
    <>
    <div className='navbar bg-red-500 dark:bg-gray-800 px-4'>
      <div className="container mx-auto flex justify-between items-center">
        {/* <Link href="/" className="text-white text-xl font-bold">
          Logo
        </Link> */}

        {/* Burger menu button */}
        <button 
          className="sm:hidden text-white"
          onClick={() => setIsMenuOpen(!isMenuOpen)}
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>

        {/* Desktop menu */}
        <div className="hidden sm:flex gap-x-4">
          {navLinks.map((link) => {
            const isActive = pathname === link.href;
            return (
              <Link
                key={link.href}
                href={link.href}
                className={`
                  px-3 py-2 rounded-md text-sm font-medium
                  ${isActive 
                    ? 'bg-red-700 text-white dark:bg-gray-900 dark:text-white'
                    : 'text-red-200 hover:bg-red-600 hover:text-white dark:text-gray-300 dark:hover:bg-gray-700 dark:hover:text-white'
                  }
                `}
              >
                {link.label}
              </Link>
            );
          })}
        </div>
      </div>

      {/* Mobile menu */}
      {isMenuOpen && (
        <div className="sm:hidden w-1/2 top-12 absolute flex flex-col bg-red-500 dark:bg-gray-800">
          {navLinks.map((link) => {
            const isActive = pathname === link.href;
            return (
              <Link
                key={link.href}
                href={link.href}
                className={`
                  block px-3 py-2 text-base font-medium
                  ${isActive 
                    ? 'bg-red-700 text-white dark:bg-gray-900 dark:text-white'
                    : 'text-red-200 hover:bg-red-600 hover:text-white dark:text-gray-300 dark:hover:bg-gray-700 dark:hover:text-white'
                  }
                `}
                onClick={() => setIsMenuOpen(false)}
              >
                {link.label}
              </Link>
            );
          })}
        </div>
      )}
    </div>
    </>
  );
};

export default NavBar;