import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Layout } from './components/Layout';
// We'll import pages as we build them, for now using placeholders
import Landing from './pages/Landing';
import Dashboard from './pages/Dashboard';
import Models from './pages/Models';
import Forecast from './pages/Forecast';
import Cities from './pages/Cities';
import Seasonal from './pages/Seasonal';
import About from './pages/About';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route element={<Layout />}>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/models" element={<Models />} />
          <Route path="/forecast" element={<Forecast />} />
          <Route path="/cities" element={<Cities />} />
          <Route path="/seasonal" element={<Seasonal />} />
          <Route path="/about" element={<About />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App;
