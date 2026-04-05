import { Link } from 'react-router-dom';
import { Wind, Activity, BarChart2, ShieldAlert, ArrowRight } from 'lucide-react';
import clsx from 'clsx';
import { useEffect, useState } from 'react';

// A simple animated gauge for the hero
const AQIGauge = () => {
  const [value, setValue] = useState(0);

  useEffect(() => {
    // Animate up to 142 (Moderate)
    const timer = setTimeout(() => setValue(142), 500);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="relative w-64 h-64 flex flex-col items-center justify-center rounded-full border-8 border-slate-800 bg-slate-900/50 shadow-2xl backdrop-blur-sm overflow-hidden group">
      <div className={clsx(
        "absolute inset-0 opacity-20 transition-all duration-1000",
        value > 0 ? "bg-[#FFFF00]" : "bg-transparent"
      )} />
      <div className="z-10 text-center">
        <Wind className="mx-auto h-10 w-10 text-yellow-400 mb-2 animate-pulse" />
        <div className="text-6xl font-black tracking-tighter text-white">
          {value}
        </div>
        <div className="text-lg font-semibold text-yellow-400 uppercase tracking-widest mt-1">Moderate</div>
        <div className="text-xs text-slate-400 mt-2">New Delhi, India</div>
      </div>
    </div>
  )
}

const FeatureCard = ({ icon: Icon, title, desc, to, colorClass }: any) => (
  <Link to={to} className="group relative block p-8 glass-panel rounded-2xl hover:-translate-y-2 transition-all duration-300 hover:shadow-indigo-500/10 hover:shadow-2xl overflow-hidden">
    <div className="absolute inset-0 bg-gradient-to-br from-slate-800/0 to-slate-800/50 opacity-0 group-hover:opacity-100 transition-opacity" />
    <div className={clsx("w-14 h-14 rounded-xl flex items-center justify-center mb-6 shadow-inner", colorClass)}>
      <Icon className="h-7 w-7 text-white" />
    </div>
    <h3 className="text-xl font-bold text-white mb-3 group-hover:text-indigo-300 transition-colors">{title}</h3>
    <p className="text-slate-400 leading-relaxed mb-6">
      {desc}
    </p>
    <div className="flex items-center text-indigo-400 font-semibold group-hover:gap-3 transition-all">
      Explore <ArrowRight className="h-4 w-4 ml-2" />
    </div>
  </Link>
)

export default function Landing() {
  return (
    <div className="min-h-screen bg-slate-950 flex flex-col relative overflow-hidden">
      {/* Background Decor */}
      <div className="absolute top-0 right-0 w-[800px] h-[800px] bg-indigo-500/10 rounded-full blur-[120px] -translate-y-1/2 translate-x-1/3" />
      <div className="absolute bottom-0 left-0 w-[600px] h-[600px] bg-emerald-500/5 rounded-full blur-[100px] translate-y-1/3 -translate-x-1/3" />

      {/* Header */}
      <header className="absolute top-0 w-full p-6 z-50 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="bg-indigo-500/20 p-2 rounded-lg border border-indigo-500/30">
            <Wind className="h-6 w-6 text-indigo-400" />
          </div>
          <span className="text-2xl font-black tracking-wider bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400">
            AETHERIS
          </span>
        </div>
        <Link to="/dashboard" className="px-6 py-2.5 rounded-full bg-indigo-600 hover:bg-indigo-500 text-white font-semibold transition-all shadow-lg hover:shadow-indigo-500/25">
          Open Dashboard
        </Link>
      </header>

      {/* Hero Section */}
      <main className="flex-1 flex flex-col items-center justify-center z-10 px-4 mt-20 lg:mt-0">
        <div className="flex flex-col lg:flex-row items-center justify-between w-full max-w-6xl gap-16">
          <div className="flex-1 text-center lg:text-left">
            <div className="inline-block px-4 py-1.5 rounded-full bg-slate-800/50 border border-slate-700 text-indigo-300 font-medium text-sm mb-6 shadow-inner backdrop-blur-md">
              Intelligent Air Quality Prediction
            </div>
            <h1 className="text-5xl lg:text-7xl font-black text-white leading-tight tracking-tight mb-6 drop-shadow-lg">
              Breathe Smarter. <br />
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-emerald-400">
                Live Better.
              </span>
            </h1>
            <p className="text-xl text-slate-400 max-w-2xl mx-auto lg:mx-0 mb-10 leading-relaxed">
              Advanced machine learning meets real-time environmental data to give you pinpoint accurate AQI forecasts and actionable health advisories across 291 Indian cities.
            </p>
            <div className="flex flex-col sm:flex-row items-center gap-4 justify-center lg:justify-start">
              <Link to="/dashboard" className="w-full sm:w-auto px-8 py-4 rounded-xl bg-white text-slate-950 font-bold hover:bg-indigo-50 transition-colors flex items-center justify-center gap-2 shadow-xl">
                Get Started <ArrowRight className="h-5 w-5" />
              </Link>
              <Link to="/about" className="w-full sm:w-auto px-8 py-4 rounded-xl glass-panel text-white font-bold hover:bg-slate-800 transition-colors flex items-center justify-center gap-2">
                How it Works
              </Link>
            </div>
          </div>

          <div className="flex-1 flex justify-center lg:justify-end relative">
            <div className="absolute inset-0 bg-indigo-500/20 blur-[80px] rounded-full" />
            <AQIGauge />
          </div>
        </div>

        {/* Feature Cards Grid */}
        <div className="w-full max-w-6xl mt-32 mb-20 grid grid-cols-1 md:grid-cols-3 gap-6">
          <FeatureCard
            icon={Activity}
            title="Predict AQI"
            desc="Leverage our state-of-the-art LightGBM models to forecast hyper-local air quality with high precision."
            to="/dashboard"
            colorClass="bg-gradient-to-br from-emerald-500 to-green-600"
          />
          <FeatureCard
            icon={BarChart2}
            title="Analyze Trends"
            desc="Explore seasonal patterns, identify pollution hotspots, and analyze long-term historical data."
            to="/cities"
            colorClass="bg-gradient-to-br from-indigo-500 to-blue-600"
          />
          <FeatureCard
            icon={ShieldAlert}
            title="Health Advisory"
            desc="Receive instant risk assessments and personalized advice on outdoor activities based on predictive models."
            to="/forecast"
            colorClass="bg-gradient-to-br from-orange-500 to-red-600"
          />
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800/50 py-8 px-6 text-center z-10 glass-panel">
        <p className="text-slate-500 font-medium">
          Aetheris © 2026. Data sourced from India Air Quality Index Dataset (2022–2025).
        </p>
      </footer>
    </div>
  )
}
