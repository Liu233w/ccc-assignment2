import Vue from 'vue'
import VueRouter from 'vue-router'


Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue'),
  },
  {
    path: '/demo',
    name: 'Demo',
    component: () => import('../layout/Index.vue'),
    children: [
      {
        path: '',
        name: 'MapView',
        component: () => import('../views/MapView.vue')
      }
    ]
  },
  {path: '*', redirect: '/' }
]

const router = new VueRouter({
  mode: 'hash',
  base: process.env.BASE_URL,
  routes
})

export default router
