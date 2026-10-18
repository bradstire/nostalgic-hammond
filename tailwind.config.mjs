/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        charcoal: '#2C2825',
        cream: '#F5F0E6',
        rust: '#B85C3E',
        'aged-gold': '#C4A35A',
        'warm-white': '#E8E0D4',
        'warm-black': '#3B3632',
        'warm-gray': '#8C8578',
        'light-gray': '#C8BFB3',
      },
      fontFamily: {
        display: ['Playfair Display', 'serif'],
        body: ['Source Serif 4', 'serif'],
        utility: ['Barlow Condensed', 'sans-serif'],
      },
      maxWidth: {
        'content': '1200px',
      },
    },
  },
  plugins: [],
}
