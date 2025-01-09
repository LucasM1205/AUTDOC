<template>
    <div class="form-container">
      <h1>Antrag - extPrüfer</h1>
  
      <!-- Checkbox Automatisch ausfüllen -->
      <div class="form-group">
        <label>
          <input type="checkbox" v-model="autoFillGrunddaten" /> Automatisch ausfüllen
        </label>
      </div>
  
      <!-- Persönliche Daten des Studierenden -->
      <div class="grunddaten-container">
        <h2>Persönliche Daten des Studierenden</h2>
        <form>
          <!-- Checkbox für Bachelor oder Master -->
          <div class="form-group">
            <label>Studiengang</label>
            <div>
              <label>
                <input
                  type="radio"
                  v-model="studierendeDaten.studiengang"
                  value="bachelor"
                  :disabled="autoFillGrunddaten"
                />
                Bachelor
              </label>
              <label>
                <input
                  type="radio"
                  v-model="studierendeDaten.studiengang"
                  value="master"
                  :disabled="autoFillGrunddaten"
                />
                Master
              </label>
            </div>
          </div>
  
          <div class="form-group">
            <label for="vorname">Vorname</label>
            <input
              type="text"
              id="vorname"
              v-model="studierendeDaten.vorname"
              :disabled="autoFillGrunddaten"
              placeholder="Vorname eingeben"
            />
          </div>
  
          <div class="form-group">
            <label for="name">Nachname</label>
            <input
              type="text"
              id="name"
              v-model="studierendeDaten.name"
              :disabled="autoFillGrunddaten"
              placeholder="Nachname eingeben"
            />
          </div>
  
          <div class="form-group">
            <label for="matrikelnummer">Matrikelnummer</label>
            <input
              type="text"
              id="matrikelnummer"
              v-model="studierendeDaten.matrikelnummer"
              :disabled="autoFillGrunddaten"
              placeholder="Matrikelnummer eingeben"
            />
          </div>
        </form>
      </div>
  
  
  
      <!-- Persönliche Daten -->
      <div class="weiterfuehrende-daten-container">
        <h2>Persönliche Daten des 2. externen Prüfers</h2>
        <form>
          <div class="form-group">
            <label for="zweitprueferName">Name, Vorname</label>
            <input
              type="text"
              id="zweitprueferName"
              v-model="zweitprueferDaten.name"
              placeholder="Name und Vorname eingeben"
            />
          </div>
  
          <div class="form-group">
            <label for="zweitprueferEmail">E-Mail-Adresse</label>
            <input
              type="email"
              id="zweitprueferEmail"
              v-model="zweitprueferDaten.email"
              placeholder="E-Mail-Adresse eingeben"
            />
          </div>
  
          <div class="form-group">
            <label for="zweitprueferTelefon">Telefonnummer</label>
            <input
              type="tel"
              id="zweitprueferTelefon"
              v-model="zweitprueferDaten.telefon"
              placeholder="Telefonnummer eingeben"
            />
          </div>
        </form>
      </div>
  
      <!-- Hochschulabschluss -->
      <div class="weiterfuehrende-daten-container">
        <h2>Hochschulabschluss</h2>
        <form>
          <div class="form-group">
            <label for="hochschule">Name der Hochschule</label>
            <input
              type="text"
              id="hochschule"
              v-model="hochschulabschluss.hochschule"
              placeholder="Name der Hochschule eingeben"
            />
          </div>
  
          <div class="form-group">
            <label for="akademischerGrad">Akademischer Grad</label>
            <input
              type="text"
              id="akademischerGrad"
              v-model="hochschulabschluss.akademischerGrad"
              placeholder="Akademischer Grad eingeben"
            />
          </div>
  
          <div class="form-group">
            <label for="abschlussjahr">Abschlussjahr</label>
            <input
              type="text"
              id="abschlussjahr"
              v-model="hochschulabschluss.abschlussjahr"
              placeholder="Abschlussjahr eingeben"
            />
          </div>
  
          <div class="form-group">
            <label for="fachgebiet">Fachgebiet</label>
            <input
              type="text"
              id="fachgebiet"
              v-model="hochschulabschluss.fachgebiet"
              placeholder="Fachgebiet eingeben"
            />
          </div>
        </form>
      </div>
  
      <!-- Berufserfahrung -->
      <div class="weiterfuehrende-daten-container">
        <h2>Berufserfahrung</h2>
        <table>
          <thead>
            <tr>
              <th>Von</th>
              <th>Bis</th>
              <th>Firma</th>
              <th>Funktion</th>
              <th>Fachgebiet</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(row, index) in berufserfahrung" :key="index">
              <td><input type="date" v-model="row.von" /></td>
              <td><input type="date" v-model="row.bis" /></td>
              <td><input type="text" v-model="row.firma" placeholder="Firma eingeben" /></td>
              <td><input type="text" v-model="row.funktion" placeholder="Funktion eingeben" /></td>
              <td><input type="text" v-model="row.fachgebiet" placeholder="Fachgebiet eingeben" /></td>
            </tr>
          </tbody>
        </table>
        <button class="button-add" @click="addRow">Weitere hinzufügen</button>
      </div>
  
      <!-- Datum und Unterschrift -->
      <div class="weiterfuehrende-daten-container">
        <h2>Datum und Unterschrift</h2>
        <form>
          <div class="form-group">
            <label for="datum">Datum</label>
            <input type="date" id="datum" v-model="datumUndUnterschrift.datum" />
          </div>
  
          <div class="form-group">
            <label for="unterschrift">Unterschrift hochladen</label>
            <input
              type="file"
              id="unterschrift"
              @change="handleUnterschriftUpload"
              accept=".png,.jpg"
            />
          </div>
        </form>
      </div>
  
      <!-- Abschlussdokument -->
      <div class="weiterfuehrende-daten-container">
        <h2>Abschlussdokument</h2>
        <form>
          <div class="form-group">
            <label for="abschlussDokument">Abschlussdokument hochladen</label>
            <input
              type="file"
              id="abschlussDokument"
              @change="handleFileUpload"
              accept=".pdf,.png,.jpg"
            />
          </div>
        </form>
      </div>
  
      <!-- Buttons -->
      <div class="button-group">
        <button type="button" class="button-main" @click="goBack">Zurück</button>
        <button type="button" class="button-main" @click="previewPDF">Vorschau</button>
        <button type="submit" class="button-main" @click="handleSubmit">Speichern</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        autoFillGrunddaten: false,
        studierendeDaten: {
          vorname: '',
          name: '',
          matrikelnummer: '',
          studiengang: '',
        },
        zweitprueferDaten: { name: '', email: '', telefon: '' },
        hochschulabschluss: {
          hochschule: '',
          akademischerGrad: '',
          abschlussjahr: '',
          fachgebiet: '',
        },
        berufserfahrung: [
          { von: '', bis: '', firma: '', funktion: '', fachgebiet: '' },
        ],
        datumUndUnterschrift: { datum: '', unterschrift: null },
      };
    },
    methods: {
      addRow() {
        this.berufserfahrung.push({
          von: '',
          bis: '',
          firma: '',
          funktion: '',
          fachgebiet: '',
        });
      },
      handleFileUpload(event) {
        this.hochschulabschluss.abschlussDokument = event.target.files[0];
      },
      handleUnterschriftUpload(event) {
        this.datumUndUnterschrift.unterschrift = event.target.files[0];
      },
      goBack() {
        this.$router.push({ name: 'form-selector' });
      },
      previewPDF() {
        console.log('PDF Vorschau');
      },
      handleSubmit() {
        console.log('Formular speichern');
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
  input[type='date'],
  input[type='file'],
  select {
    width: 100%;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  .button-group {
    display: flex;
    justify-content: space-between;
    margin-top: 20px;
  }
  
  button {
    padding: 10px 20px;
    font-size: 16px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .button-main {
    background-color: #80ba24;
    color: white;
  }
  
  .button-main:hover {
    background-color: #6ca61c;
  }
  
  .button-add {
    background-color: #80ba24;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .button-add:hover {
    background-color: #6ca61c;
  }
  </style>