import { createVuetify } from 'vuetify'
import '@mdi/font/css/materialdesignicons.css'

import 'vuetify/styles'

export default createVuetify({
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        colors: {
          // Cores principais
          'primary': '#475569', // slate-600 - usado em botões principais
          'secondary': '#64748b', // slate-500
          'surface': '#ffffff',
          'background': '#f8fafc', // slate-50 - background da página

          // Paleta slate (substituir text-slate-xxx)
          'slate900': '#0f172a',
          'slate600': '#475569',
          'slate500': '#64748b',
          'slate400': '#94a3b8',
          'slate300': '#cbd5e1',
          'slate200': '#e2e8f0',
          'slate100': '#f1f5f9',
          'slate50': '#f8fafc',

          // Status colors (para chips)
          'success': '#059669', // green-600
          'success-bg': '#d1fae5', // green-100
          'success-border': '#a7f3d0', // green-200

          'warning': '#d97706', // amber-600
          'warning-bg': '#fef3c7', // amber-100
          'warning-border': '#fde68a', // amber-200

          'error': '#dc2626', // red-600
          'error-bg': '#fee2e2', // red-100
          'error-border': '#fecaca', // red-200
        },
      },
    },
  },

  // Defaults globais para componentes
  defaults: {
    VBtn: {
      style: [{ textTransform: 'none', letterSpacing: 'normal' }],
    },
    VChip: {
      style: [{ textTransform: 'none', letterSpacing: 'normal' }],
    },
    VCard: {
      elevation: 3,
    },
  },
})
