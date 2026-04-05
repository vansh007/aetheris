import { Info, Database, Code2, Sparkles, Server, Network } from 'lucide-react';

export default function About() {
  return (
    <div className="max-w-4xl mx-auto space-y-12 pb-12">
      
      {/* Hero */}
      <section className="text-center pt-8">
        <div className="inline-flex p-4 bg-indigo-500/20 rounded-full border border-indigo-500/30 mb-6">
          <Info className="h-8 w-8 text-indigo-400" />
        </div>
        <h1 className="text-4xl font-black text-white mb-4">About Aetheris</h1>
        <p className="text-xl text-slate-400 leading-relaxed">
          The Intelligent Air Quality Prediction & Advisory System. <br className="hidden md:block"/>
          Built to combine atmospheric data with machine learning for precise, hyperlocal AQI forecasting.
        </p>
      </section>

      {/* Dataset & Scale */}
      <section className="glass-panel p-8 rounded-3xl relative overflow-hidden">
        <div className="absolute top-0 right-0 p-8 opacity-10">
          <Database className="w-48 h-48 text-indigo-400" />
        </div>
        <div className="relative z-10">
          <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
            <span className="p-2 bg-emerald-500/20 rounded-lg text-emerald-400"><Database className="h-5 w-5"/></span>
            Dataset & Scale
          </h2>
          <p className="text-slate-300 mb-8 leading-relaxed max-w-2xl">
            Aetheris was trained on the expansive <strong>India Air Quality Index (AQI) Dataset (2022–2025)</strong>. It models real-world pollution volatility by parsing extreme class imbalances and geographical disparities.
          </p>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-slate-800/50 p-4 rounded-xl border border-slate-700/50">
              <div className="text-3xl font-black text-white mb-1">235K+</div>
              <div className="text-xs text-slate-400 uppercase font-semibold">Records Analyzed</div>
            </div>
            <div className="bg-slate-800/50 p-4 rounded-xl border border-slate-700/50">
              <div className="text-3xl font-black text-white mb-1">291</div>
              <div className="text-xs text-slate-400 uppercase font-semibold">Indian Cities</div>
            </div>
            <div className="bg-slate-800/50 p-4 rounded-xl border border-slate-700/50">
              <div className="text-3xl font-black text-white mb-1">32</div>
              <div className="text-xs text-slate-400 uppercase font-semibold">States & UTs</div>
            </div>
            <div className="bg-slate-800/50 p-4 rounded-xl border border-slate-700/50">
              <div className="text-3xl font-black text-white mb-1">45K+</div>
              <div className="text-xs text-slate-400 uppercase font-semibold">Test Validation Set</div>
            </div>
          </div>
        </div>
      </section>

      {/* Architecture Flow */}
      <section className="glass-panel p-8 rounded-3xl">
        <h2 className="text-2xl font-bold text-white mb-8 flex items-center gap-3">
          <span className="p-2 bg-sky-500/20 rounded-lg text-sky-400"><Network className="h-5 w-5"/></span>
          System Architecture
        </h2>
        
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex-1 w-full bg-slate-800/40 border border-slate-700/50 p-6 rounded-2xl text-center shadow-lg">
            <Database className="h-8 w-8 text-slate-400 mx-auto mb-3" />
            <h3 className="font-bold text-white mb-1">Data Pipeline</h3>
            <p className="text-xs text-slate-400">Cleaning, SMOTE, Targets</p>
          </div>
          
          <div className="hidden md:block w-8 h-[2px] bg-indigo-500/50 relative">
             <div className="absolute right-0 top-1/2 -translate-y-1/2 w-2 h-2 rounded-full bg-indigo-400" />
          </div>
          
          <div className="flex-1 w-full bg-slate-800/40 border border-slate-700/50 p-6 rounded-2xl text-center shadow-lg">
            <Sparkles className="h-8 w-8 text-indigo-400 mx-auto mb-3" />
            <h3 className="font-bold text-white mb-1">ML Engine</h3>
            <p className="text-xs text-slate-400">LightGBM, XGBoost, ARIMA</p>
          </div>
          
          <div className="hidden md:block w-8 h-[2px] bg-indigo-500/50 relative">
             <div className="absolute right-0 top-1/2 -translate-y-1/2 w-2 h-2 rounded-full bg-indigo-400" />
          </div>
          
          <div className="flex-1 w-full bg-slate-800/40 border border-slate-700/50 p-6 rounded-2xl text-center shadow-lg">
            <Server className="h-8 w-8 text-emerald-400 mx-auto mb-3" />
            <h3 className="font-bold text-white mb-1">FastAPI Backend</h3>
            <p className="text-xs text-slate-400">Predictions & Health Logic</p>
          </div>

          <div className="hidden md:block w-8 h-[2px] bg-indigo-500/50 relative">
             <div className="absolute right-0 top-1/2 -translate-y-1/2 w-2 h-2 rounded-full bg-indigo-400" />
          </div>
          
          <div className="flex-1 w-full bg-indigo-500/10 border border-indigo-500/30 p-6 rounded-2xl text-center shadow-[0_0_20px_rgba(99,102,241,0.15)] ring-1 ring-indigo-500/50 relative overflow-hidden">
            <Code2 className="h-8 w-8 text-indigo-300 mx-auto mb-3" />
            <h3 className="font-bold text-white mb-1">React Client</h3>
            <p className="text-xs text-indigo-200/80">Dashboard & Insights UI</p>
          </div>
        </div>
      </section>

      {/* Tech Stack */}
      <section className="glass-panel p-8 rounded-3xl">
        <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
          <span className="p-2 bg-purple-500/20 rounded-lg text-purple-400"><Code2 className="h-5 w-5"/></span>
          Technology Stack
        </h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
           {['Python Data Stack', 'scikit-learn', 'XGBoost / LightGBM / CatBoost', 'ARIMA / Prophet', 'FastAPI', 'React 18 + Vite', 'Tailwind CSS', 'Recharts'].map(tech => (
             <div key={tech} className="bg-slate-900/50 py-3 px-4 rounded-lg border border-slate-800 text-sm font-medium text-slate-300 text-center">
               {tech}
             </div>
           ))}
        </div>
      </section>

      {/* Team / Credits */}
      <section className="text-center pt-4">
         <p className="text-slate-500 font-medium">Built as an academic endeavor bridging Environmental Science and MLOps.</p>
         <div className="mt-4 inline-block px-6 py-2 rounded-full glass-panel text-sm text-slate-400 font-medium">Aetheris v1.0.0</div>
      </section>

    </div>
  )
}
