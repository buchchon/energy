import { createRouter, createWebHistory } from 'vue-router';
import Homeview from '@/views/Homeview.vue'
import Dashboardview from '@/views/Dashboardview.vue'
import WeeklyReportview from '@/views/WeeklyReportview.vue';
import DevAuthenticate from '@/views/DevAuthenticate.vue';
import Devdashboardview from '@/views/Devdashboardview.vue';
import Addbuilding from '@/views/Add/Addbuilding.vue';
import Addfloor from '@/views/Add/Addfloor.vue';
import Addmonitor from '@/views/Add/Addmonitor.vue';

import Deletemonitor from '@/views/Delete/Deletemonitor.vue'

const router = createRouter({
   history: createWebHistory(import.meta.env.BASE_URL),
   routes: [
       {
           path: '/',
           name: 'home',
           component: Homeview,
       },
       {
           path: '/db',
           name: 'dashboard',
           component: Dashboardview,
       },
       {
           path: '/wr',
           name: 'weeklyreport',
           component: WeeklyReportview,
       },
       {
           path: '/dmauthenticate',
           name: 'devmodeauthenticate',
           component: DevAuthenticate,
       },
       {
           path: '/devdashboard',
           name: 'devdashboard',
           component: Devdashboardview,
       },
       {
           path: '/addmonitor',
           name: 'addmonitor',
           component: Addmonitor,
       },

       {
           path: '/deletemonitor',
           name: 'deletemonitor',
           component: Deletemonitor,
       },

       {
           path: '/addfloor',
           name: 'addfloor',
           component: Addfloor,
       },

       {
           path: '/addbuilding',
           name: 'addbuilding',
           component: Addbuilding,
       },
   ],
});

export default router;
