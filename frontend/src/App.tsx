import { Header } from './components/Header.js'
import { Route, Routes } from 'react-router'
import { lazy } from 'react'

const Home = lazy(() => import('./pages/Home.js'))

  // El overflow-hidden en el div es para proteger toda la ventana
  // El overflow-hidden en el main es para proteger al header
export default function App() {
  return (
    <div className='flex flex-col h-dvh overflow-hidden'>
      <Header />
      <main className='flex-1 overflow-hidden p-4 max-w-6xl mx-auto w-full'>
        <Routes>
          <Route path='/' element={<Home />} />
        </Routes>
      </main>
    </div>
  )
}
