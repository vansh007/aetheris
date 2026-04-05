export const getAqiColor = (aqi: number) => {
  if (aqi <= 50) return '#00B050'; // Good
  if (aqi <= 100) return '#92D050'; // Satisfactory
  if (aqi <= 200) return '#FFFF00'; // Moderate
  if (aqi <= 300) return '#FF9900'; // Poor
  if (aqi <= 400) return '#FF0000'; // Very Poor
  return '#990000'; // Severe
};

export const getAqiCategory = (aqi: number) => {
  if (aqi <= 50) return 'Good';
  if (aqi <= 100) return 'Satisfactory';
  if (aqi <= 200) return 'Moderate';
  if (aqi <= 300) return 'Poor';
  if (aqi <= 400) return 'Very Poor';
  return 'Severe';
};

export const getAqiBadgeStyles = (category: string) => {
  switch(category) {
    case 'Good': return 'bg-[#00B050] text-white';
    case 'Satisfactory': return 'bg-[#92D050] text-slate-900';
    case 'Moderate': return 'bg-[#FFFF00] text-slate-900';
    case 'Poor': return 'bg-[#FF9900] text-white';
    case 'Very Poor': return 'bg-[#FF0000] text-white';
    case 'Severe': return 'bg-[#990000] text-white';
    default: return 'bg-slate-700 text-white';
  }
};
