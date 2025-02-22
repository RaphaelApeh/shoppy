/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './**/**.py',
    './items/templates/items/items_list.html',
    './templates/allauth/layouts/base.html'
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

