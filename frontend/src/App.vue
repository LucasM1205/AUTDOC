<template>
    <div id="app" class="main-container">
      <header class="header">
        <img src="/THM_Logo_4c.png" alt="THM Logo" class="thm-logo" />
      </header>
      <router-view />
    </div>
  </template>
  
  <script>
  export default {};
  </script>
  
  <style>
  /* Globale CSS-Variablen für Primary, Secondary und Highlight Color */
  :root {
    --primary-color: #80ba24; /* Angepasste Primary Color */
    --secondary-color: #4a5c66; /* Angepasste Secondary Color */
    --highlight-color: #c1272d; /* Drittfarbe für Hervorhebungen */
  }
  
  /* Hauptcontainer mit Abstand zum oberen Rand */
  .main-container {
    margin-top: 20px;
    font-family: Arial, sans-serif;
  }
  
  /* Header Styling für das Logo */
  .header {
    display: flex;
    justify-content: flex-start; /* Logo linksbündig ausrichten */
    align-items: center;
    padding: 20px;
    background-color: white;
    border-bottom: 1px solid #ccc;
  }
  
  /* Styling für das THM-Logo */
  .thm-logo {
    height: 60px; /* Höhe des Logos */
    margin-left: 20px; /* Abstand links als Schutzzone */
  }
  
  /* Styling für Buttons */
  button {
    background-color: var(--primary-color);
    color: white;
    border: none;
    padding: 10px 20px;
    cursor: pointer;
  }
  
  /* Hover-Effekt für Buttons */
  button:hover {
    background-color: #6da22d;
  }
  
  /* Styling für wichtige Buttons mit der Highlight-Farbe */
  button.highlight {
    background-color: var(--highlight-color);
  }
  
  button.highlight:hover {
    background-color: #a02125;
  }
  </style>
  