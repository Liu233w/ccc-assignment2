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
    name: 'Default',
    component: () => import('../layout/Index.vue'),
    children: [
      {
        path: '',
        name: 'MapView',
        component: () => import('../views/MapView.vue')
      },
      {
        path: '/chart',
        name: 'ChartView',
        component: () => import('../views/ChartView.vue')
      }
    ]
  },
  {path: '*', redirect: '/' }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
