<template>
  <div class="form-container">
    <h1>Antrag - Joker</h1>

    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="vorname">Vorname</label>
        <input type="text" id="vorname" v-model="formData.vorname" placeholder="Vorname eingeben" />
      </div>

      <div class="form-group">
        <label for="nachname">Nachname</label>
        <input type="text" id="nachname" v-model="formData.nachname" placeholder="Nachname eingeben" />
      </div>

      <div class="form-group">
        <label for="fachbereich">Fachbereich</label>
        <input type="text" id="fachbereich" v-model="formData.fachbereich" placeholder="Fachbereich eingeben" />
      </div>

      <div class="form-group">
        <label for="studiengang">Studiengang</label>
        <input type="text" id="studiengang" v-model="formData.studiengang" placeholder="Studiengang eingeben" />
      </div>

      <!-- Button-Gruppe für Zurück und Speichern -->
      <div class="button-group">
        <button type="button" @click="goBack">Zurück</button>
        <button type="submit">Speichern</button>
      </div>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      formData: {
        vorname: '',
        nachname: '',
        fachbereich: '',
        studiengang: ''
      }
    };
  },
  methods: {
    handleSubmit() {
      console.log("Formular abgesendet mit den Daten:", this.formData);
    },
    goBack() {
      this.$router.push({ name: 'form-selector' }); // Navigation zurück zur FormSelector-Seite
    }
  }
};
</script>

<style scoped>
/* Stile für die Form */
.form-container {
  max-width: 600px;
  margin: auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
}

h1 {
  text-align: center;
  color: #4CAF50;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
}

input[type="text"] {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

/* Button-Gruppe Styling */
.button-group {
  display: flex;
  justify-content: space-between;
}

button {
  padding: 10px 20px;
  background-color: var(--primary-color);
  color: white;
  font-size: 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}

button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
</style>
