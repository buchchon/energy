<script setup>
import { RouterLink } from 'vue-router';
import axios from 'axios';

function downloadDatabase() {
   axios({
       url: 'http://127.0.0.1:5002/download-database',
       method: 'GET',
       responseType: 'blob'
   })
   .then(response => {
       const url = window.URL.createObjectURL(new Blob([response.data])); //creation of url for download
       const link = document.createElement('a');
       link.href = url;
       link.setAttribute('download', 'database_export.csv');
       document.body.appendChild(link);
       link.click();
       link.remove();
   })
   .catch(error => {
       console.error('Error downloading database:', error);
       alert("An error occurred while downloading the database: " + error.message);
   });
}
</script>

<template>
   <h1>
       Developer Dashboard
   </h1>
   <h2>Add</h2>
  
   <router-link to="/addbuilding">
       <button class = 'norm'> Add Building </button>
   </router-link>
  
   <router-link to="/addfloor">
       <button class = 'norm'> Add Floor </button>
   </router-link>
  
   <router-link to="/addmonitor">
       <button class = 'norm'> Add Monitor </button>
   </router-link>

   <h2>Delete</h2>

   <router-link to="/deletemonitor">
       <button class = 'norm'> Delete Monitor </button>
   </router-link>

   <h2>Download Database</h2>
   <<button @click="downloadDatabase" class="download-button norm">Download Database</button>
   <router-link to="/">
     <button class="gohome">Go to Home</button>
   </router-link>
</template>

<style>
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
  
   button:active {
       background-color: red;
       transform: translateY(4px);
   }
</style>
