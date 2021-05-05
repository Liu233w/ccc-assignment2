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
    path: '/',
    name: 'Default',
    component: () => import('../layout/Index.vue'),
    children: [
      {
        path: 'chart',
        Name: 'ChartView',
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
