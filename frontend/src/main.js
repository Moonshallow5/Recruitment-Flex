/**
 * main.js
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Plugins
import { registerPlugins } from '@/plugins'

// Components
import App from './App.vue'

// Composables
import { createApp } from 'vue'

// Vuex Store
import store from '@/states/store'

// Toast Notification Styles
import 'vue-toast-notification/dist/theme-sugar.css'

// Styles
import 'unfonts.css'

const app = createApp(App)

// Register Vuex store
app.use(store)

registerPlugins(app)

app.mount('#app')
