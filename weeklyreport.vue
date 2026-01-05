<script setup>
import { RouterLink } from 'vue-router';
import { ref, onMounted } from 'vue';
import axios from 'axios';

const weekStart = ref('');
const weekEnd = ref('');
const totalPowerConsumed = ref('');
const totalCost = ref('');
const averagePowerPerDay = ref('');
const averageCostPerDay = ref('');

onMounted(() => {
   axios.get('http://127.0.0.1:5002/weekly-report')
       .then(response => {
           weekStart.value = response.data.week_start;
           weekEnd.value = response.data.week_end;
           totalPowerConsumed.value = response.data.total_power_consumed + ' kWh';
           totalCost.value = '฿ ' + response.data.total_cost;
           averagePowerPerDay.value = response.data.average_power_per_day + ' kWh';
           averageCostPerDay.value = '฿ ' + response.data.average_cost_per_day;
       })
       .catch(error => {
           console.error('Error fetching weekly report:', error);
       });
});
</script>

<template>
   <h1>Weekly Report</h1>
   <div class="container">
       <div class="item">
           <p>Week Start</p>
           <input type="text" v-model="weekStart" readonly>
       </div>
       <div class="item">
           <p>Week End</p>
           <input type="text" v-model="weekEnd" readonly>
       </div>
       <div class="item">
           <p>Total Power Consumed</p>
           <input type="text" v-model="totalPowerConsumed" readonly>
       </div>
       <div class="item">
           <p>Average Power Consumed Per Day</p>
           <input type="text" v-model="averagePowerPerDay" readonly>
       </div>
       <div class="item">
           <p>Total Cost</p>
           <input type="text" v-model="totalCost" readonly>
       </div>
       <div class="item">
           <p>Average Cost Per Day</p>
           <input type="text" v-model="averageCostPerDay" readonly>
       </div>
   </div>
  
  
   <router-link to="/">
     <button>Go to Home</button>
   </router-link>
</template>


<style scoped>
   body {
       display: flex;
       justify-content: center;
       align-items: center;
       height: 100px;
       margin: 0;
   }

   .container {
       display: grid;
       grid-template-columns: 1fr 1fr;
       gap: 20px;
       max-width: 600px;
       background-color: darkcyan;
       padding: 20px;
       border: 1px solid #ccc;
       border-radius: 8px;
       margin-right: auto;
       margin-left: auto;
   }

   .item {
       display: flex;
       flex-direction: column;
       align-items: center;
   }

   .item p {
       margin: 0 0 10px;
       font-size: 14px;
       text-align: center;
   }

   .item input {
       text-align: center;
       padding: 10px;
       width: 150px;
       border: 1px solid #ccc;
       border-radius: 4px;
   }
  
  
  
   button {
       background-color: grey;
       padding: 10px 30px;
       text-align: center;
       color: black;
       font-family: Arial, Helvetica, sans-serif;
       border-radius: 5px;
       position: fixed;
       bottom: 10px;
       left: 10px;
   }

   button:active {
       background-color: red;
       transform: translateY(4px);
   }

   b {
       text-align: center;
       position: relative;
   }

   .margin {
     margin-top: 20px;
   }
</style>
