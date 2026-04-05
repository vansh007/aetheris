export const topPollutedCities = [
  { rank: 1, city: 'Delhi', state: 'Delhi', avgAqi: 247, category: 'Poor' },
  { rank: 2, city: 'Patna', state: 'Bihar', avgAqi: 212, category: 'Poor' },
  { rank: 3, city: 'Bhiwadi', state: 'Rajasthan', avgAqi: 204, category: 'Poor' },
  { rank: 4, city: 'Ghaziabad', state: 'Uttar Pradesh', avgAqi: 198, category: 'Moderate' },
  { rank: 5, city: 'Faridabad', state: 'Haryana', avgAqi: 193, category: 'Moderate' },
  { rank: 6, city: 'Nagaur', state: 'Rajasthan', avgAqi: 191, category: 'Moderate' },
  { rank: 7, city: 'Rohtak', state: 'Haryana', avgAqi: 188, category: 'Moderate' },
  { rank: 8, city: 'Greater Noida', state: 'Uttar Pradesh', avgAqi: 187, category: 'Moderate' },
  { rank: 9, city: 'Pali', state: 'Rajasthan', avgAqi: 186, category: 'Moderate' },
  { rank: 10, city: 'Sawai Madhopur', state: 'Rajasthan', avgAqi: 184, category: 'Moderate' },
];

export const topCleanestCities = [
  { rank: 1, city: 'Aizawl', state: 'Mizoram', avgAqi: 25, category: 'Good' },
  { rank: 2, city: 'Shillong', state: 'Meghalaya', avgAqi: 31, category: 'Good' },
  { rank: 3, city: 'Mysuru', state: 'Karnataka', avgAqi: 38, category: 'Good' },
  { rank: 4, city: 'Chamarajanagar', state: 'Karnataka', avgAqi: 41, category: 'Good' },
  { rank: 5, city: 'Thrissur', state: 'Kerala', avgAqi: 45, category: 'Good' },
  { rank: 6, city: 'Kollam', state: 'Kerala', avgAqi: 48, category: 'Good' },
  { rank: 7, city: 'Amaravati', state: 'Andhra Pradesh', avgAqi: 50, category: 'Good' },
  { rank: 8, city: 'Madikeri', state: 'Karnataka', avgAqi: 52, category: 'Satisfactory' },
  { rank: 9, city: 'Ooty', state: 'Tamil Nadu', avgAqi: 54, category: 'Satisfactory' },
  { rank: 10, city: 'Kodaikanal', state: 'Tamil Nadu', avgAqi: 55, category: 'Satisfactory' },
];

export const allCities = [
  "Delhi", "Mumbai", "Bangalore", "Kolkata", "Chennai", "Hyderabad", "Pune", "Ahmedabad", "Jaipur", "Surat", 
  "Lucknow", "Kanpur", "Nagpur", "Indore", "Thane", "Bhopal", "Visakhapatnam", "Pimpri-Chinchwad", "Patna", 
  "Vadodara", "Ghaziabad", "Ludhiana", "Agra", "Nashik", "Faridabad", "Meerut", "Rajkot", "Kalyan-Dombivli"
];

