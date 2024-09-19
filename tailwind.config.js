/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{html,ts}",
  ],
  theme: {
    extend: {
      colors: {
        height: {
          '0.3':'0.0875rem',
          '0.2':'0.075rem',
          '0.1':'0.0625rem',
          '104': '26rem',
          '112': '28rem',
          '120': '30rem',
          '128':'32rem',
          '144': '36rem',
          '160': '40rem',
          '176': '44rem',
          '192': '48rem',
          '208': '52rem',
          '224': '56rem',
          '240': '60rem',
        },
        width: {
          '104': '26rem',
          '112': '28rem',
          '120': '30rem',
          '128': '32rem',
          '144': '36rem',
          '160': '40rem',
          '176': '44rem',
          '192': '48rem',
          '208': '52rem',
          '224': '56rem',
          '240': '60rem',
        },
      }
    },
  },
  plugins: [],
}