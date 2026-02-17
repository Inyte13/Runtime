import { Header } from './components/Header.js'
import { Route, Routes } from 'react-router'
import { lazy } from 'react'

const Home = lazy(() => import('./pages/Home.js'))

export default function App() {
  return (
    <div className='flex flex-col h-screen'>
      <Header />
      <main className='flex-1 overflow-hidden max-w-7xl mx-auto p-4 w-full'>
        <Routes>
          <Route path='/' element={<Home />} />
        </Routes>
      </main>
    </div>
  )
}
