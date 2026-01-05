<script setup>
import { RouterLink } from 'vue-router';
import { ref, onMounted } from 'vue';
import axios from 'axios';

// Defining the refs to hold the data from the backend
const powerLast5Min = ref('');
const powerLastHour = ref('');
const powerToday = ref('');
const powerThisWeek = ref('');
const totalCost = ref('');

// Fetch values on component mount
onMounted(() => {
   axios.get('http://127.0.0.1:5002/power-last-5-min')
       .then(response => { powerLast5Min.value = response.data.power_last_5_min + ' kWh'; })
       .catch(error => { console.error('Error fetching power consumed in last 5 minutes:', error); });

   axios.get('http://127.0.0.1:5002/power-last-hour')
       .then(response => { powerLastHour.value = response.data.power_last_hour + ' kWh'; })
       .catch(error => { console.error('Error fetching power consumed in last hour:', error); });

   axios.get('http://127.0.0.1:5002/power-today')
       .then(response => { powerToday.value = response.data.power_today + ' kWh'; })
       .catch(error => { console.error('Error fetching power consumed today:', error); });

   axios.get('http://127.0.0.1:5002/power-this-week')
       .then(response => { powerThisWeek.value = response.data.power_this_week + ' kWh'; })
       .catch(error => { console.error('Error fetching power consumed this week:', error); });

   axios.get('http://127.0.0.1:5002/total-cost-this-week')
       .then(response => { totalCost.value = '฿ ' + response.data.total_cost; })
       .catch(error => { console.error('Error fetching total cost of electricity for this week:', error); });
});
</script>


<template>
   <h1>Dashboard</h1>
   <div class="container">
   <div class="item">
     <p>Power Consumed in last 5 min.</p>
     <input type="text" v-model="powerLast5Min" readonly>
   </div>
   <div class="item">
     <p>Power Consumed in last Hour</p>
     <input type="text" v-model="powerLastHour" readonly>
   </div>
   <div class="item">
     <p>Power Consumed Today</p>
     <input type="text" v-model="powerToday" readonly>
   </div>
   <div class="item">
     <p>Power Consumed This Week</p>
     <input type="text" v-model="powerThisWeek" readonly>
   </div>
   <div class="item">
     <p>Total Cost of Electricity for This Week</p>
     <input type="text" v-model="totalCost" readonly>
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
       background-color: darkred;
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
  

   button:active {
       background-color: red;
       transform: translateY(4px);
   }
</style>
