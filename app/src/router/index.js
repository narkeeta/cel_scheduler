import { createRouter, createWebHistory } from 'vue-router'
import Scheduler from '../views/Scheduler.vue'

const routes = [
  {
    path: '/',
    name: 'scheduler',
    component: Scheduler
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
