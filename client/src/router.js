import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/acer',
      name: 'acer',
      component: () => import('./views/Acer.vue')
    },
    {
      path: '/frontdesk',
      name: 'frontdesk',
      component: () => import('./views/Frontdesk.vue')
    },
    {
      path: '/manager',
      name: 'manager',
      component: () => import('./views/Manager.vue')
    },
    {
      path: '/user',
      name: 'user',
      component: () => import('./views/User.vue')
    },
  ]
})
