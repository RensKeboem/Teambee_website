/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./public/**/*.{html,js}",
    "./**/*.py"
  ],
  theme: {
    extend: {
      colors: {
        primary: '#3D2E7C',
        secondary: '#E8973A',
        accent: '#94C46F',
      },
      borderRadius: {
        lg: "8px",
        xl: "12px",
        "2xl": "16px"
      }
    }
  },
  plugins: []
} 