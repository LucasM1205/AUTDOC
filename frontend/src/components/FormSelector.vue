<template>
    <div class="form-selector-container">
      <h1>Formulare</h1>
      <p>Wählen Sie das Formular aus, welches Sie erstellen möchten</p>
  
      <select v-model="selectedForm" class="dropdown">
        <option disabled value="">Bitte wählen</option>
        <option value="joker">Antrag - Joker</option>
        <option value="bpp">Anmeldung BPP</option>
        <option value="abschlussarbeit">Abschlussarbeit</option>
        <option value="verlaengerung">Antrag auf Verlängerung</option>
      </select>
  
      <button @click="navigateToForm" :disabled="!selectedForm">Erstellen</button>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        selectedForm: ""
      };
    },
    methods: {
      navigateToForm() {
        if (this.selectedForm) {
          this.$router.push({ name: this.selectedForm });
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .form-selector-container {
    max-width: 600px;
    margin: auto;
    text-align: center;
    padding: 20px;
  }
  
  .dropdown {
    width: 100%;
    padding: 10px;
    margin: 20px 0;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  button {
    padding: 10px 20px;
    background-color: var(--primary-color);
    color: white;
    border: none;
    cursor: pointer;
    border-radius: 4px;
  }
  
  button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }
  </style>
  