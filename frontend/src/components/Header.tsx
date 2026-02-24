import { useEffect, useState } from 'react'
import { Link } from 'react-router'
import { Button } from './ui/button'
import { Settings } from 'lucide-react'
export function Header() {
  // Btn para dark mode
  const [isDark, setIsDark] = useState(
    () => localStorage.getItem('theme') === 'dark'
  )
  useEffect(() => {
    if (isDark) {
      document.documentElement.classList.add('dark')
      localStorage.setItem('theme', 'dark')
    } else {
      document.documentElement.classList.remove('dark')
      localStorage.setItem('theme', 'light')
    }
  }, [isDark])
  return (
    <header className='flex justify-around items-center py-5 px-4 border-b border-border '>
      <h1 className='text-3xl font-semibold'>
        <Link to='/'>Runtime</Link>
      </h1>
      <nav>
        <ul className='flex justify-center items-center gap-x-2'>
          <li>
            <Button asChild size='icon-md' className='rounded-full'>
              <Link to='/configuraciones'>
                <Settings />
              </Link>
            </Button> 
          </li>
          <li>
            <Button
              variant='secondary'
              onClick={() => setIsDark(!isDark)}
            >
              {isDark ? 'Dark' : 'Light'}
            </Button>
          </li>
        </ul>
      </nav>
    </header>
  )
}
