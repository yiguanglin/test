import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../views/login.vue'
import Home from '../views/home.vue'
import Users from '../components/users/users.vue'
import Match from '../components/match/match.vue'
import Subject from '../components/subject/subject.vue'
import topicgroup from '../components/subject/topicgroup.vue'
Vue.use(VueRouter)

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: Login },
  {
    path: '/home',
    component: Home,
    redirect: '/users',
    children: [
      { path: '/users', component: Users },
      { path: '/match', component: Match },
      { path: '/subject', component: Subject },
      { path: '/topicgroup', component: topicgroup }
    ]
  }
]

const router = new VueRouter({
  routes
})
// 路由导肮守卫
router.beforeEach((to, from, next) => {
  // 如果访问login页面 直接放行
  if (to.path === '/login') return next()
  // 拿判断是否有token 有token就可以访问home页面 如果有就保存
  const tokenStr = window.sessionStorage.getItem('token')
  if (!tokenStr) return next('/login')
  next()
})
export default router
