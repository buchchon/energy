<script setup>
import { ref, onMounted } from 'vue';
import { RouterLink } from 'vue-router';
import axios from 'axios';

const floors = ref([]); // List of floors for dropdown
const selectedFloor = ref('');

onMounted(() => {
   // Fetch the list of floors
   axios.get('http://127.0.0.1:5002/get-floors')
       .then(response => {
           floors.value = response.data.floors;
       })
       .catch(error => {
           console.error('Error fetching floors:', error);
           alert("An error occurred while fetching floors: " + error.message);
       });
});



function addClamp() {
   // Ensure a floor is selected
   if (selectedFloor.value.trim() === "") {
       alert("Select a Floor.");
       return;
   }

   // Get the clamp ID input value directly from the DOM
   const clampInputElement = document.getElementById('clampInput');
   const clampID = clampInputElement ? clampInputElement.value.trim() : '';

   if (clampID === "") {
       alert("Clamp ID can't be empty.");
       return;
   }

   // Send POST request to add the new clamp
   axios.post('http://127.0.0.1:5002/add-clamp', {
       floor_id: selectedFloor.value,
       clamp_id: clampID
   })
   .then(response => {
       alert(response.data.message);
   })
   .catch(error => {
       console.error('Error adding clamp:', error);
       alert("An error occurred: " + error.message);
   });
}


</script>

<template>
   <h1>
       Add Monitor
   </h1>

   <label for="floorSelect" class="margin">Select Floor:</label>
   <select id="floorSelect" v-model="selectedFloor" class="margin">
       <option value="" disabled>Please select a floor</option>
       <option v-for="floor in floors" :key="floor.floor_ID" :value="floor.floor_ID">
           {{ floor.floor_ID }}
       </option>
   </select>

   <body class = 'center'> Input UID </body>

   <input type="text" id="clampInput" name="clamp_id">

   <button class="margin" @click="addClamp">Confirm</button>


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