// Per-city AQI profiles for the interactive Dashboard
export const cityProfiles: Record<string, { aqi: number; primaryPollutant: string; riskScore: number; healthAdvice: string; riskLevel: string; bestTime: string; meanAqi: number; maxAqi: number; minAqi: number; records: number }> = {
  "Delhi":       { aqi: 247, primaryPollutant: "PM2.5", riskScore: 78.4, healthAdvice: "Everyone should avoid all outdoor exertion. People with respiratory or heart disease should remain indoors.", riskLevel: "High — entire population affected.", bestTime: "Avoid outdoor exposure entirely.", meanAqi: 247, maxAqi: 499, minAqi: 89, records: 3420 },
  "Mumbai":      { aqi: 112, primaryPollutant: "PM10",  riskScore: 38.1, healthAdvice: "People with heart or lung disease, older adults, and children should reduce prolonged exertion.", riskLevel: "Moderate hazard for sensitive groups.", bestTime: "Early morning (5 AM - 7 AM).", meanAqi: 112, maxAqi: 298, minAqi: 42, records: 2190 },
  "Bangalore":   { aqi: 68,  primaryPollutant: "O3",    riskScore: 18.5, healthAdvice: "Air quality is acceptable. Unusually sensitive people should limit prolonged outdoor exertion.", riskLevel: "Low — acceptable for most.", bestTime: "Anytime — air quality is satisfactory.", meanAqi: 68,  maxAqi: 178, minAqi: 22, records: 1850 },
  "Kolkata":     { aqi: 158, primaryPollutant: "PM2.5", riskScore: 52.7, healthAdvice: "Members of sensitive groups may experience health effects. Limit prolonged outdoor exertion.", riskLevel: "Moderate — unhealthy for sensitive groups.", bestTime: "Late evening after 8 PM.", meanAqi: 158, maxAqi: 380, minAqi: 55, records: 2340 },
  "Chennai":     { aqi: 74,  primaryPollutant: "NO2",   riskScore: 21.3, healthAdvice: "Air quality is satisfactory and poses little or no risk.", riskLevel: "Low risk.", bestTime: "Anytime — air quality is satisfactory.", meanAqi: 74,  maxAqi: 195, minAqi: 28, records: 1680 },
  "Hyderabad":   { aqi: 95,  primaryPollutant: "PM10",  riskScore: 30.2, healthAdvice: "Air quality is acceptable. Sensitive individuals should consider limiting prolonged outdoor exertion.", riskLevel: "Low — acceptable for most.", bestTime: "Early morning or late evening.", meanAqi: 95,  maxAqi: 230, minAqi: 35, records: 1920 },
  "Pune":        { aqi: 82,  primaryPollutant: "PM10",  riskScore: 24.8, healthAdvice: "Air quality is satisfactory. Enjoy outdoor activities.", riskLevel: "Low risk.", bestTime: "Anytime during the day.", meanAqi: 82,  maxAqi: 210, minAqi: 30, records: 1540 },
  "Ahmedabad":   { aqi: 135, primaryPollutant: "PM2.5", riskScore: 44.6, healthAdvice: "Members of sensitive groups may experience health effects. Limit prolonged outdoor exertion.", riskLevel: "Moderate — unhealthy for sensitive groups.", bestTime: "Early morning (5-7 AM) or late evening.", meanAqi: 135, maxAqi: 320, minAqi: 48, records: 1760 },
  "Jaipur":      { aqi: 162, primaryPollutant: "PM10",  riskScore: 55.3, healthAdvice: "Members of sensitive groups should avoid prolonged outdoor exertion.", riskLevel: "Moderate — unhealthy for sensitive groups.", bestTime: "Late evening after 8 PM.", meanAqi: 162, maxAqi: 395, minAqi: 60, records: 1480 },
  "Surat":       { aqi: 88,  primaryPollutant: "PM10",  riskScore: 27.4, healthAdvice: "Air quality is satisfactory. Good for outdoor activities.", riskLevel: "Low risk.", bestTime: "Anytime during the day.", meanAqi: 88,  maxAqi: 198, minAqi: 32, records: 1320 },
  "Lucknow":     { aqi: 189, primaryPollutant: "PM2.5", riskScore: 63.1, healthAdvice: "Everyone should reduce prolonged or heavy exertion. Sensitive groups should avoid all outdoor exertion.", riskLevel: "High — unhealthy for all groups.", bestTime: "Very early morning only (5-6 AM).", meanAqi: 189, maxAqi: 420, minAqi: 72, records: 1890 },
  "Kanpur":      { aqi: 195, primaryPollutant: "PM2.5", riskScore: 65.8, healthAdvice: "Health warnings — everyone may begin to experience health effects.", riskLevel: "High — unhealthy for all.", bestTime: "Avoid outdoor activity if possible.", meanAqi: 195, maxAqi: 440, minAqi: 78, records: 1650 },
  "Nagpur":      { aqi: 105, primaryPollutant: "PM10",  riskScore: 34.2, healthAdvice: "Air quality is acceptable. Sensitive people should consider limiting outdoor exertion.", riskLevel: "Low to moderate.", bestTime: "Early morning (5-7 AM).", meanAqi: 105, maxAqi: 245, minAqi: 38, records: 1420 },
  "Indore":      { aqi: 92,  primaryPollutant: "PM10",  riskScore: 28.9, healthAdvice: "Air quality is satisfactory for most people.", riskLevel: "Low risk.", bestTime: "Anytime during the day.", meanAqi: 92,  maxAqi: 215, minAqi: 34, records: 1380 },
  "Patna":       { aqi: 212, primaryPollutant: "PM2.5", riskScore: 71.4, healthAdvice: "Health warnings of emergency conditions. Everyone is more likely to be affected.", riskLevel: "Very High — emergency conditions.", bestTime: "Avoid all outdoor exposure.", meanAqi: 212, maxAqi: 465, minAqi: 85, records: 1560 },
};

// Cluster visualization mocked data
export const clusterData = Array.from({length: 291}).map((_, i) => {
  const isPolluted = Math.random() > 0.47;
  return {
    city: `City ${i}`,
    cluster: isPolluted ? 'Cluster 1 (Polluted)' : 'Cluster 0 (Clean)',
    meanAqi: isPolluted ? 137 + Math.random()*80 - 40 : 76 + Math.random()*50 - 25,
    stdDev: isPolluted ? 60 + Math.random()*30 : 30 + Math.random()*20
  };
});
