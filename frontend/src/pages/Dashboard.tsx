import { useState, useEffect } from 'react';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, Tooltip as RechartsTooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { MapPin, Calendar, HeartPulse, CheckCircle, AlertTriangle, ShieldAlert, Activity, TrendingUp, Loader2 } from 'lucide-react';
import { allCities, cityProfiles } from '../data/citiesData';
import { dashboardTrend, pollutantBreakdown } from '../data/seasonalData';
import { getAqiColor, getAqiCategory, getAqiBadgeStyles } from '../utils/aqiUtils';
import clsx from 'clsx';

const DEFAULT_PROFILE = { aqi: 142, primaryPollutant: "PM10", riskScore: 41.2, healthAdvice: "People with heart or lung disease, older adults, and children should reduce prolonged or heavy exertion.", riskLevel: "Moderate hazard for sensitive groups.", bestTime: "Early morning (5 AM - 7 AM) or late evening after 8 PM.", meanAqi: 124.5, maxAqi: 430, minAqi: 32, records: 1284 };

export default function Dashboard() {
  const [selectedCity, setSelectedCity] = useState("Delhi");
  const [prediction, setPrediction] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(false);

  // Static historical profile fallback for bottom stats
  const profile = cityProfiles[selectedCity] || DEFAULT_PROFILE;

  useEffect(() => {
    let isMounted = true;
    const fetchPrediction = async () => {
      setLoading(true);
      setError(false);
      try {
        const response = await axios.post('/api/predict', {
          city: selectedCity,
          state: "Unknown", // the backend now handles city-based lookup directly via area
          date: new Date().toISOString().split('T')[0],
          primary_pollutant: "PM10"
        });
        
        if (isMounted) {
          setPrediction(response.data);
          setLoading(false);
        }
      } catch (err) {
        console.error("API Prediction Error:", err);
        if (isMounted) {
          setError(true);
          setLoading(false);
        }
      }
    };
    
    fetchPrediction();
    
    return () => { isMounted = false; };
  }, [selectedCity]);

  // Derived Values
  const currentAqi = prediction ? Math.round(prediction.predicted_aqi) : profile.aqi;
  const category = prediction ? prediction.category : getAqiCategory(currentAqi);
  const badgeStyle = getAqiBadgeStyles(category);
  const color = getAqiColor(currentAqi);
  const healthAdvice = prediction ? prediction.health_advice : profile.healthAdvice;
  const riskLevel = prediction ? prediction.risk : profile.riskLevel;
  const bestTime = prediction ? prediction.best_time_outside : profile.bestTime;

  return (
    <div className="space-y-6">

      {/* Top Bar */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 glass-panel p-4 rounded-2xl">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-indigo-500/20 rounded-lg"><MapPin className="text-indigo-400 h-5 w-5" /></div>
          <select
            value={selectedCity}
            onChange={e => setSelectedCity(e.target.value)}
            className="bg-transparent text-xl font-bold text-white outline-none border-b border-indigo-500/30 cursor-pointer pb-1"
          >
            {allCities.slice(0, 50).map(city => <option key={city} className="bg-slate-900">{city}</option>)}
          </select>
        </div>
        <div className="flex items-center gap-2 text-slate-400 font-medium">
          <Calendar className="h-4 w-4" /> Today: {new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
        </div>
      </div>

      {error && (
        <div className="bg-rose-500/20 border border-rose-500/50 text-rose-200 p-4 rounded-xl flex items-center justify-center gap-2">
          <AlertTriangle className="h-5 w-5" /> 
          Could not connect to the ML Prediction Engine. Showing historical mock data.
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

        {/* Main AQI Display */}
        <div className="glass-panel p-8 rounded-3xl flex flex-col items-center justify-center text-center relative overflow-hidden shadow-2xl group">
          <div className="absolute top-0 right-0 w-64 h-64 opacity-20 blur-[100px] rounded-full transition-colors duration-700" style={{ backgroundColor: color }} />

          <h2 className="text-slate-400 font-semibold mb-2 uppercase tracking-widest text-sm z-10 flex items-center gap-2">
            <Activity className="h-4 w-4" /> Current AQI Index
            {loading && <Loader2 className="h-3 w-3 animate-spin text-indigo-400" />}
          </h2>
          
          <div className={clsx("text-8xl font-black text-white my-4 tracking-tighter drop-shadow-2xl z-10 transition-all duration-500", loading ? "opacity-50 blur-sm scale-95" : "opacity-100 scale-100")}>
            {currentAqi}
          </div>
          <div className={clsx("px-6 py-2 rounded-full font-bold uppercase tracking-wider text-sm shadow-xl z-10 mb-4 transition-colors duration-500", badgeStyle)}>
            {category}
          </div>

          <div className="w-full mt-4 pt-4 border-t border-slate-800/50 flex justify-between z-10 hidden sm:flex">
            <div className="text-center">
              <div className="text-slate-400 text-xs uppercase mb-1">Risk Score</div>
              <div className="font-bold text-white">{profile.riskScore} / 100</div>
            </div>
            <div className="text-center">
              <div className="text-slate-400 text-xs uppercase mb-1">Primary Pollutant</div>
              <div className="font-bold text-white">{profile.primaryPollutant}</div>
            </div>
          </div>
        </div>

        {/* Health Advisory */}
        <div className="lg:col-span-2 glass-panel p-6 sm:p-8 rounded-3xl relative overflow-hidden flex flex-col justify-center">
          <div className="flex items-center gap-3 mb-6">
            <HeartPulse className="h-6 w-6 text-pink-500" />
            <h2 className="text-xl font-bold text-white">Health Advisory — {selectedCity}</h2>
          </div>

          <div className={clsx("grid grid-cols-1 md:grid-cols-2 gap-6 transition-all duration-500", loading ? "opacity-50 blur-sm relative" : "opacity-100")}>
            {loading && <div className="absolute inset-0 flex items-center justify-center z-20"><Loader2 className="h-8 w-8 animate-spin text-indigo-400" /></div>}
            <div className="bg-slate-800/40 p-5 rounded-2xl border border-slate-700/50 flex gap-4 hover:border-slate-600 transition-colors">
              <ShieldAlert className={clsx("h-8 w-8 shrink-0", currentAqi <= 100 ? "text-emerald-400" : currentAqi <= 200 ? "text-yellow-400" : "text-rose-400")} />
              <div>
                <h3 className="font-bold text-white mb-2">Message</h3>
                <p className="text-sm text-slate-400">{healthAdvice}</p>
              </div>
            </div>
            <div className="bg-slate-800/40 p-5 rounded-2xl border border-slate-700/50 flex gap-4 hover:border-slate-600 transition-colors">
              <AlertTriangle className="h-8 w-8 text-orange-400 shrink-0" />
              <div>
                <h3 className="font-bold text-white mb-2">Risk Level</h3>
                <p className="text-sm text-slate-400">{riskLevel}</p>
              </div>
            </div>
            <div className="md:col-span-2 bg-indigo-500/10 p-5 rounded-2xl border border-indigo-500/20 flex gap-4 items-center hover:border-indigo-500/40 transition-colors">
              <CheckCircle className="h-8 w-8 text-indigo-400 shrink-0" />
              <div>
                <h3 className="font-bold text-white">Best time to go outside</h3>
                <p className="text-sm text-indigo-200/80">{bestTime}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Charts & Stats */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">

        {/* Trend line */}
        <div className="lg:col-span-2 glass-panel p-6 rounded-3xl hover:border-slate-700 transition-colors">
          <h3 className="text-lg font-bold text-white mb-6 flex items-center gap-2">
            <TrendingUp className="h-5 w-5 text-indigo-400" /> 30-Day AQI Trend ({selectedCity})
          </h3>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={dashboardTrend.map(d => ({...d, aqi: d.aqi * (profile.meanAqi / 124.5)}))}>
                <XAxis dataKey="date" stroke="#475569" tick={{ fill: '#94a3b8', fontSize: 12 }} />
                <YAxis stroke="#475569" tick={{ fill: '#94a3b8', fontSize: 12 }} />
                <RechartsTooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', color: '#fff' }}
                />
                <Line type="monotone" dataKey="aqi" stroke="#818cf8" strokeWidth={3} dot={false} activeDot={{ r: 6 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Pollutants Donut */}
        <div className="glass-panel p-6 rounded-3xl flex flex-col hover:border-slate-700 transition-colors">
          <h3 className="text-lg font-bold text-white mb-4">Pollutant Breakdown</h3>
          <div className="flex-1 min-h-[220px] relative">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={pollutantBreakdown}
                  innerRadius={60}
                  outerRadius={80}
                  paddingAngle={5}
                  dataKey="value"
                  stroke="none"
                >
                  {pollutantBreakdown.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.fill} />
                  ))}
                </Pie>
                <RechartsTooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155' }} />
              </PieChart>
            </ResponsiveContainer>
            <div className="absolute inset-0 flex items-center justify-center pointer-events-none flex-col">
              <span className="text-2xl font-black text-white">47%</span>
              <span className="text-xs text-slate-400">PM10</span>
            </div>
          </div>
          <div className="grid grid-cols-2 gap-2 mt-4">
            {pollutantBreakdown.slice(0, 4).map(p => (
              <div key={p.name} className="flex items-center gap-2 text-xs text-slate-300">
                <div className="w-3 h-3 rounded-full" style={{ backgroundColor: p.fill }} />
                {p.name}: {p.value}%
              </div>
            ))}
          </div>
        </div>

      </div>

      {/* Quick Stats Row - Dynamic */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { label: 'Mean AQI', val: profile.meanAqi.toFixed(1), icon: '📊' },
          { label: 'Max AQI', val: String(profile.maxAqi), icon: '🔺' },
          { label: 'Min AQI', val: String(profile.minAqi), icon: '🔻' },
          { label: 'Total Records', val: profile.records.toLocaleString(), icon: '📁' },
        ].map(s => (
          <div key={s.label} className="glass-panel p-5 rounded-2xl flex flex-col justify-center items-center text-center hover:border-slate-700 transition-colors group">
            <span className="text-lg mb-1">{s.icon}</span>
            <span className="text-sm text-slate-400 mb-1">{s.label}</span>
            <span className="text-2xl font-bold text-white group-hover:text-indigo-300 transition-colors">{s.val}</span>
          </div>
        ))}
      </div>

    </div>
  )
}
