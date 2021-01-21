// This is a minimal config.
// If you need the full config, get it from here:
// https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
module.exports = {
  purge: [
    // Templates within theme app (e.g. base.html)
    '../templates/**/*.html',
    // Templates in other apps. Uncomment the following line if it matches
    // your project structure or change it to match.
    '../../templates/**/*.html',
  ],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      colors: {
        'brown-50': '#f2be8a',
        'brown-100': '#e5b483',
        'brown-200': '#cca074',
        'brown-300': '#b38c66',
        'brown-400': '#997857',
        'brown-500': '#806449',
        'brown-600': '#66503a',
        'brown-700': '#4d3c2c',
        'brown-800': '#33281d',
        'brown-900': '#1a140f',
      },
    },
  },
  variants: {
    extend: {
      borderWidth: ['hover'],
    },
  },
  plugins: [],
};
