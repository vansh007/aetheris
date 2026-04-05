export const forecastData = [
  { date: 'May 1', aqi: 205, category: 'Poor', advice: 'Health warnings of emergency conditions. The entire population is more likely to be affected.', icon: 'warning' },
  { date: 'May 2', aqi: 210, category: 'Poor', advice: 'Health alert: everyone may experience more serious health effects.', icon: 'warning' },
  { date: 'May 3', aqi: 210, category: 'Poor', advice: 'Health alert: everyone may experience more serious health effects.', icon: 'warning' },
  { date: 'May 4', aqi: 212, category: 'Poor', advice: 'Health alert: everyone may experience more serious health effects.', icon: 'warning' },
  { date: 'May 5', aqi: 214, category: 'Poor', advice: 'Health alert: everyone may experience more serious health effects.', icon: 'warning' },
  { date: 'May 6', aqi: 214, category: 'Poor', advice: 'Health alert: everyone may experience more serious health effects.', icon: 'warning' },
  { date: 'May 7', aqi: 215, category: 'Poor', advice: 'Health alert: everyone may experience more serious health effects.', icon: 'warning' }
];

export const prophetVsArima = [
  { model: 'ARIMA(5,1,2)', rmse: 50.73, mae: 43.41 },
  { model: 'Prophet', rmse: 51.56, mae: 43.67 }
];

export const chartTimeSeriesData = [
  ...Array.from({length: 60}).map((_, i) => ({ day: `Day -${60-i}`, observed: 100 + Math.random() * 80, forecast: null })),
  ...Array.from({length: 7}).map((_, i) => ({ day: `Day +${i+1}`, observed: null, forecast: 205 + i * 1.5 }))
];

// Time-series decomposition data (365 days — simulating annual seasonality)
export const decompositionData = Array.from({ length: 120 }).map((_, i) => {
  const month = (i / 10); // ~12 months
  const trend = 130 + (i < 60 ? i * 0.3 : (120 - i) * 0.3); // arch-shaped trend
  const seasonal = 40 * Math.sin((month - 1) * Math.PI / 6); // winter high, monsoon low
  const residual = (Math.random() - 0.5) * 30;
  const observed = trend + seasonal + residual;
  return {
    day: i + 1,
    observed: Math.round(observed * 10) / 10,
    trend: Math.round(trend * 10) / 10,
    seasonal: Math.round(seasonal * 10) / 10,
    residual: Math.round(residual * 10) / 10,
  };
});
