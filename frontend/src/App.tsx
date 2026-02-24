import { Header } from './components/Header.js'
import { Route, Routes } from 'react-router'
import { lazy } from 'react'

const Home = lazy(() => import('./pages/Home.js'))

  // El overflow-hidden en el div es para proteger toda la ventana
  // El overflow-hidden en el main es para proteger al header
export default function App() {
  return (
    <>
      <Header />
      <main>
        <Routes>
          <Route path='/' element={<Home />} />
        </Routes>
      </main>
    </>
  )
}
