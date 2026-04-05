/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        aqi: {
          good: '#00B050',
          satisfactory: '#92D050',
          moderate: '#FFFF00',
          poor: '#FF9900',
          veryPoor: '#FF0000',
          severe: '#990000'
        },
        slate: {
          950: '#020617', // Darker slate for background
          900: '#0f172a',
          800: '#1e293b',
          700: '#334155',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
