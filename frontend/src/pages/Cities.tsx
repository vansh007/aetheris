import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { topPollutedCities, topCleanestCities, clusterData } from '../data/citiesData';
import { getAqiBadgeStyles } from '../utils/aqiUtils';
import { Map, AlertTriangle, Building2, Trees } from 'lucide-react';
import clsx from 'clsx';

export default function Cities() {
  return (
    <div className="space-y-8">
      
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between md:items-end gap-6 mb-8">
        <div className="flex items-center gap-4">
          <div className="p-3 bg-emerald-500/20 rounded-xl border border-emerald-500/30">
            <Map className="h-6 w-6 text-emerald-400" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">Geospatial Insights</h1>
            <p className="text-slate-400">Analysis across 291 Indian cities showcasing hotspots and clean zones.</p>
          </div>
        </div>
        
        {/* Anomaly Highlight */}
        <div className="glass-panel px-5 py-3 rounded-xl border-orange-500/30 flex items-center gap-3">
           <AlertTriangle className="text-orange-400 h-5 w-5" />
           <div>
             <div className="text-xs text-slate-400 uppercase tracking-widest font-semibold">Anomaly Warning</div>
             <div className="text-white font-bold text-sm">4,538 anomalies detected (2.0%)</div>
           </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        <section className="glass-panel p-6 rounded-3xl">
          <h2 className="text-lg font-bold text-white mb-6 flex items-center gap-2"><Building2 className="text-rose-400 h-5 w-5"/> Top 10 Polluted Cities</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead className="text-xs uppercase bg-slate-800/50 text-slate-400">
                <tr>
                  <th className="px-4 py-3 rounded-tl-lg">Rank</th>
                  <th className="px-4 py-3">City</th>
                  <th className="px-4 py-3">State</th>
                  <th className="px-4 py-3">Avg AQI</th>
                  <th className="px-4 py-3 rounded-tr-lg">Category</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/50">
                {topPollutedCities.map((row) => (
                  <tr key={row.rank} className="hover:bg-slate-800/30 transition-colors">
                    <td className="px-4 py-3 font-semibold text-slate-300">#{row.rank}</td>
                    <td className="px-4 py-3 font-bold text-white">{row.city}</td>
                    <td className="px-4 py-3 text-slate-400">{row.state}</td>
                    <td className="px-4 py-3 font-mono">{row.avgAqi}</td>
                    <td className="px-4 py-3">
                      <span className={clsx("px-2 py-1 text-[10px] font-bold uppercase tracking-wider rounded-md", getAqiBadgeStyles(row.category))}>
                        {row.category}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        <section className="glass-panel p-6 rounded-3xl">
          <h2 className="text-lg font-bold text-white mb-6 flex items-center gap-2"><Trees className="text-emerald-400 h-5 w-5"/> Top 10 Cleanest Cities</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-sm text-left">
              <thead className="text-xs uppercase bg-slate-800/50 text-slate-400">
                <tr>
                  <th className="px-4 py-3 rounded-tl-lg">Rank</th>
                  <th className="px-4 py-3">City</th>
                  <th className="px-4 py-3">State</th>
                  <th className="px-4 py-3">Avg AQI</th>
                  <th className="px-4 py-3 rounded-tr-lg">Category</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/50">
                {topCleanestCities.map((row) => (
                  <tr key={row.rank} className="hover:bg-emerald-900/10 transition-colors">
                    <td className="px-4 py-3 font-semibold text-slate-300">#{row.rank}</td>
                    <td className="px-4 py-3 font-bold text-white">{row.city}</td>
                    <td className="px-4 py-3 text-slate-400">{row.state}</td>
                    <td className="px-4 py-3 font-mono">{row.avgAqi}</td>
                    <td className="px-4 py-3">
                      <span className={clsx("px-2 py-1 text-[10px] font-bold uppercase tracking-wider rounded-md", getAqiBadgeStyles(row.category))}>
                        {row.category}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

      </div>

      <section className="glass-panel p-6 rounded-3xl">
         <div className="flex flex-col md:flex-row md:items-center justify-between mb-6">
           <h2 className="text-xl font-bold text-white">City Clustering Visualization (K-Means)</h2>
           <div className="flex items-center gap-4 text-sm mt-3 md:mt-0">
              <div className="flex items-center gap-2"><div className="w-3 h-3 rounded-full bg-emerald-400" /> Cluster 0 (Cleaner)</div>
              <div className="flex items-center gap-2"><div className="w-3 h-3 rounded-full bg-rose-500" /> Cluster 1 (Polluted)</div>
           </div>
         </div>
         <p className="text-slate-400 text-sm mb-6 max-w-3xl">
           The optimal number of clusters computed was 2 (silhouette score = 0.209), indicating pollution profiles don't form perfectly separated islands but exist on a continuum leaning into the Indo-Gangetic basin.
         </p>
         
         <div className="h-[400px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                <XAxis type="number" dataKey="meanAqi" name="Mean AQI" stroke="#475569" tick={{fill: '#94a3b8'}} label={{ value: 'Mean AQI Range', position: 'insideBottom', offset: -10, fill: '#64748b' }} />
                <YAxis type="number" dataKey="stdDev" name="Volatility (Std Dev)" stroke="#475569" tick={{fill: '#94a3b8'}} label={{ value: 'Volatility (Std. Dev)', angle: -90, position: 'insideLeft', fill: '#64748b', offset: 0 }} />
                <Tooltip cursor={{ strokeDasharray: '3 3', stroke: '#cbd5e1' }} contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px' }} />
                <Scatter name="Cluster 0" data={clusterData.filter(d => d.cluster.includes('0'))} fill="#34d399" opacity={0.6} />
                <Scatter name="Cluster 1" data={clusterData.filter(d => d.cluster.includes('1'))} fill="#f43f5e" opacity={0.6} />
              </ScatterChart>
            </ResponsiveContainer>
         </div>
      </section>

    </div>
  )
}
