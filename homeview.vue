<script setup>
import Header from '@/components/Header.vue';
import WeeklyReport from '@/components/Weekly-Report.vue'
import Dashboard from '@/components/Dashboard.vue'
import Devmode from '@/components/Dev-Mode.vue'
</script>

<template>
   <Header />
 <div class="containter">
   <WeeklyReport></WeeklyReport>
 </div>
  <div class="containter margin">
   <Dashboard></Dashboard>
 </div>

 <div class="containter">
   <Devmode></Devmode>
 </div>
</template>

<style scoped>
</style>
