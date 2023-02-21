import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

// const homes=()=>import('../views/dierge.vue')

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path:'/loggedin',
    name:'LoggedIn',
    component:()=>import('../views/LoggedIn'),
  },
  {
    path:'/ranking',
    name:'LoggedIns',
    component:()=>import('../views/LoggedIn/Ranking.vue')
  },
]

const router = new VueRouter({
  routes
})



router.beforeEach((to, from, next) => {
  // console.log(to.name)
  if(sessionStorage.getItem('token')){
    // console.log("有token")
    if(to.name == 'Home') next('/loggedIn')
  }else{
    // console.log("无token")
    if(to.name == 'LoggedIn' || to.name == 'LoggedIns'){
      next('/')
      alert("你还没登录呢!")
    } 
  }
  next()
})

export default router
