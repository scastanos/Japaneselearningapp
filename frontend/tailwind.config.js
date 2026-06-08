/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        sakura:  { DEFAULT: '#D4537E', light: '#FBEAF0', mid: '#ED93B1', dark: '#72243E' },
        matcha:  { DEFAULT: '#1D9E75', light: '#E1F5EE', mid: '#5DCAA5', dark: '#085041' },
        yuzu:    { DEFAULT: '#BA7517', light: '#FAEEDA', mid: '#FAC775', dark: '#633806' },
        indigo:  { DEFAULT: '#534AB7', light: '#EEEDFE', mid: '#AFA9EC', dark: '#26215C' },
        ocean:   { DEFAULT: '#185FA5', light: '#E6F1FB', mid: '#85B7EB', dark: '#042C53' },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        jp:   ['"Noto Sans JP"', 'sans-serif'],
      },
    }
  },
  plugins: [],
}
