import { Outlet, NavLink, useLocation } from 'react-router-dom';
import { Wind, LayoutDashboard, Database, LineChart, Map, SunSnow, Info, Menu, X } from 'lucide-react';
import { useState } from 'react';
import clsx from 'clsx';

const AQI_SCALE = [
  { label: 'Good', color: '#00B050', range: '0–50' },
  { label: 'Satisfactory', color: '#92D050', range: '51–100' },
  { label: 'Moderate', color: '#FFFF00', range: '101–200' },
  { label: 'Poor', color: '#FF9900', range: '201–300' },
  { label: 'Very Poor', color: '#FF0000', range: '301–400' },
  { label: 'Severe', color: '#990000', range: '401–500' },
];

export const Layout = () => {
  const [isMobileOpen, setIsMobileOpen] = useState(false);
  const location = useLocation();

  const navItems = [
    { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
    { name: 'Models', path: '/models', icon: Database },
    { name: 'Forecast', path: '/forecast', icon: LineChart },
    { name: 'Cities', path: '/cities', icon: Map },
    { name: 'Seasonal', path: '/seasonal', icon: SunSnow },
    { name: 'About', path: '/about', icon: Info },
  ];

  const closeMobile = () => setIsMobileOpen(false);

  return (
    <div className="flex h-screen overflow-hidden bg-slate-950 font-sans text-slate-200">

      {/* Mobile Header */}
      <div className="lg:hidden absolute top-0 left-0 right-0 h-16 glass-panel border-b border-slate-800 z-50 flex items-center justify-between px-4">
        <NavLink to="/" className="flex items-center gap-2 text-indigo-400 font-bold text-xl">
          <Wind className="h-6 w-6" /> Aetheris
        </NavLink>
        <button onClick={() => setIsMobileOpen(!isMobileOpen)} className="p-2 text-slate-300">
          {isMobileOpen ? <X /> : <Menu />}
        </button>
      </div>

      {/* Sidebar Desktop & Mobile */}
      <nav className={clsx(
        "fixed inset-y-0 left-0 z-40 w-64 glass-panel border-r border-slate-800 transform transition-transform duration-300 ease-in-out lg:relative lg:translate-x-0 flex flex-col pt-16 lg:pt-0",
        isMobileOpen ? "translate-x-0" : "-translate-x-full"
      )}>
        <div className="hidden lg:flex items-center h-20 px-6 border-b border-slate-800/50">
          <NavLink to="/" className="flex items-center gap-3 text-indigo-400 font-bold text-2xl tracking-wide">
            <Wind className="h-8 w-8" /> Aetheris
          </NavLink>
        </div>

        <div className="flex-1 overflow-y-auto py-6 px-4 space-y-2">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;
            return (
              <NavLink
                key={item.path}
                to={item.path}
                onClick={closeMobile}
                className={clsx(
                  "flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200",
                  isActive
                    ? "bg-indigo-500/20 text-indigo-300 shadow-[inset_0_1px_0_0_rgba(255,255,255,0.1)] border border-indigo-500/30"
                    : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/50"
                )}
              >
                <Icon className={clsx("h-5 w-5", isActive ? "text-indigo-400" : "text-slate-500")} />
                <span className="font-semibold">{item.name}</span>
              </NavLink>
            )
          })}
        </div>

        {/* AQI Scale Legend */}
        <div className="px-4 pb-2">
          <div className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-2 px-2">AQI Scale</div>
          <div className="flex gap-[2px] rounded-lg overflow-hidden mb-2">
            {AQI_SCALE.map(s => (
              <div key={s.label} className="flex-1 h-2" style={{ backgroundColor: s.color }} title={`${s.label}: ${s.range}`} />
            ))}
          </div>
          <div className="flex justify-between text-[9px] text-slate-500 px-0.5">
            <span>0</span>
            <span>Good</span>
            <span>Moderate</span>
            <span>Severe</span>
            <span>500</span>
          </div>
        </div>

        <div className="p-4 border-t border-slate-800/50">
          <div className="flex items-center gap-2 text-xs text-emerald-500/80 font-medium bg-emerald-500/10 p-3 rounded-lg border border-emerald-500/20">
            <span className="w-2 h-2 rounded-full bg-emerald-500 pulse-ring" />
            Systems Operational
          </div>
        </div>
      </nav>

      {/* Main Content Area */}
      <main className="flex-1 relative overflow-y-auto lg:overflow-x-hidden pt-16 lg:pt-0 bg-gradient-to-br from-slate-950 to-slate-900">
        <div className="container mx-auto p-4 lg:p-8">
          <Outlet />
        </div>
      </main>

      {/* Mobile overlay */}
      {isMobileOpen && (
        <div className="lg:hidden fixed inset-0 bg-black/50 backdrop-blur-sm z-30" onClick={closeMobile} />
      )}
    </div>
  );
}
