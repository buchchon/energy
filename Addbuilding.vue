<script>

</script>

<template>
   <router-link to="/wr">
     <button>WEEKLY REPORT</button>
   </router-link>
</template>

<style scoped>
   button {
       width: 200px;
       background-color: lightblue;
       padding: 10px 30px;
       text-align: center;
       color: black;
       font-family: Arial, Helvetica, sans-serif;
       border-radius: 5px;
       border-color: white;
       position: relative;
       display: block;
       margin: auto;
   }

   button:active {
       background-color: red;
       transform: translateY(4px);
   }
</style>
