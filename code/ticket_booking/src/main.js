import App from './App.vue'
import router from './router'
import { createApp } from 'vue';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';
import "popper.js";




const app = createApp(App);
app.use(router); // Use the router instance
app.mount('#app');
