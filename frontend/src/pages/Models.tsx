import { BarChart, Bar, XAxis, YAxis, Tooltip as RechartsTooltip, ResponsiveContainer, Cell, CartesianGrid } from 'recharts';
import { regressionResults, classificationResults, featureImportance } from '../data/modelsData';
import { Database, TrendingUp, Filter, BarChart2, Sparkles } from 'lucide-react';
import clsx from 'clsx';

export default function Models() {

  const bestReg = [...regressionResults].sort((a, b) => a.rmse - b.rmse)[0];
  const bestClf = [...classificationResults].sort((a, b) => b.f1 - a.f1)[0];

  const chartDataReg = regressionResults.map(r => ({ name: r.model, RMSE: r.rmse })).sort((a, b) => b.RMSE - a.RMSE);
  const chartDataClf = classificationResults.map(r => ({ name: r.model, F1: r.f1 })).sort((a, b) => a.F1 - b.F1);

  const chartDataFI = featureImportance.map(f => ({ name: f.feature.replace(/_/g, ' '), value: f.importance })).reverse();

  return (
    <div className="space-y-8">

      <div className="flex items-center gap-4 mb-4">
        <div className="p-3 bg-indigo-500/20 rounded-xl border border-indigo-500/30">
          <Database className="h-6 w-6 text-indigo-400" />
        </div>
        <div>
          <h1 className="text-2xl font-bold text-white">Model Comparison</h1>
          <p className="text-slate-400">Detailed performance metrics across 13 machine learning architectures.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-8">

        {/* Regression Models Section */}
        <section className="space-y-4">
          <div className="flex items-center gap-2 mb-2">
            <TrendingUp className="text-emerald-400 h-5 w-5" />
            <h2 className="text-xl font-bold text-white">Regression (Predicting AQI Value)</h2>
          </div>

          <div className="glass-panel rounded-2xl overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-sm text-left">
                <thead className="text-xs uppercase bg-slate-800/50 text-slate-400">
                  <tr>
                    <th className="px-4 py-3 rounded-tl-lg">Model</th>
                    <th className="px-4 py-3 text-right">RMSE</th>
                    <th className="px-4 py-3 text-right">MAE</th>
                    <th className="px-4 py-3 text-right">R²</th>
                    <th className="px-4 py-3 text-right rounded-tr-lg">MAPE</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/50">
                  {regressionResults.map(row => (
                    <tr key={row.model} className={clsx("hover:bg-slate-800/30 transition-colors", row.model === bestReg.model && "bg-emerald-500/5")}>
                      <td className="px-4 py-3 font-medium text-white flex items-center gap-2">
                        {row.model === bestReg.model && <span className="text-emerald-400 text-[10px] font-bold bg-emerald-500/20 px-2 py-0.5 rounded-full">BEST</span>}
                        {row.model}
                      </td>
                      <td className="px-4 py-3 text-right tabular-nums text-slate-300">{row.rmse}</td>
                      <td className="px-4 py-3 text-right tabular-nums text-slate-300">{row.mae}</td>
                      <td className="px-4 py-3 text-right tabular-nums text-slate-300">{row.r2.toFixed(4)}</td>
                      <td className="px-4 py-3 text-right tabular-nums text-slate-300">{row.mape}%</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          <div className="glass-panel p-6 rounded-2xl">
            <h3 className="text-sm font-bold text-slate-300 mb-4 flex items-center gap-2"><BarChart2 className="h-4 w-4" /> RMSE Comparison (Lower is Better)</h3>
            <div className="h-[250px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartDataReg} layout="vertical" margin={{ top: 0, right: 0, left: 30, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#334155" />
                  <XAxis type="number" stroke="#475569" tick={{ fill: '#94a3b8', fontSize: 12 }} />
                  <YAxis dataKey="name" type="category" stroke="#475569" tick={{ fill: '#94a3b8', fontSize: 11 }} width={90} />
                  <RechartsTooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155' }} cursor={{ fill: '#1e293b' }} />
                  <Bar dataKey="RMSE" radius={[0, 4, 4, 0]}>
                    {chartDataReg.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.name === bestReg.model ? '#34d399' : '#6366f1'} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </section>

        {/* Classification Models Section */}
        <section className="space-y-4">
          <div className="flex items-center gap-2 mb-2">
            <Filter className="text-indigo-400 h-5 w-5" />
            <h2 className="text-xl font-bold text-white">Classification (Predicting Category)</h2>
          </div>

          <div className="glass-panel rounded-2xl overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-sm text-left">
                <thead className="text-xs uppercase bg-slate-800/50 text-slate-400">
                  <tr>
                    <th className="px-4 py-3 rounded-tl-lg">Model</th>
                    <th className="px-4 py-3 text-right">Accuracy</th>
                    <th className="px-4 py-3 text-right">Precision</th>
                    <th className="px-4 py-3 text-right">Recall</th>
                    <th className="px-4 py-3 text-right rounded-tr-lg">F1</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/50">
                  {classificationResults.map(row => (
                    <tr key={row.model} className={clsx("hover:bg-slate-800/30 transition-colors", row.model === bestClf.model && "bg-indigo-500/5")}>
                      <td className="px-4 py-3 font-medium text-white flex items-center gap-2">
                        {row.model === bestClf.model && <span className="text-indigo-400 text-[10px] font-bold bg-indigo-500/20 px-2 py-0.5 rounded-full">BEST</span>}
                        {row.model}
                      </td>
                      <td className="px-4 py-3 text-right tabular-nums text-slate-300">{(row.accuracy * 100).toFixed(2)}%</td>
                      <td className="px-4 py-3 text-right tabular-nums text-slate-300">{(row.precision * 100).toFixed(2)}%</td>
                      <td className="px-4 py-3 text-right tabular-nums text-slate-300">{(row.recall * 100).toFixed(2)}%</td>
                      <td className="px-4 py-3 text-right tabular-nums text-slate-300">{(row.f1 * 100).toFixed(2)}%</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          <div className="glass-panel p-6 rounded-2xl">
            <h3 className="text-sm font-bold text-slate-300 mb-4 flex items-center gap-2"><BarChart2 className="h-4 w-4" /> F1 Score Comparison (Higher is Better)</h3>
            <div className="h-[250px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartDataClf} layout="vertical" margin={{ top: 0, right: 0, left: 30, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#334155" />
                  <XAxis type="number" domain={[0.99, 1]} stroke="#475569" tick={{ fill: '#94a3b8', fontSize: 12 }} />
                  <YAxis dataKey="name" type="category" stroke="#475569" tick={{ fill: '#94a3b8', fontSize: 11 }} width={90} />
                  <RechartsTooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155' }} cursor={{ fill: '#1e293b' }} />
                  <Bar dataKey="F1" radius={[0, 4, 4, 0]}>
                    {chartDataClf.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.name === bestClf.model ? '#818cf8' : '#334155'} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

        </section>

      </div>

      {/* Feature Importance — Full Width */}
      <section className="glass-panel p-6 rounded-3xl">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-2 bg-amber-500/20 rounded-lg">
            <Sparkles className="h-5 w-5 text-amber-400" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-white">Top 10 Feature Importance (LightGBM)</h2>
            <p className="text-sm text-slate-400">Which features contribute most to predicting AQI values.</p>
          </div>
        </div>
        <div className="h-[320px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartDataFI} layout="vertical" margin={{ top: 0, right: 20, left: 10, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#334155" />
              <XAxis type="number" stroke="#475569" tick={{ fill: '#94a3b8', fontSize: 12 }} tickFormatter={(v: number) => `${(v * 100).toFixed(0)}%`} />
              <YAxis dataKey="name" type="category" stroke="#475569" tick={{ fill: '#cbd5e1', fontSize: 12 }} width={140} />
              <RechartsTooltip
                contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px' }}
                formatter={(v: any) => [`${(Number(v) * 100).toFixed(1)}%`, 'Importance']}
              />
              <Bar dataKey="value" radius={[0, 6, 6, 0]}>
                {chartDataFI.map((_, index) => (
                  <Cell key={`fi-${index}`} fill={index >= chartDataFI.length - 3 ? '#f59e0b' : '#6366f1'} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
        <p className="text-xs text-slate-500 mt-4 leading-relaxed max-w-3xl">
          <strong className="text-slate-400">Note:</strong> Features like <span className="text-amber-400">pollution_risk_score</span> and <span className="text-amber-400">city_aqi_mean</span> dominate because they encode historical pollution context. Temporal features (month, day_of_week) capture seasonality patterns crucial for Indian AQI forecasting.
        </p>
      </section>
    </div>
  )
}
