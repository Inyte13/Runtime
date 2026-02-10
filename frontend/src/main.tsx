import { createRoot } from 'react-dom/client'
import './App.css'
import { BrowserRouter } from 'react-router'
import App from './App'

createRoot(document.getElementById('root')).render(
  <BrowserRouter>
    <App />
  </BrowserRouter>
)
