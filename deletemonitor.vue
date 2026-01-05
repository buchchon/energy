<script setup>
import { ref, onMounted } from 'vue';
import { RouterLink } from 'vue-router';
import axios from 'axios';

const clamps = ref([]); // List of clamps for dropdown
const selectedClamp = ref('');

onMounted(() => {
   // Fetch the list of clamps
   axios.get('http://127.0.0.1:5002/get-clamps')
       .then(response => {
           clamps.value = response.data.clamps;
       })
       .catch(error => {
           console.error('Error fetching clamps:', error);
           alert("An error occurred while fetching clamps: " + error.message);
       });
});

function deletemonitor() { // Ensure a clamp is selected
   if (selectedClamp.value.trim() === "") {
       alert("Select a Clamp.");
       return;
   }

   // Send POST request to add the new clamp
   axios.post('http://127.0.0.1:5002/delete-clamp', {
       clamp_id: selectedClamp.value
   })
   .then(response => {
       alert(response.data.message);
   })
   .catch(error => {
       console.error('Error deleting clamp:', error);
       alert("An error occurred: " + error.message);
   });
}


</script>

<template>
   <h1>
       Delete Monitor
   </h1>

   <label for="clampSelect" class="margin">Select Clamp:</label>
   <select id="clampSelect" v-model="selectedClamp" class="margin">
       <option value="" disabled>Please select a clamp</option>
       <option v-for="clamp in clamps" :key="clamp.clamp_ID" :value="clamp.clamp_ID">
           {{ clamp.clamp_ID }}
       </option>
   </select>

  
  
   <button class="margin" @click="deletemonitor">Confirm</button>





   <router-link to="/">
     <button class="gohome">Go to Home</button>
   </router-link>

   <router-link to="/devdashboard">
     <button class="goback">Go to Dashboard</button>
   </router-link>
</template>

<style>
   .center {
       text-align: center;
   }
  
   .norm {
       background-color: lightgrey;
       position: relative;
       display: block;
       margin-right: auto;
       margin-left: auto;
   }
  

   .gohome {
       position: fixed;
       bottom: 10px;
       left: 10px;
   }

   .goback {
       position: fixed;
       bottom: 10px;
       right: 10px;
   }
  
   button {
       background-color: grey;
       padding: 10px 30px;
       text-align: center;
       color: black;
       font-family: Arial, Helvetica, sans-serif;
       border-radius: 5px;
   }

   button:active {
       background-color: red;
       transform: translateY(4px);
   }
</style>
