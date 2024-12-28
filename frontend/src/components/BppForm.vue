<template>
    <div class="form-container">
      <!-- Titel in THM-Grün -->
      <h1 class="title-green">Anmeldung zur Berufspraktischen Phase (BPP)</h1>
  
      <div class="form-group">
    <input 
      type="checkbox" 
      id="autoAusfuellen" 
      v-model="bppForm.autoAusfuellen"
      style="margin-right: 10px;"
    />
    <label for="autoAusfuellen" style="font-weight: normal;">Automatisch ausfüllen</label>
  </div>
  
  
      <!-- Persönliche Daten -->
      <div class="form-group-container">
        <h2>Persönliche Daten</h2>
  
        <div class="form-group">
          <label for="vorname">Vorname</label>
          <input
            type="text"
            id="vorname"
            v-model="bppForm.vorname"
            placeholder="Vorname eingeben"
          />
        </div>
  
        <div class="form-group">
          <label for="nachname">Nachname</label>
          <input
            type="text"
            id="nachname"
            v-model="bppForm.nachname"
            placeholder="Nachname eingeben"
          />
        </div>
  
        <div class="form-group">
          <label for="matrikelnummer">Matrikelnummer</label>
          <input
            type="text"
            id="matrikelnummer"
            v-model="bppForm.matrikelnummer"
            placeholder="Matrikelnummer eingeben"
          />
        </div>
  
        <div class="form-group">
      <label for="aktuellesDatum">Datum des Antrags</label>
      <input
        type="date"
        id="aktuellesDatum"
        v-model="bppForm.aktuellesDatum"
      />
    </div>
  
    <div class="form-group">
      <label for="ort">Ort</label>
      <input
        type="text"
        id="ort"
        v-model="bppForm.ort"
        placeholder="Ort eingeben"
      />
    </div>
  
        <div class="form-group">
          <label for="unterschrift">Unterschrift hochladen</label>
          <input
            type="file"
            id="unterschrift"
            @change="handleFileUpload"
            accept="image/*"
          />
          <p v-if="bppForm.unterschrift">
            Hochgeladen: {{ bppForm.unterschrift.name }}
          </p>
        </div>
      </div>
  
      <!-- Zulassungsstatus -->
      <div class="form-group-container">
        <form>
          <div class="form-group">
            <label>Zulassung</label>
            <div>
              <label>
                <input
                  type="radio"
                  value="zulassungVorhanden"
                  v-model="bppForm.zulassung"
                />
                Meine Zulassung liegt vor
              </label>
            </div>
            <div>
              <label>
                <input
                  type="radio"
                  value="zulassungUnterVorbehalt"
                  v-model="bppForm.zulassung"
                />
                Zulassung unter Vorbehalt beantragen
              </label>
            </div>
          </div>
  
          <!-- WIS2-Daten -->
          <div
            v-if="bppForm.zulassung === 'zulassungUnterVorbehalt'"
            class="form-group"
          >
            <label for="wis2Abgabe">Abgabedatum WIS2</label>
            <input type="date" id="wis2Abgabe" v-model="bppForm.wis2Abgabe" />
            <label for="wis2Vortrag">Vortragsdatum WIS2</label>
            <input type="date" id="wis2Vortrag" v-model="bppForm.wis2Vortrag" />
          </div>
        </form>
      </div>
  
      <!-- Beginn und Ende der BPP -->
      <div class="form-group-container">
        <h2>Zeitraum der BPP</h2>
        <div class="form-group">
          <label for="bppBeginn">Beginn der BPP</label>
          <input type="date" id="bppBeginn" v-model="bppForm.bppBeginn" />
        </div>
        <div class="form-group checkbox-row">
          <input type="checkbox" v-model="bppForm.bppEndeCheckbox" />
          <span>Ende der BPP</span>
          <input
            v-if="bppForm.bppEndeCheckbox"
            type="date"
            id="bppEnde"
            v-model="bppForm.bppEnde"
          />
        </div>
        <div class="form-group checkbox-row">
          <input type="checkbox" v-model="bppForm.stundenVariante" />
          <span>800-Stunden-Variante</span>
        </div>
      </div>
  
      <!-- Anschrift der BPP-Stelle -->
      <div class="form-group-container">
        <h2>Anschrift der BPP-Stelle</h2>
  
        <div class="form-group">
          <label for="bppName">Name</label>
          <input
            type="text"
            id="bppName"
            v-model="bppForm.bppName"
            placeholder="Name der BPP-Stelle"
          />
        </div>
  
        <div class="form-group">
          <label for="bppAbteilung">Abteilung</label>
          <input
            type="text"
            id="bppAbteilung"
            v-model="bppForm.bppAbteilung"
            placeholder="Abteilung eingeben"
          />
        </div>
  
        <div class="form-group">
          <label for="bppBetreuer">Betreuer/in</label>
          <input
            type="text"
            id="bppBetreuer"
            v-model="bppForm.bppBetreuer"
            placeholder="Betreuer/in eingeben"
          />
        </div>
  
        <div class="form-group">
          <label for="bppStrasse">Straße</label>
          <input
            type="text"
            id="bppStrasse"
            v-model="bppForm.bppStrasse"
            placeholder="Straße eingeben"
          />
        </div>
  
        <div class="form-group">
          <label for="bppPostfach">Postfach</label>
          <input
            type="text"
            id="bppPostfach"
            v-model="bppForm.bppPostfach"
            placeholder="Postfach eingeben"
          />
        </div>
  
        <div class="form-group">
          <label for="bppPlz">PLZ</label>
          <input
            type="text"
            id="bppPlz"
            v-model="bppForm.bppPlz"
            placeholder="PLZ eingeben"
          />
        </div>
  
        <div class="form-group">
          <label for="bppOrt">Ort</label>
          <input
            type="text"
            id="bppOrt"
            v-model="bppForm.bppOrt"
            placeholder="Ort eingeben"
          />
        </div>
  
        <div class="form-group">
          <label for="bppTelefon">Telefon</label>
          <input
            type="text"
            id="bppTelefon"
            v-model="bppForm.bppTelefon"
            placeholder="Telefonnummer eingeben"
          />
        </div>
  
        <div class="form-group">
          <label for="bppTaetigkeit">Inhalt der praktischen Tätigkeit</label>
          <textarea
            id="bppTaetigkeit"
            v-model="bppForm.bppTaetigkeit"
            placeholder="Beschreibung der Tätigkeit (max. 2 Sätze)"
          ></textarea>
        </div>
      </div>
  
      <!-- Betreuende/r Dozent/in der THM -->
      <div class="form-group-container">
        <h2>Betreuende/r Dozent/in der THM</h2>
        <div class="form-group">
          <label for="dozentName">Name</label>
          <input
            type="text"
            id="dozentName"
            v-model="bppForm.dozentName"
            placeholder="Name eingeben"
          />
        </div>
        <div class="form-group">
          <label for="dozentDatum">Datum</label>
          <input type="date" id="dozentDatum" v-model="bppForm.dozentDatum" />
        </div>
        <div class="form-group">
          <label for="dozentUnterschrift">Unterschrift hochladen</label>
          <input
            type="file"
            id="dozentUnterschrift"
            @change="handleDozentFileUpload"
            accept="image/*"
          />
          <p v-if="bppForm.dozentUnterschrift">
            Hochgeladen: {{ bppForm.dozentUnterschrift.name }}
          </p>
        </div>
      </div>
  
      <!-- Buttons -->
      <div class="button-group">
        <button type="button" @click="goBack">Zurück</button>
        <button type="button" @click="handlePreview">Vorschau</button>
        <button type="submit" @click.prevent="handleSave">Speichern</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      const today = new Date().toISOString().split('T')[0];
      return {
        bppForm: {
          vorname: "",
          nachname: "",
          matrikelnummer: "",
          unterschrift: null,
          aktuellesDatum: today,
          ort:"",
          zulassung: "",
          wis2Abgabe: "",
          wis2Vortrag: "",
          bppBeginn: "",
          bppEndeCheckbox: false,
          bppEnde: "",
          stundenVariante: false,
          bppName: "",
          bppAbteilung: "",
          bppBetreuer: "",
          bppStrasse: "",
          bppPostfach: "",
          bppPlz: "",
          bppOrt: "",
          bppTelefon: "",
          bppTaetigkeit: "",
          dozentName: "",
          dozentDatum: "",
          dozentUnterschrift: null,
        },
      };
    },
    
    methods: {
      handleFileUpload(event) {
        this.bppForm.unterschrift = event.target.files[0];
      },
      handleDozentFileUpload(event) {
        this.bppForm.dozentUnterschrift = event.target.files[0];
      },
      goBack() {
        console.log("Zurück zur vorherigen Seite");
      },
      handlePreview() {
        console.log("Vorschau anzeigen");
      },
      handleSave() {
        console.log("Formular gespeichert:", this.bppForm);
      },
    },
    };
  </script>
  
  <style scoped>
  .form-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    font-family: Arial, sans-serif;
  }
  
  .title-green {
    color: #80ba24; /* THM Grün */
    text-align: center;
  }
  
  .section-title {
    font-weight: bold;
    margin-bottom: 15px;
  }
  
  .form-group-container {
    border: 1px solid #ddd;
    padding: 20px;
    margin-bottom: 20px;
    border-radius: 5px;
  }
  
  .form-group {
    display: flex;
    align-items: center;
    margin-bottom: 15px;
  }
  
  label {
    font-weight: bold;
    width: 200px;
  }
  
  input[type="text"],
  input[type="file"],
  textarea {
    flex: 1;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  
  .radio-group {
    display: flex;
    flex-direction: column;
  }
  
  textarea {
    resize: none;
  }
  
  .button-group button {
    background-color: #80ba24; /* THM Grün */
    color: #fff; /* Weißer Text */
    border: none; /* Kein Rahmen */
    padding: 10px 20px; /* Innenabstand */
    margin: 0 10px; /* Abstand zwischen Buttons */
    border-radius: 5px; /* Abgerundete Ecken */
    cursor: pointer; /* Mauszeiger als Zeiger */
    font-size: 16px; /* Schriftgröße */
    font-weight: bold; /* Fettdruck */
    text-align: center; /* Zentrierter Text */
  }
  
  .button-group button:hover {
    background-color: #6e9e1b; /* Dunkleres Grün beim Hovern */
  }
  
  .button-group {
    display: flex; /* Buttons nebeneinander ausrichten */
    justify-content: center; /* Zentriert anzeigen */
    align-items: center; /* Vertikale Zentrierung */
    margin-top: 20px; /* Abstand nach oben */
  }
  
  </style>
  