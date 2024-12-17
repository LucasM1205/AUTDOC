<template>
    <div class="form-container">
      <h1>Antrag auf Zulassung zur Abschlussarbeit und –prüfung</h1>
  
      <!-- Formularabschnitt -->
      <form @submit.prevent="handleSubmit">
        <!-- Persönliche Angaben -->
        <fieldset class="section">
          <legend>Persönliche Angaben</legend>
          
          <!-- Automatisch ausfüllen Checkbox -->
          <div class="form-group checkbox-container">
            <label>
              <input type="checkbox" v-model="formData.autoAusfuellen" />
              Automatisch ausfüllen
            </label>
          </div>
  
          <!-- Persönliche Angaben Eingabefelder -->
          <div class="form-group">
            <label for="vorname">Vorname</label>
            <input type="text" id="vorname" v-model="formData.vorname" placeholder="Vorname eingeben" />
          </div>
          <div class="form-group">
            <label for="nachname">Nachname</label>
            <input type="text" id="nachname" v-model="formData.nachname" placeholder="Nachname eingeben" />
          </div>
          <div class="form-group">
            <label for="strasse">Straße</label>
            <input type="text" id="strasse" v-model="formData.strasse" placeholder="Straße eingeben" />
          </div>
          <div class="form-group">
            <label for="plzOrt">PLZ/Ort</label>
            <input type="text" id="plzOrt" v-model="formData.plzOrt" placeholder="PLZ/Ort eingeben" />
          </div>
          <div class="form-group">
            <label for="matrikelnummer">Matrikelnummer</label>
            <input type="text" id="matrikelnummer" v-model="formData.matrikelnummer" placeholder="Matrikelnummer eingeben" />
          </div>
          <div class="form-group">
            <label for="email">THM-E-Mail-Adresse</label>
            <input type="email" id="email" v-model="formData.email" placeholder="THM-E-Mail-Adresse eingeben" />
          </div>
  
          <!-- Studienabschluss Checkboxen (Bachelor und Master) -->
          <div class="form-group">
            <label>Studienabschluss:</label>
            <div class="checkbox-group">
              <label>
                <input type="checkbox" v-model="formData.bachelor" /> Bachelor
              </label>
              <label>
                <input type="checkbox" v-model="formData.master" /> Master
              </label>
            </div>
          </div>
  
          <div class="form-group">
            <label for="unterschrift">Unterschrift hochladen</label>
            <input type="file" id="unterschrift" @change="handleFileUploadUnterschrift" />
          </div>
        </fieldset>
  
        <!-- Prüfungsdetails -->
        <fieldset class="section">
          <legend>Prüfungsdetails</legend>
          
          <!-- Thema der Arbeit Eingabefeld -->
          <div class="form-group">
            <label for="thema">Thema der Arbeit</label>
            <textarea id="thema" v-model="formData.thema" placeholder="Thema der Arbeit eingeben"></textarea>
          </div>
          
          <!-- Weitere Prüfungsdetails Eingabefelder -->
          <div class="form-group">
            <label for="pruefer1">1. Prüfer(in) (THM)</label>
            <input type="text" id="pruefer1" v-model="formData.pruefer1" placeholder="Name des Prüfers" />
          </div>
          <div class="form-group">
            <label for="pruefer2">2. Prüfer(in) (THM oder Institution)</label>
            <input type="text" id="pruefer2" v-model="formData.pruefer2" placeholder="Name des Prüfers" />
          </div>
          <div class="form-group">
            <label for="unterschriftPruefer2">Unterschrift 2. Prüfer(in):</label>
            <input type="file" id="unterschriftPruefer2" @change="handleFileUploadPruefer2" />
          </div>
          <div class="form-group">
            <label for="starttermin">Gewünschter Starttermin der Abschlussarbeit:</label>
            <input type="date" id="starttermin" v-model="formData.starttermin" />
          </div>
          <div class="form-group">
            <label for="datumStudierender">Datum:</label>
            <input type="date" id="datumStudierender" v-model="formData.datumStudierender" />
          </div>
          <div class="form-group">
            <label for="unterschriftStudierender">Unterschrift Studierende(r):</label>
            <input type="file" id="unterschriftStudierender" @change="handleFileUploadStudierender" />
          </div>
        </fieldset>
  
        <!-- Entscheidung des Prüfungsausschusses -->
        <fieldset class="section">
          <legend>Entscheidung des Prüfungsausschusses</legend>
          <div class="form-group checkbox-inline">
            <label>
              <input type="checkbox" v-model="formData.zulassungAngenommen" /> Antrag auf Zulassung angenommen
            </label>
            <label>
              <input type="checkbox" v-model="formData.zulassungAbgelehnt" /> Antrag auf Zulassung abgelehnt
            </label>
            <label>
              <input type="checkbox" v-model="formData.korrekturErforderlich" /> Korrektur erforderlich
            </label>
          </div>
  
          <!-- Info-Feld für "Korrektur erforderlich" -->
          <div v-if="formData.korrekturErforderlich" class="form-group">
            <label for="korrekturInfo">Weitere Information:</label>
            <input type="text" id="korrekturInfo" v-model="formData.korrekturInfo" placeholder="Weitere Information eingeben" />
          </div>
  
          <div v-if="formData.zulassungAbgelehnt" class="form-group">
            <label for="begruendung">Begründung:</label>
            <input type="text" id="begruendung" v-model="formData.begruendung" placeholder="Begründung eingeben" />
          </div>
          <div class="form-group">
            <label>Externer Prüfer(in):</label>
            <div class="checkbox-group">
              <label>
                <input type="checkbox" v-model="formData.externerZugelassen" /> Zugelassen
              </label>
              <label>
                <input type="checkbox" v-model="formData.externerNichtZugelassen" /> Nicht zugelassen
              </label>
            </div>
          </div>
          <div class="form-group" v-if="formData.externerNichtZugelassen">
            <label for="externerBegruendung">Begründung (falls nicht zugelassen)</label>
            <input type="text" id="externerBegruendung" v-model="formData.externerBegruendung" placeholder="Begründung eingeben" />
          </div>
          <div class="form-group">
            <label for="datum">Datum</label>
            <input type="date" id="datum" v-model="formData.datum" />
          </div>
          <div class="form-group">
            <label for="unterschriftAusschuss">Unterschrift Ausschussvorsitzende(r):</label>
            <input type="file" id="unterschriftAusschuss" @change="handleFileUploadAusschuss" />
          </div>
        </fieldset>
  
        <!-- Ausgabe der Abschlussarbeit -->
        <fieldset class="section">
          <legend>Ausgabe der Abschlussarbeit</legend>
          
          <!-- (von der/dem 1. Prüfer(in) auszufüllen) Text -->
          <div class="form-group">
            <span class="info-text">(von der/dem 1. Prüfer(in) auszufüllen)</span>
          </div>
  
          <div class="form-group checkbox-inline">
            <label>
              <input type="checkbox" v-model="formData.bestaetigungVorschlaege" /> Bestätigung der Vorschläge der Kandidaten
            </label>
            <label>
              <input type="checkbox" v-model="formData.neinSieheUnten" /> Nein (siehe unten)
            </label>
          </div>
          <div class="form-group inline-group">
            <div>
              <label for="beginn">Beginn:</label>
              <input type="date" id="beginn" v-model="formData.beginn" />
            </div>
            <div>
              <label for="abgabe">Abgabe:</label>
              <input type="date" id="abgabe" v-model="formData.abgabe" />
            </div>
          </div>
          <div class="form-group">
            <label for="ausgabeDatum">Datum</label>
            <input type="date" id="ausgabeDatum" v-model="formData.ausgabeDatum" />
          </div>
          <div class="form-group">
            <label for="ausgabeUnterschrift">Unterschrift 1. Prüfer(in):</label>
            <input type="file" id="ausgabeUnterschrift" @change="handleFileUploadAusgabe" />
          </div>
        </fieldset>
  
        <!-- Buttons -->
        <div class="button-group">
          <button type="button" class="btn" @click="goBack">Zurück</button>
          <button type="button" class="btn" @click="previewPDF">Vorschau</button>
          <button type="submit" class="btn">Speichern</button>
        </div>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        formData: {
          autoAusfuellen: false,
          vorname: "",
          nachname: "",
          matrikelnummer: "",
          fachbereich: "",
          bachelorstudiengang: "",
          unterschrift: null,
          fach: "",
          pruefungsnummer: "",
          modulbereich: "",
          pruefer: "",
          bachelor: false,
          master: false,
          zulassungAngenommen: false,
          zulassungAbgelehnt: false,
          begruendung: "",
          externerZugelassen: false,
          externerNichtZugelassen: false,
          externerBegruendung: "",
          datum: "",
          ausgabeDatum: "",
          bestaetigungVorschlaege: false,
          neinSieheUnten: false,
          beginn: "",
          abgabe: "",
          strasse: "",
          plzOrt: "",
          datumStudierender: "",
          korrekturErforderlich: false,
          korrekturInfo: "",
          thema: "" // Hinzugefügt für das Thema der Arbeit
        }
      };
    },
    methods: {
      handleFileUploadUnterschrift(event) {
        console.log(event.target.files[0]);
      },
      handleFileUploadAusschuss(event) {
        console.log(event.target.files[0]);
      },
      handleFileUploadAusgabe(event) {
        console.log(event.target.files[0]);
      },
      handleFileUploadPruefer2(event) {
        console.log(event.target.files[0]);
      },
      handleFileUploadStudierender(event) {
        console.log(event.target.files[0]);
      },
      handleSubmit() {
        console.log("Formular abgeschickt:", this.formData);
      },
      previewPDF() {
        console.log("Vorschau wird angezeigt:", this.formData);
      },
      goBack() {
        console.log("Zurück gedrückt");
      }
    }
  };
  </script>
  
  <style scoped>
  .form-container {
    max-width: 900px;
    margin: 0 auto;
    font-family: Arial, sans-serif;
  }
  
  h1 {
    text-align: center;
    color: #80ba24;
  }
  
  .section {
    margin-bottom: 20px;
    padding: 15px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  .checkbox-container {
    margin-bottom: 20px;
  }
  
  .checkbox-group {
    display: flex;
    gap: 15px;
  }
  
  .checkbox-inline {
    display: flex;
    justify-content: flex-start;
    gap: 20px;
  }
  
  .inline-group {
    display: flex;
    gap: 20px;
  }
  
  .inline-group > div {
    flex: 1;
  }
  
  button {
    background-color: #80ba24;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    width: 30%;
  }
  
  button:hover {
    background-color: #4e8c1e;
  }
  
  button:first-child {
    margin-right: 20px;
  }
  
  button:nth-child(2) {
    margin-left: 20px;
    margin-right: 20px;
  }
  
  button:last-child {
    margin-left: 20px;
  }
  
  input[type="text"], input[type="email"], input[type="date"], input[type="file"], textarea {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    margin-top: 5px;
  }
  
  textarea {
    resize: vertical;
  }
  
  input[type="checkbox"] {
    margin-right: 10px;
  }
  
  .info-text {
    display: block;
    font-size: 0.9em;
    color: #555;
    margin-top: 10px;
  }
  </style>
  