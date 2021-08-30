import {createApp} from 'vue'
import router from './router'
import store from './store'
import axios from "axios";

import App from './App.vue'
import AppButton from "./components/ui/AppButton";
import AppCard from "./components/ui/AppCard"
import AppDialog from "./components/ui/AppDialog"
import AppLoader from "./components/ui/AppLoader"
import {requestInterceptor} from "./utils/interceptors";

const app = createApp(App);

app.use(store)
app.use(router)

app.component('AppButton', AppButton);
app.component('AppCard', AppCard);
app.component('AppDialog', AppDialog);
app.component('AppLoader', AppLoader);

axios.defaults.baseURL = process.env.VUE_APP_BACKEND_URL;
app.config.globalProperties.$axios = axios;
store.$axios = axios;

requestInterceptor();

app.mount('#app');