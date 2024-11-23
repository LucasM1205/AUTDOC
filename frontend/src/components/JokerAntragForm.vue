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

        <!-- Unterschrift-Upload -->
        <div class="form-group">
          <label for="unterschrift">Unterschrift hochladen</label>
          <input
            type="file"
            id="unterschrift"
            @change="handleFileUpload"
            accept="image/png"
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
          <input
            type="text"
            id="pruefungsnummer"
            v-model="weiterfuehrendeDaten.pruefungsnummer"
            placeholder="Prüfungsnummer eingeben"
          />
        </div>

        <div class="form-group">
          <label for="fachbereichModul">Fachbereich des Moduls</label>
          <input
            type="text"
            id="fachbereichModul"
            v-model="weiterfuehrendeDaten.fachbereichModul"
            placeholder="Fachbereich des Moduls eingeben"
          />
        </div>

        <div class="form-group">
          <label for="pruefer">Prüfer</label>
          <input
            type="text"
            id="pruefer"
            v-model="weiterfuehrendeDaten.pruefer"
            placeholder="Prüfer eingeben"
          />
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
          <input
            type="text"
            id="doppelstudiumBachelor"
            v-model="weiterfuehrendeDaten.doppelstudiumBachelor"
            placeholder="Bachelorstudiengang eingeben"
          />
        </div>

        <!-- Button-Gruppe für Zurück, Vorschau und Speichern -->
        <div class="button-group">
          <button type="button" @click="goBack">Zurück</button>
          <button type="button" @click="previewPDF">Vorschau</button>
          <button type="submit">Speichern</button>
        </div>
      </form>
    </div>

    <!-- Vorschau-Modal -->
    <div v-if="showPreview" class="preview-modal">
      <div class="preview-container">
        <button @click="closePreview">Schließen</button>
        <iframe id="pdf-preview" :src="previewUrl" frameborder="0" style="width: 100%; height: 500px;"></iframe>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      autoFillGrunddaten: false,
      showPreview: false,
      previewUrl: "", // Vorschau-URL für das iframe
      grunddaten: {
        vorname: '',
        nachname: '',
        matrikelnummer: '',
        fachbereich: '',
        bachelorstudiengang: '',
        unterschrift: null,
      },
      weiterfuehrendeDaten: {
        fach: '',
        pruefungsnummer: '',
        fachbereichModul: '',
        pruefer: '',
        jokerStatus: '',
        doppelstudiumBachelor: '',
      },
    };
  },
  methods: {
    handleFileUpload(event) {
      this.grunddaten.unterschrift = event.target.files[0];
      console.log('Unterschrift hochgeladen:', this.grunddaten.unterschrift);
    },
    async previewPDF() {
      try {
        const formData = new FormData();
        formData.append('vorname', this.grunddaten.vorname);
        formData.append('nachname', this.grunddaten.nachname);
        formData.append('matrikelnummer', this.grunddaten.matrikelnummer);
        formData.append('fachbereich', this.grunddaten.fachbereich);
        formData.append('bachelorstudiengang', this.grunddaten.bachelorstudiengang);
        formData.append('unterschrift', this.grunddaten.unterschrift);
        formData.append('fach', this.weiterfuehrendeDaten.fach);
        formData.append('pruefungsnummer', this.weiterfuehrendeDaten.pruefungsnummer);
        formData.append('fachbereich_modul', this.weiterfuehrendeDaten.fachbereichModul);
        formData.append('pruefer', this.weiterfuehrendeDaten.pruefer);
        formData.append('joker_status', this.weiterfuehrendeDaten.jokerStatus);
        formData.append('doppelstudium_bachelor', this.weiterfuehrendeDaten.doppelstudiumBachelor || '');

        const response = await fetch('http://127.0.0.1:8000/preview-pdf', {
          method: 'POST',
          body: formData,
        });

        if (!response.ok) throw new Error('Fehler bei der Vorschau');

        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        this.previewUrl = url;
        this.showPreview = true;
      } catch (error) {
        console.error('Fehler bei der Vorschau:', error);
      }
    },
    closePreview() {
      this.showPreview = false;
      this.previewUrl = "";
    },
    async handleSubmit() {
      try {
        const formData = new FormData();
        formData.append('vorname', this.grunddaten.vorname);
        formData.append('nachname', this.grunddaten.nachname);
        formData.append('matrikelnummer', this.grunddaten.matrikelnummer);
        formData.append('fachbereich', this.grunddaten.fachbereich);
        formData.append('bachelorstudiengang', this.grunddaten.bachelorstudiengang);
        formData.append('unterschrift', this.grunddaten.unterschrift);
        formData.append('fach', this.weiterfuehrendeDaten.fach);
        formData.append('pruefungsnummer', this.weiterfuehrendeDaten.pruefungsnummer);
        formData.append('fachbereich_modul', this.weiterfuehrendeDaten.fachbereichModul);
        formData.append('pruefer', this.weiterfuehrendeDaten.pruefer);
        formData.append('joker_status', this.weiterfuehrendeDaten.jokerStatus);
        formData.append('doppelstudium_bachelor', this.weiterfuehrendeDaten.doppelstudiumBachelor || '');

        const response = await fetch('http://127.0.0.1:8000/generate-pdf', {
          method: 'POST',
          body: formData,
        });

        if (!response.ok) {
          const errorDetails = await response.json();
          console.error('Fehlerdetails:', errorDetails);
          throw new Error(`Fehler beim Erstellen der PDF-Datei: ${errorDetails.detail}`);
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);

        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'joker_antrag_ausgefuellt.pdf');
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        console.log('PDF erfolgreich generiert und heruntergeladen!');
      } catch (error) {
        console.error('Fehler:', error.message);
      }
    },
    goBack() {
      this.$router.push({ name: 'form-selector' });
    },
    checkDoppelstudium() {
      if (this.weiterfuehrendeDaten.jokerStatus !== 'doppelstudium') {
        this.weiterfuehrendeDaten.doppelstudiumBachelor = '';
      }
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

input[type='text'],
select,
input[type='file'] {
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

.preview-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
}

.preview-container {
  background: white;
  padding: 20px;
  border-radius: 10px;
  max-width: 80%;
  max-height: 80%;
  overflow: auto;
}

iframe {
  border: none;
}
</style>
