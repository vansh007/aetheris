export const seasonalDistributions = [
  { season: 'Winter', good: 5, satisfactory: 20, moderate: 40, poor: 20, veryPoor: 10, severe: 5 },
  { season: 'Spring', good: 15, satisfactory: 40, moderate: 30, poor: 10, veryPoor: 4, severe: 1 },
  { season: 'Monsoon', good: 45, satisfactory: 40, moderate: 12, poor: 3, veryPoor: 0, severe: 0 },
  { season: 'Autumn', good: 10, satisfactory: 35, moderate: 35, poor: 15, veryPoor: 4, severe: 1 },
];

export const monthlyTrendData = [
  { month: 'Jan', avgAqi: 152 },
  { month: 'Feb', avgAqi: 140 },
  { month: 'Mar', avgAqi: 130 },
  { month: 'Apr', avgAqi: 110 },
  { month: 'May', avgAqi: 105 },
  { month: 'Jun', avgAqi: 85 },
  { month: 'Jul', avgAqi: 75 },
  { month: 'Aug', avgAqi: 70 },
  { month: 'Sep', avgAqi: 77 },
  { month: 'Oct', avgAqi: 120 },
  { month: 'Nov', avgAqi: 160 },
  { month: 'Dec', avgAqi: 175 },
];

export const pollutantBreakdown = [
  { name: 'PM10', value: 47, fill: '#8884d8' },
  { name: 'PM2.5', value: 25, fill: '#82ca9d' },
  { name: 'O3', value: 12, fill: '#ffc658' },
  { name: 'CO', value: 8, fill: '#ff8042' },
  { name: 'NO2', value: 5, fill: '#8dd1e1' },
  { name: 'SO2', value: 3, fill: '#a4de6c' },
];

export const dashboardTrend = Array.from({length: 30}).map((_, i) => ({
  date: `Apr ${i+1}`,
  aqi: 90 + Math.sin(i*0.5)*30 + Math.random()*20
}));
