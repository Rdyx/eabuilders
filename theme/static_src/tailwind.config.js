// This is a minimal config.
// If you need the full config, get it from here:
// https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
module.exports = {
  purge: [
    // Templates within theme app (e.g. base.html)
    '../templates/**/*.html',
    // Templates in other apps. Uncomment the following line if it matches
    // your project structure or change it to match.
    '../../**/templates/**/*.html',
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
        'orange-50': '#ffccb3',
        'orange-100': '#ffb996',
        'orange-200': '#ff9865',
        'orange-300': '#ff7f3f',
        'orange-400': '#ff5500',
        'orange-500': '#d74800',
        'orange-600': '#9a3300',
        'orange-700': '#6b2400',
        'orange-800': '#481800',
        'orange-900': '#240c00',
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
