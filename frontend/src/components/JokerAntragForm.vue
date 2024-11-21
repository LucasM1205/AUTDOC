<template>
  <div class="form-container">
    <h1>Antrag - Joker</h1>

    <!-- Grunddaten Container mit Toggle -->
    <div class="grunddaten-container">
      <!-- Toggle zur automatischen Übernahme der Grunddaten -->
      <div class="form-group">
        <label>
          <input type="checkbox" v-model="autoFillGrunddaten" /> Automatisch ausfüllen
        </label>
      </div>

      <form>
        <div class="form-group">
          <label for="vorname">Vorname</label>
          <input 
            type="text" 
            id="vorname" 
            v-model="grunddaten.vorname" 
            :disabled="autoFillGrunddaten" 
            placeholder="Vorname eingeben" 
          />
        </div>

        <div class="form-group">
          <label for="nachname">Nachname</label>
          <input 
            type="text" 
            id="nachname" 
            v-model="grunddaten.nachname" 
            :disabled="autoFillGrunddaten" 
            placeholder="Nachname eingeben" 
          />
        </div>

        <div class="form-group">
          <label for="matrikelnummer">Matrikelnummer</label>
          <input 
            type="text" 
            id="matrikelnummer" 
            v-model="grunddaten.matrikelnummer" 
            :disabled="autoFillGrunddaten" 
            placeholder="Matrikelnummer eingeben" 
          />
        </div>

        <div class="form-group">
          <label for="fachbereich">Fachbereich</label>
          <input 
            type="text" 
            id="fachbereich" 
            v-model="grunddaten.fachbereich" 
            :disabled="autoFillGrunddaten" 
            placeholder="Fachbereich eingeben" 
          />
        </div>

        <div class="form-group">
          <label for="bachelorstudiengang">Bachelorstudiengang</label>
          <input 
            type="text" 
            id="bachelorstudiengang" 
            v-model="grunddaten.bachelorstudiengang" 
            :disabled="autoFillGrunddaten" 
            placeholder="Bachelorstudiengang eingeben" 
          />
        </div>
      </form>
    </div>

    <!-- Weiterführende Daten Container -->
    <div class="weiterfuehrende-daten-container">
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="fach">Fach</label>
          <input type="text" id="fach" v-model="weiterfuehrendeDaten.fach" placeholder="Fach eingeben" />
        </div>

        <div class="form-group">
          <label for="pruefungsnummer">Prüfungsnummer</label>
          <input type="text" id="pruefungsnummer" v-model="weiterfuehrendeDaten.pruefungsnummer" placeholder="Prüfungsnummer eingeben" />
        </div>

        <div class="form-group">
          <label for="fachbereichModul">Fachbereich des Moduls</label>
          <input type="text" id="fachbereichModul" v-model="weiterfuehrendeDaten.fachbereichModul" placeholder="Fachbereich des Moduls eingeben" />
        </div>

        <div class="form-group">
          <label for="pruefer">Prüfer</label>
          <input type="text" id="pruefer" v-model="weiterfuehrendeDaten.pruefer" placeholder="Prüfer eingeben" />
        </div>

        <div class="form-group">
          <label for="jokerStatus">Joker-Status</label>
          <select v-model="weiterfuehrendeDaten.jokerStatus" @change="checkDoppelstudium">
            <option disabled value="">Bitte wählen</option>
            <option value="keinJoker">Ich habe bisher noch keinen Joker verwendet</option>
            <option value="einJoker">Ich habe bisher einen Joker verwendet</option>
            <option value="doppelstudium">Ich studiere im Doppelstudium</option>
          </select>
        </div>

        <!-- Zusätzliche Eingabe für Bachelorstudiengang bei Doppelstudium -->
        <div v-if="weiterfuehrendeDaten.jokerStatus === 'doppelstudium'" class="form-group">
          <label for="doppelstudiumBachelor">Bachelorstudiengang</label>
          <input type="text" id="doppelstudiumBachelor" v-model="weiterfuehrendeDaten.doppelstudiumBachelor" placeholder="Bachelorstudiengang eingeben" />
        </div>

        <!-- Button-Gruppe für Zurück und Speichern -->
        <div class="button-group">
          <button type="button" @click="goBack">Zurück</button>
          <button type="submit">Speichern</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      autoFillGrunddaten: false,
      grunddaten: {
        vorname: '',
        nachname: '',
        matrikelnummer: '',
        fachbereich: '',
        bachelorstudiengang: ''
      },
      weiterfuehrendeDaten: {
        fach: '',
        pruefungsnummer: '',
        fachbereichModul: '',
        pruefer: '',
        jokerStatus: '',
        doppelstudiumBachelor: ''
      }
    };
  },
  methods: {
    async handleSubmit() {
      try {
        const requestData = {
          vorname: this.grunddaten.vorname,
          nachname: this.grunddaten.nachname,
          matrikelnummer: this.grunddaten.matrikelnummer,
          fachbereich: this.grunddaten.fachbereich,
          bachelorstudiengang: this.grunddaten.bachelorstudiengang,
          fach: this.weiterfuehrendeDaten.fach,
          pruefungsnummer: this.weiterfuehrendeDaten.pruefungsnummer,
          fachbereich_modul: this.weiterfuehrendeDaten.fachbereichModul,
          pruefer: this.weiterfuehrendeDaten.pruefer,
          joker_status: this.weiterfuehrendeDaten.jokerStatus,
          doppelstudium_bachelor: this.weiterfuehrendeDaten.doppelstudiumBachelor || "",
        };

        console.log("Gesendete Daten:", requestData);

        const response = await fetch("http://127.0.0.1:8000/generate-pdf", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(requestData)
        });

        if (!response.ok) {
          console.error(`Fehlerstatus: ${response.status}`);
          const errorDetails = await response.json();
          console.error("Fehlerdetails:", errorDetails);
          throw new Error(`Fehler beim Erstellen der PDF-Datei: ${errorDetails.detail || 'Unbekannter Fehler'}`);
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);

        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", "joker_antrag_ausgefuellt.pdf");
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        console.log("PDF erfolgreich generiert und heruntergeladen!");
      } catch (error) {
        console.error("Fehler:", error.message);
      }
    },
    goBack() {
      this.$router.push({ name: 'form-selector' });
    },
    checkDoppelstudium() {
      if (this.weiterfuehrendeDaten.jokerStatus !== 'doppelstudium') {
        this.weiterfuehrendeDaten.doppelstudiumBachelor = '';
      }
    }
  }
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

.grunddaten-container,
.weiterfuehrende-daten-container {
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
