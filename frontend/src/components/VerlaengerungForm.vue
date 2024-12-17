<template> 
    <div class="form-container">
      <h1>Antrag auf Verlängerung der Bachelor-/Masterarbeit</h1>
  
      <!-- Grunddaten Container mit Toggle -->
      <div class="grunddaten-container">
        <div class="form-group">
          <label>
            <input type="checkbox" v-model="autoFillGrunddaten" /> Automatisch ausfüllen
          </label>
        </div>
  
        <form>
          <div class="form-group" :class="{'error': !formData.studiengang && formSubmitted}">
            <label>Studiengang</label>
            <div class="spacing"></div>
            <div>
              <div>
                <input type="radio" id="bachelor" value="Bachelor" v-model="formData.studiengang" />
                <label for="bachelor">Bachelor</label>
              </div>
              <div>
                <input type="radio" id="master" value="Master" v-model="formData.studiengang" />
                <label for="master">Master</label>
              </div>
            </div>
            <span v-if="!formData.studiengang && formSubmitted" class="error-message">Dieses Feld ist erforderlich</span>
          </div>
  
          <div class="form-group" :class="{'error': !formData.frauHerr && formSubmitted}">
            <label for="frauHerr">Frau / Herrn</label>
            <input
              type="text"
              id="frauHerr"
              v-model="formData.frauHerr"
              :disabled="autoFillGrunddaten"
              placeholder="Frau / Herrn eingeben"
            />
            <span v-if="!formData.frauHerr && formSubmitted" class="error-message">Dieses Feld ist erforderlich</span>
          </div>
  
          <div class="form-group" :class="{'error': !formData.thema && formSubmitted}">
            <label for="thema">Thema</label>
            <input
              type="text"
              id="thema"
              v-model="formData.thema"
              :disabled="autoFillGrunddaten"
              placeholder="Thema eingeben"
            />
            <span v-if="!formData.thema && formSubmitted" class="error-message">Dieses Feld ist erforderlich</span>
          </div>
  
          <div class="form-group" :class="{'error': !formData.firma && formSubmitted}">
            <label for="firma">Firma</label>
            <input
              type="text"
              id="firma"
              v-model="formData.firma"
              :disabled="autoFillGrunddaten"
              placeholder="Firma eingeben"
            />
            <span v-if="!formData.firma && formSubmitted" class="error-message">Dieses Feld ist erforderlich</span>
          </div>
  
          <div class="form-group" :class="{'error': !formData.grund && formSubmitted}">
            <label for="grund">Grund</label>
            <textarea
              id="grund"
              v-model="formData.grund"
              :disabled="autoFillGrunddaten"
              placeholder="Grund eingeben"
              rows="10"
            ></textarea>
            <span v-if="!formData.grund && formSubmitted" class="error-message">Dieses Feld ist erforderlich</span>
          </div>
  
          <div class="form-group">
            <label for="optionalDocument">Optionales Dokument hochladen</label>
            <input
              type="file"
              id="optionalDocument"
              @change="uploadOptionalDocument"
              accept="application/pdf, image/png, image/jpeg"
            />
          </div>
  
          <div class="form-group" :class="{'error': !formData.signature && formSubmitted}">
            <label for="signature">Unterschrift hochladen</label>
            <input
              type="file"
              id="signature"
              @change="uploadSignature"
              accept="image/png, image/jpeg"
            />
            <span v-if="!formData.signature && formSubmitted" class="error-message">Dieses Feld ist erforderlich</span>
          </div>
        </form>
      </div>
  
    <!-- Container für Entscheidung des Referenten -->
  <div class="referent-container">
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="referentName">Referent*in</label>
        <input
          type="text"
          id="referentName"
          v-model="formData.referentName"
          placeholder="Name der Referent*in eingeben"
        />
      </div>
  
      <div class="form-group">
        <label>Stellungnahme/ Befürwortung durch den/die 1.Referent*in:</label>
        <textarea
          id="referentStellungnahme"
          v-model="formData.referentStellungnahme"
          placeholder="Hier Stellungnahme des Referenten eingeben"
          rows="8"
        ></textarea>
      </div>
  
      <div class="form-group">
        <label for="referentSignature">Unterschrift hochladen</label>
        <input
          type="file"
          id="referentSignature"
          @change="uploadReferentSignature"
          accept="image/png, image/jpeg"
        />
      </div>
    </form>
  </div>
  
  
      <!-- Container für Entscheidung des Prüfungsausschusses -->
      <div class="ausschuss-container">
        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <label>Entscheidung des Prüfungsausschusses</label>
            <div class="spacing"></div>
            <div>
              <div>
                <input type="radio" id="ausschussZugelassen" value="zugelassen" v-model="formData.ausschussEntscheidung" />
                <label for="ausschussZugelassen">Antrag zulassen</label>
              </div>
              <div>
                <input type="radio" id="ausschussNichtZugelassen" value="nicht zugelassen" v-model="formData.ausschussEntscheidung" />
                <label for="ausschussNichtZugelassen">Antrag nicht zulassen</label>
              </div>
            </div>
          </div>
  
          <div class="form-group">
            <label for="ausschussName">Ausschussvorsitzende(r)</label>
            <input
              type="text"
              id="ausschussName"
              v-model="formData.ausschussName"
              placeholder="Name des Vorsitzenden eingeben"
            />
          </div>
  
          <div class="form-group">
            <label for="ausschussBegruendung">Begründung</label>
            <textarea
              id="ausschussBegruendung"
              v-model="formData.ausschussBegruendung"
              placeholder="Begründung eingeben"
              rows="3"
            ></textarea>
          </div>
  
  
          <div class="form-group">
            <label for="ausschussSignature">Unterschrift hochladen</label>
            <input
              type="file"
              id="ausschussSignature"
              @change="uploadAusschussSignature"
              accept="image/png, image/jpeg"
            />
          </div>
        </form>
      </div>
  
      <!-- Button-Gruppe für Zurück, Vorschau und Speichern -->
      <div class="button-group">
        <button type="button" @click="goBack" class="btn-green">Zurück</button>
        <button type="button" @click="previewPdf" class="btn-green">Vorschau</button>
        <button type="submit" class="btn-green">Speichern</button>
      </div>
  
      <!-- PDF Vorschau -->
      <div v-if="pdfPreview" class="pdf-preview">
        <iframe :src="pdfPreview" width="100%" height="600px"></iframe>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        formData: {
          studiengang: '',
          frauHerr: '',
          thema: '',
          firma: '',
          grund: '',
          datum: '',
          signature: null,
          referentStellungnahme: '',
          referentDatum: '',
          referentSignature: null,
          ausschussEntscheidung: '',
          ausschussName: '',
          ausschussBegruendung: '',
          ausschussDatum: '',
          ausschussSignature: null,
        },
        autoFillGrunddaten: false,
        formSubmitted: false,
        pdfPreview: null,
      };
    },
    methods: {
      uploadSignature(event) {
        this.formData.signature = event.target.files[0];
        console.log("Unterschrift hochgeladen:", this.formData.signature);
      },
      uploadReferentSignature(event) {
        this.formData.referentSignature = event.target.files[0];
        console.log("Referenten-Unterschrift hochgeladen:", this.formData.referentSignature);
      },
      uploadAusschussSignature(event) {
        this.formData.ausschussSignature = event.target.files[0];
        console.log("Unterschrift des Ausschusses hochgeladen:", this.formData.ausschussSignature);
      },
      previewPdf() {
        this.formSubmitted = true; // Trigger validation
        if (this.validateForm()) {
          const formData = new FormData();
          Object.keys(this.formData).forEach((key) => {
            formData.append(key, this.formData[key]);
          });
  
          fetch("http://127.0.0.1:8000/preview-verlaengerung-pdf", {
            method: "POST",
            body: formData,
          })
            .then((response) => response.blob())
            .then((blob) => {
              this.pdfPreview = URL.createObjectURL(blob);
            })
            .catch((error) => {
              console.error("Fehler bei der Vorschau:", error);
            });
        }
      },
      generatePdf() {
        this.formSubmitted = true; // Trigger validation
        if (this.validateForm()) {
          const formData = new FormData();
          Object.keys(this.formData).forEach((key) => {
            formData.append(key, this.formData[key]);
          });
  
          fetch("http://127.0.0.1:8000/generate-verlaengerung-pdf", {
            method: "POST",
            body: formData,
          })
            .then((response) => response.blob())
            .then((blob) => {
              const url = window.URL.createObjectURL(blob);
              const link = document.createElement("a");
              link.href = url;
              link.setAttribute("download", "verlaengerung_bachelorarbeit.pdf");
              document.body.appendChild(link);
              link.click();
              document.body.removeChild(link);
            })
            .catch((error) => {
              console.error("Fehler beim Erstellen der PDF:", error);
            });
        }
      },
      validateForm() {
        return (
          this.formData.frauHerr &&
          this.formData.thema &&
          this.formData.firma &&
          this.formData.grund &&
          this.formData.datum &&
          this.formData.signature
        );
      },
      goBack() {
        console.log("Zurück zur vorherigen Seite.");
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
  .referent-container,
  .ausschuss-container {
    margin-top: 20px;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 8px;
    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  .spacing {
    height: 10px;
  }
  
  label {
    font-weight: bold;
    margin-bottom: 5px;
  }
  
  input[type="text"],
  input[type="file"],
  input[type="date"],
  textarea {
    width: 100%;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  textarea {
    resize: none;
  }
  
  .button-group {
    display: flex;
    justify-content: space-between;
    margin-top: 20px;
  }
  
  .btn-green {
    padding: 10px 20px;
    background-color: #80ba24;
    color: white;
    font-size: 16px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .btn-green:hover {
    background-color: #4a5c66;
  }
  
  .pdf-preview {
    margin-top: 20px;
  }
  
  .error {
    border: 1px solid red;
  }
  
  .error-message {
    color: red;
    font-size: 12px;
  }
  </style>