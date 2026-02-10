import { Header } from './components/Header.js'
import './App.css'
import { Route, Routes } from 'react-router'
import { lazy } from 'react'

const Home = lazy(() => import('./pages/Home.js'))

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
