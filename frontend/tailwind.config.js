/** @type {import('tailwindcss').Config} */
console.log(process.env.ANY_COLOR)
module.exports = {
  content: [
    "../**/src/**/*.{js,css,scss,html}",
    "../**/templates/**/*.{js,css,scss,html}",
    "../../.venv/**/crispy_tailwind/**/*.html"
  ],
  theme: {
    extend: {
      placepython: "#e08631",
    },
  },
  plugins: [
    require('daisyui'),
  ],
}

