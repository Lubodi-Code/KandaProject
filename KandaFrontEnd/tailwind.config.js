/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      // Agregar utilidades personalizadas para scrollbar
      utilities: {
        '.scrollbar-thin': {
          'scrollbar-width': 'thin',
          'scrollbar-color': '#10b981 #1f2937',
        },
        '.scrollbar-thin::-webkit-scrollbar': {
          'width': '8px',
        },
        '.scrollbar-thin::-webkit-scrollbar-track': {
          'background': '#1f2937',
          'border-radius': '4px',
        },
        '.scrollbar-thin::-webkit-scrollbar-thumb': {
          'background': '#10b981',
          'border-radius': '4px',
        },
        '.scrollbar-thin::-webkit-scrollbar-thumb:hover': {
          'background': '#059669',
        },
      }
    },
  },
  plugins: [
    import('@tailwindcss/forms'),
    // Plugin personalizado para scrollbar
    function({ addUtilities }) {
      const newUtilities = {
        '.scrollbar-thin': {
          'scrollbar-width': 'thin',
          'scrollbar-color': '#10b981 #1f2937',
        },
        '.scrollbar-thin::-webkit-scrollbar': {
          'width': '8px',
        },
        '.scrollbar-thin::-webkit-scrollbar-track': {
          'background': '#1f2937',
          'border-radius': '4px',
        },
        '.scrollbar-thin::-webkit-scrollbar-thumb': {
          'background': '#10b981',
          'border-radius': '4px',
        },
        '.scrollbar-thin::-webkit-scrollbar-thumb:hover': {
          'background': '#059669',
        },
        '.scrollbar-thumb-green-500': {
          'scrollbar-color': '#10b981 #1f2937',
        },
        '.scrollbar-track-gray-800': {
          'scrollbar-color': '#10b981 #1f2937',
        },
      }
      addUtilities(newUtilities)
    }
  ],
}

