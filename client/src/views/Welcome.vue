<script >
  

export default {
    name: "Welcome",
    components: {  }
};
</script>



<template >
  <br>
  <br>
  
  <img src="../../src/assets/quan.png" class="rounded mx-auto d-block"  alt="quansApp"/>
  <br>
  <div class="card text-center ">
  
  <div class="card-body">
    <h1 class="card-title">Quantified Self App v2</h1>
    <h4 class="card-text">Track your every activity here</h4>
    <br>
    <router-link :to="{ name: 'Login'}">
  <a class="btn btn-primary">Getting Started</a>
</router-link>
    
  </div>

 
</div>

    

  
   

</template>

<style scoped>
  .card {
   
    background-color: rgba(0, 0, 0, 0);
    color: white;
    border: 0;
    
}



</style>
