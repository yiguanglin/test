import Vue from 'vue'
import App from './App.vue'
import router from './router'
// 公共样式css
import './assets/css/global.css'
import './plugins/element'
// 引入element样式
import 'element-ui/lib/theme-chalk/index.css'
// 引入图标
import './assets/icon/iconfont.css'
// 引入打印的包
import Print from 'vue-printjs'
// 配置markdown
import mavonEditor from 'mavon-editor'
import 'mavon-editor/dist/css/index.css'
// showdown markdown转html
import showdown from 'showdown'
//  配置网络请求
import axios from 'axios'
// 请求根路径
axios.defaults.baseURL = 'http://172.16.100.88:888/admin'
Vue.prototype.$http = axios
Vue.config.productionTip = false
Vue.prototype.converter = new showdown.Converter()
Vue.use(Print)
Vue.use(mavonEditor)

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
