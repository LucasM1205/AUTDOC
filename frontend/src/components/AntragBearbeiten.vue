<template>
    <div class="form-container">
      <h1>Antrag bearbeiten</h1>
      
      <!-- Details des Antrags anzeigen -->
      <div class="details">
        <p><strong>Fach:</strong> {{ antrag.fach || "Nicht angegeben" }}</p>
        <p><strong>Prüfungsnummer:</strong> {{ antrag.pruefungsnummer || "Nicht angegeben" }}</p>
        <p><strong>Status:</strong> {{ antrag.status || "Nicht angegeben" }}</p>
        <p><strong>Bemerkungen:</strong> {{ antrag.bemerkungen || "Keine Bemerkungen" }}</p>
        <p><strong>Joker verwendet:</strong> {{ antrag.joker_verwendet ? "Ja" : "Nein" }}</p>
        <p><strong>Doppelstudium:</strong> {{ antrag.doppelstudium ? "Ja" : "Nein" }}</p>
        <p><strong>Name des Studierenden:</strong> {{ antrag.student_name || "Nicht angegeben" }}</p>
        <p><strong>Vorname des Studierenden:</strong> {{ antrag.student_vorname || "Nicht angegeben" }}</p>
        <p><strong>Matrikelnummer:</strong> {{ antrag.student_matrikelnummer || "Nicht angegeben" }}</p>
        <p><strong>Studiengang:</strong> {{ antrag.student_studiengang || "Nicht angegeben" }}</p>
      </div>
  
      <!-- Bearbeiten-Formular -->
      <form @submit.prevent="submitForm">
        <div class="form-group">
          <label for="jokerVerfuegbar">Joker verfügbar</label>
          <select v-model="form.joker_verfuegbar" id="jokerVerfuegbar">
            <option value="" disabled>Bitte auswählen</option>
            <option value="true">Ja</option>
            <option value="false">Nein</option>
          </select>
        </div>
        <div class="form-group">
          <label for="bemerkungen">Bemerkungen</label>
          <textarea id="bemerkungen" v-model="form.bemerkungen" placeholder="Bemerkungen eingeben"></textarea>
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
          joker_verfuegbar: this.antrag.joker_verfuegbar,
          bemerkungen: this.antrag.bemerkungen,
          status: this.antrag.status, // Status hinzufügen
        },
      };
    },
    methods: {
      async submitForm() {
        try {
          // Dynamischer Status basierend auf joker_verfuegbar
          if (this.form.joker_verfuegbar === "true") {
            this.form.status =
              "Antrag durch Sekretariat genehmigt; Rückmeldung durch Prüfungsausschuss ausstehend";
          } else if (this.form.joker_verfuegbar === "false") {
            this.form.status = "Antrag durch Sekretariat abgelehnt";
          }
  
          console.log("DEBUG: Zu sendende Formulardaten:", this.form); // Debugging
  
          const response = await fetch(
            `http://127.0.0.1:8000/api/antraege/${this.antrag.antrag_id}`,
            {
              method: "PUT",
              headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${localStorage.getItem("access_token")}`,
              },
              body: JSON.stringify(this.form),
            }
          );
  
          if (!response.ok) {
            const errorText = await response.text();
            console.error("DEBUG: Fehlertext beim Speichern:", errorText); // Debugging
            throw new Error("Fehler beim Speichern des Antrags");
          }
  
          const responseData = await response.json();
          console.log("DEBUG: Antwort des Servers:", responseData); // Debugging
          this.$emit("update-success");
        } catch (error) {
          console.error("Fehler beim Speichern:", error); // Debugging
        }
      },
      cancelEdit() {
        console.log("DEBUG: Bearbeiten abgebrochen"); // Debugging
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
  
  .sekretariat-form {
    margin-top: 20px;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 8px;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
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
  