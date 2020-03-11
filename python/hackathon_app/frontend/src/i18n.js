import i18n from 'i18next'
import LanguageDetector from 'i18next-browser-languagedetector'

import translationIt from './locales/it/translation.json'

i18n.use(LanguageDetector).init({
  resources: {
    it: {
      translations: translationIt,
    },
  },

  ns: ['translations'],
  defaultNS: 'translations',
  keySeparator: false,

  interpolation: {
    escapeValue: false,
    formatSeparator: ',',
  },

  react: {
    wait: true,
  },

  fallbackLng: ['en-US'],
})

export default i18n
