<template>
    <div id="app" class="main-container">
      <router-view />
    </div>
  </template>
  
  <script>
  export default {};
  </script>
  
  <style>
  /* Definiere eine globale CSS-Variable für die Primary Color */
  :root {
    --primary-color: #80ba27;
  }
  
  .main-container {
    margin-top: 20px;
  }
  
  /* Beispiel für das Styling eines Buttons */
  button {
    background-color: var(--primary-color);
    color: white;
    border: none;
    padding: 10px 20px;
    cursor: pointer;
  }
  </style>
  