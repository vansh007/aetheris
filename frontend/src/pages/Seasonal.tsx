import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { seasonalDistributions, monthlyTrendData } from '../data/seasonalData';
import { SunSnow, Info, Sparkles } from 'lucide-react';

export default function Seasonal() {
  return (
    <div className="space-y-8">
      
      <div className="flex items-center gap-4 mb-4">
        <div className="p-3 bg-pink-500/20 rounded-xl border border-pink-500/30">
          <SunSnow className="h-6 w-6 text-pink-400" />
        </div>
        <div>
          <h1 className="text-2xl font-bold text-white">Seasonal Anomalies & Trends</h1>
          <p className="text-slate-400">Discover macroscopic patterns driving Indian air quality across the calendar year.</p>
        </div>
      </div>

      {/* Insight Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="glass-panel p-6 rounded-2xl border-t-2 border-t-sky-400 relative overflow-hidden group">
          <Info className="absolute top-4 right-4 h-6 w-6 text-slate-600 group-hover:text-sky-400 transition-colors" />
          <h3 className="text-sm font-bold text-slate-300 uppercase tracking-wider mb-2">Winter Phenomenon</h3>
          <p className="text-white font-medium text-lg">Winter is <span className="text-rose-400 font-bold">2x more polluted</span> than the Monsoon season across the Indo-Gangetic Basin.</p>
        </div>
        <div className="glass-panel p-6 rounded-2xl border-t-2 border-t-indigo-400 relative overflow-hidden group">
          <Info className="absolute top-4 right-4 h-6 w-6 text-slate-600 group-hover:text-indigo-400 transition-colors" />
          <h3 className="text-sm font-bold text-slate-300 uppercase tracking-wider mb-2">Particulate Dominance</h3>
          <p className="text-white font-medium text-lg">PM10 constitutes the primary threat in <span className="text-indigo-400 font-bold">47%</span> of all severely dangerous recordings.</p>
        </div>
        <div className="glass-panel p-6 rounded-2xl border-t-2 border-t-emerald-400 relative overflow-hidden group">
          <Sparkles className="absolute top-4 right-4 h-6 w-6 text-slate-600 group-hover:text-emerald-400 transition-colors" />
          <h3 className="text-sm font-bold text-slate-300 uppercase tracking-wider mb-2">Imbalance Ratio</h3>
          <p className="text-white font-medium text-lg">There is a staggering <span className="text-emerald-400 font-bold">160:1 ratio</span> separating Satisfactory readings from Severe.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        {/* Category Stacked Bar */}
        <section className="glass-panel p-6 rounded-3xl">
          <h2 className="text-lg font-bold text-white mb-6">Seasonal Category Distribution</h2>
          <div className="h-[350px] w-full">
             <ResponsiveContainer width="100%" height="100%">
                <BarChart data={seasonalDistributions} layout="vertical" margin={{ top: 0, right: 0, left: 10, bottom: 0 }}>
                   <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#334155" />
                   <XAxis type="number" max={100} stroke="#475569" tick={{fill: '#94a3b8', fontSize: 12}} />
                   <YAxis dataKey="season" type="category" stroke="#475569" tick={{fill: '#94a3b8', fontSize: 12}} />
                   <Tooltip cursor={{fill: '#1e293b'}} contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', color: '#fff' }} />
                   <Legend wrapperStyle={{ paddingTop: '20px' }} />
                   
                   <Bar dataKey="good" name="Good" stackId="a" fill="#00B050" />
                   <Bar dataKey="satisfactory" name="Satisfactory" stackId="a" fill="#92D050" />
                   <Bar dataKey="moderate" name="Moderate" stackId="a" fill="#FFFF00" />
                   <Bar dataKey="poor" name="Poor" stackId="a" fill="#FF9900" />
                   <Bar dataKey="veryPoor" name="Very Poor" stackId="a" fill="#FF0000" />
                   <Bar dataKey="severe" name="Severe" stackId="a" fill="#990000" radius={[0, 4, 4, 0]} />
                </BarChart>
             </ResponsiveContainer>
          </div>
        </section>

        {/* Monthly Trend */}
        <section className="glass-panel p-6 rounded-3xl">
          <h2 className="text-lg font-bold text-white mb-6">Annual Aggregate Trend Overlay</h2>
          <div className="h-[350px] w-full">
             <ResponsiveContainer width="100%" height="100%">
                <LineChart data={monthlyTrendData} margin={{ top: 20, right: 20, left: -20, bottom: 0 }}>
                   <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#334155" />
                   <XAxis dataKey="month" stroke="#475569" tick={{fill: '#94a3b8', fontSize: 12}} />
                   <YAxis stroke="#475569" tick={{fill: '#94a3b8', fontSize: 12}} />
                   <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', color: '#fff' }} />
                   <Line type="monotone" dataKey="avgAqi" name="Avg AQI" stroke="#60a5fa" strokeWidth={3} dot={{r: 5, fill: '#3b82f6', stroke: '#1e3a8a'}} activeDot={{r: 8}} />
                </LineChart>
             </ResponsiveContainer>
          </div>
        </section>
        
      </div>
    </div>
  )
}
