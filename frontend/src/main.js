import { createApp } from 'vue';
import App from './App.vue';
import router from './router'; // Router importieren

const app = createApp(App);
app.use(router); // Router einbinden
app.mount('#app');
