<template>
    <div class="form-container">
      <h1>Antrag prüfen</h1>
  
      <!-- Details des Antrags anzeigen -->
      <div class="details">
        <p><strong>Fach:</strong> {{ antrag.fach || "Nicht angegeben" }}</p>
        <p><strong>Prüfungsnummer:</strong> {{ antrag.pruefungsnummer || "Nicht angegeben" }}</p>
        <p><strong>Status:</strong> {{ antrag.status || "Nicht angegeben" }}</p>
        <p><strong>Bemerkungen:</strong> {{ antrag.bemerkungen || "Keine Bemerkungen" }}</p>
        <p><strong>Name des Studierenden:</strong> {{ antrag.student_name || "Nicht angegeben" }}</p>
        <p><strong>Vorname des Studierenden:</strong> {{ antrag.student_vorname || "Nicht angegeben" }}</p>
        <p><strong>Matrikelnummer:</strong> {{ antrag.student_matrikelnummer || "Nicht angegeben" }}</p>
        <p><strong>Studiengang:</strong> {{ antrag.student_studiengang || "Nicht angegeben" }}</p>
      </div>
  
      <!-- Bearbeiten-Formular -->
      <form @submit.prevent="submitForm">
        <div class="form-group">
          <label for="entscheidung">Entscheidung:</label>
          <select v-model="form.entscheidung" id="entscheidung" @change="handleEntscheidungChange">
            <option value="" disabled>Bitte auswählen</option>
            <option value="keineBedenken">Gegen den Einsatz des Jokers bestehen keine Bedenken</option>
            <option value="bedenken">Gegen den Einsatz des Jokers bestehen Bedenken</option>
          </select>
        </div>
  
        <!-- Optionales Textfeld für Bedenken -->
        <div v-if="form.entscheidung === 'bedenken'" class="form-group">
          <label for="bedenken">Bedenken (optional):</label>
          <textarea id="bedenken" v-model="form.bedenken" placeholder="Geben Sie hier die Bedenken ein"></textarea>
        </div>
  
        <div class="form-group">
          <label for="unterschrift">Unterschrift hochladen:</label>
          <input type="file" id="unterschrift" @change="handleFileUpload" />
        </div>
  
        <div class="button-group">
          <button type="button" @click="cancelEdit">Abbrechen</button>
          <button type="submit">Speichern</button>
        </div>
      </form>
    </div>
  </template>
  
  <script>
export default {
  props: {
    antrag: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      form: {
        entscheidung: "", // Entscheidung des Prüfungsausschusses
        bedenken: "", // Optionales Feld für Bedenken
        unterschrift: null, // Datei-Upload
      },
    };
  },
  methods: {
    handleFileUpload(event) {
      const file = event.target.files[0];
      this.form.unterschrift = file;
    },
    handleEntscheidungChange() {
      // Bedenken zurücksetzen, falls keine Bedenken ausgewählt werden
      if (this.form.entscheidung !== "bedenken") {
        this.form.bedenken = "";
      }
    },
    async submitForm() {
      try {
        const formData = new FormData();
        formData.append("entscheidung", this.form.entscheidung);
        formData.append("bedenken", this.form.bedenken);
        if (this.form.unterschrift) {
          formData.append("unterschrift", this.form.unterschrift);
        }

        const token = localStorage.getItem("access_token");
        // Korrigierter Endpunkt
        const response = await fetch(`http://127.0.0.1:8000/api/antraege/pruefungsausschuss/${this.antrag.antrag_id}`, {
          method: "PUT",
          headers: {
            Authorization: `Bearer ${token}`,
          },
          body: formData,
        });

        if (!response.ok) {
          throw new Error("Fehler beim Speichern des Antrags");
        }

        this.$emit("update-success");
        alert("Antrag erfolgreich gespeichert!");
      } catch (error) {
        console.error("Fehler beim Speichern:", error);
        alert("Speichern des Antrags fehlgeschlagen.");
      }
    },
    cancelEdit() {
      this.$emit("cancel-edit");
    },
  },
};
</script>

  
  <style scoped>
  .form-container {
    max-width: 800px;
    margin: auto;
    padding: 20px;
  }
  
  h1 {
    text-align: center;
    color: #80ba24;
  }
  
  .details {
    margin-bottom: 20px;
    padding: 15px;
    border: 1px solid #ccc;
    border-radius: 8px;
    background-color: #f9f9f9;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  label {
    display: block;
    font-weight: bold;
    margin-bottom: 5px;
  }
  
  textarea,
  input[type="text"],
  input[type="file"],
  select {
    width: 100%;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
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
    background-color: #4a5c66;
  }
  
  button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }
  </style>
  