import Vue from 'vue'
import App from './App.vue'
import router from './router'

Vue.config.productionTip = false

// element-ui
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';

Vue.use(ElementUI);

// import store from './store'

//axios
import axios from 'axios'


// axios.defaults.baseURL = 'http://47.107.243.80:8080/user/'
axios.defaults.baseURL = 'http://172.16.100.88:888/user/'

// import './mock'

Vue.prototype.$http = axios


new Vue({
  router,
  // store,
  render: h => h(App)
}).$mount('#app')
