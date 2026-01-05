<script setup>
import { ref, onMounted } from 'vue';
import { RouterLink } from 'vue-router';
import axios from 'axios';

const buildings = ref([]);
const selectedBuilding = ref('');

onMounted(() => {
   // Fetch the current list of buildings
   axios.get('http://127.0.0.1:5002/get-buildings')
       .then(response => {
           // Filter unique buildings based on building_ID
           const uniqueBuildings = Array.from(
               new Set(response.data.buildings.map(building => building[0]))
           ).map(building_ID => ({
               building_ID,
           }));

           buildings.value = uniqueBuildings;
       })
       .catch(error => {
           console.error('Error fetching buildings:', error);
           alert("An error occurred while fetching buildings: " + error.message);
       });
});

function addFloor() {
   // Ensure a building is selected
   if (selectedBuilding.value.trim() === "") {
       alert("Select a building.");
       return;
   }

   // Get the floor ID input value directly from the DOM
   const floorInputElement = document.getElementById('floorInput');
   const floorID = floorInputElement ? floorInputElement.value.trim() : '';

   if (floorID === "") {
       alert("Floor ID can't be empty.");
       return;
   }

   // Send POST request to add the new floor
   axios.post('http://127.0.0.1:5002/add-floor', {
       building_id: selectedBuilding.value,
       floor_id: floorID
   })
   .then(response => {
       alert(response.data.message);
   })
   .catch(error => {
       console.error('Error adding floor:', error);
       alert("An error occurred: " + error.message);
   });
}
</script>

<template>
   <h1>Add Floor</h1>
  
   <label for="buildingSelect" class="margin">Select Building:</label>
   <select id="buildingSelect" v-model="selectedBuilding" class="margin">
       <option value="" disabled>Please select a building</option>
       <option v-for="building in buildings" :key="building.building_ID" :value="building.building_ID">
           {{ building.building_ID }}
       </option>
   </select>
  
   <label class="margin"> Floor: </label>
   <input type="text" id="floorInput" name="floor_id">

   <button class="margin" @click="addFloor">Confirm</button>

   <router-link to="/">
       <button class="gohome">Go to Home</button>
   </router-link>

   <router-link to="/devdashboard">
       <button class="goback">Go to Dashboard</button>
   </router-link>
</template>

<style>
   .margin {
       margin: 10px;
   }

   button {
       background-color: grey;
       padding: 10px 20px;
       border: none;
       color: white;
       cursor: pointer;
       border-radius: 5px;
   }

   button:hover {
       background-color: darkgrey;
   }

   select, input {
       display: block;
       margin: 10px auto;
       padding: 5px;
       color: black;
       background-color: white;
       border: 1px solid #ccc;
       appearance: none;
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
</style>
