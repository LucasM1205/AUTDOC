<template>
  <div class="main-container" :class="{ 'preview-active': showPreview }">
    <div class="form-section">
      <h1>Antrag - Joker</h1>

      <!-- Grunddaten Container mit Toggle -->
      <div class="grunddaten-container">
        <div class="form-group">
          <label>
            <input
              type="checkbox"
              v-model="autoFillGrunddaten"
              @change="handleAutoFillGrunddaten"
            />
            Automatisch ausfüllen
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
            <input
              type="text"
              id="fach"
              v-model="weiterfuehrendeDaten.fach"
              placeholder="Fach eingeben"
            />
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
          <!-- Ergänztes Feld: Fachbereich des Moduls -->
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
          <div v-if="weiterfuehrendeDaten.jokerStatus === 'doppelstudium'" class="form-group">
            <label for="doppelstudiumBachelor">Bachelorstudiengang</label>
            <input
              type="text"
              id="doppelstudiumBachelor"
              v-model="weiterfuehrendeDaten.doppelstudiumBachelor"
              placeholder="Bachelorstudiengang eingeben"
            />
          </div>
          <div class="button-group">
            <button type="button" @click="goBack">Zurück</button>
            <button type="button" @click="previewPDF">Vorschau</button>
            <button type="submit">Speichern</button>
          </div>
        </form>
      </div>

      <!-- Vorschau-Modal -->
      <!-- Statt modal -->
      <div v-if="showPreview" class="pdf-container">
        <button @click="closePreview" class="close-button">Schließen</button>
        <iframe :src="previewUrl" width="100%" height="calc(100% - 50px)"></iframe>
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
        vorname: "",
        nachname: "",
        matrikelnummer: "",
        fachbereich: "",
        bachelorstudiengang: "",
        unterschrift: null,
      },
      weiterfuehrendeDaten: {
        fach: "",
        pruefungsnummer: "",
        pruefer: "",
        fachbereichModul: "",
        jokerStatus: "",
        doppelstudiumBachelor: "",
      },
    };
  },
  methods: {
    handleFileUpload(event) {
      this.grunddaten.unterschrift = event.target.files[0];
    },
    async handleAutoFillGrunddaten() {
      if (this.autoFillGrunddaten) {
        try {
          const token = localStorage.getItem("access_token");
          if (!token) {
            alert("Kein Token gefunden. Bitte erneut anmelden.");
            this.$router.push({ name: "login" });
            return;
          }

          // Daten vom Backend abrufen
          const response = await fetch("http://127.0.0.1:8000/api/grunddaten", {
            method: "GET",
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });

          if (!response.ok) {
            throw new Error("Fehler beim Abrufen der Benutzerinformationen");
          }

          const data = await response.json();
          console.log("Benutzerinformationen:", data);

          // Felder automatisch ausfüllen
          this.grunddaten.vorname = data.vorname || "";
          this.grunddaten.nachname = data.nachname || "";
          this.grunddaten.matrikelnummer = data.matrikelnummer || "Unbekannt";
          this.grunddaten.fachbereich = data.fachbereich || "Unbekannt";
          this.grunddaten.bachelorstudiengang = data.studiengang || "Unbekannt";
        } catch (error) {
          console.error("Fehler beim automatischen Ausfüllen:", error);
          alert("Fehler beim automatischen Ausfüllen der Grunddaten.");
        }
      } else {
        // Felder zurücksetzen, falls Checkbox deaktiviert wird
        this.grunddaten.vorname = "";
        this.grunddaten.nachname = "";
        this.grunddaten.matrikelnummer = "";
        this.grunddaten.fachbereich = "";
        this.grunddaten.bachelorstudiengang = "";
      }
    },
    async previewPDF() {
      try {
        const formData = new FormData();
        // Fügen Sie Grunddaten hinzu
        Object.entries(this.grunddaten).forEach(([key, value]) =>
          formData.append(key, value || "")
        );

        // Weiterführende Daten in snake_case hinzufügen
        const snakeCaseFields = {
          fach: this.weiterfuehrendeDaten.fach,
          pruefungsnummer: this.weiterfuehrendeDaten.pruefungsnummer,
          pruefer: this.weiterfuehrendeDaten.pruefer,
          fachbereich_modul: this.weiterfuehrendeDaten.fachbereichModul,
          joker_status: this.weiterfuehrendeDaten.jokerStatus,
          doppelstudium_bachelor: this.weiterfuehrendeDaten.doppelstudiumBachelor,
        };

        Object.entries(snakeCaseFields).forEach(([key, value]) =>
          formData.append(key, value || "")
        );

        // Unterschrift hinzufügen, falls vorhanden
        if (this.grunddaten.unterschrift) {
          formData.append("unterschrift", this.grunddaten.unterschrift);
        }

        // Vorschau-PDF anfordern
        const response = await fetch("http://127.0.0.1:8000/preview-pdf", {
          method: "POST",
          body: formData,
        });

        if (!response.ok) {
          const errorDetails = await response.json();
          console.error("Fehlerdetails bei Vorschau:", errorDetails);
          throw new Error("Fehler bei der Vorschau");
        }

        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        this.previewUrl = url;
        this.showPreview = true;
      } catch (error) {
        console.error("Fehler bei der Vorschau:", error);
        alert("Fehler bei der Vorschau.");
      }
    },
    closePreview() {
      this.showPreview = false;
      this.previewUrl = "";
    },
    async handleSubmit() {
      try {
        const token = localStorage.getItem("access_token");
        if (!token) {
          alert("Kein Token gefunden. Bitte erneut anmelden.");
          this.$router.push({ name: "login" });
          return;
        }

        const formData = new FormData();
        // Fügen Sie Grunddaten hinzu
        Object.entries(this.grunddaten).forEach(([key, value]) =>
          formData.append(key, value || "")
        );

        // Weiterführende Daten in snake_case hinzufügen
        const snakeCaseFields = {
          fach: this.weiterfuehrendeDaten.fach,
          pruefungsnummer: this.weiterfuehrendeDaten.pruefungsnummer,
          pruefer: this.weiterfuehrendeDaten.pruefer,
          fachbereich_modul: this.weiterfuehrendeDaten.fachbereichModul,
          joker_status: this.weiterfuehrendeDaten.jokerStatus,
          doppelstudium_bachelor: this.weiterfuehrendeDaten.doppelstudiumBachelor,
        };

        Object.entries(snakeCaseFields).forEach(([key, value]) =>
          formData.append(key, value || "")
        );

        // Unterschrift hinzufügen, falls vorhanden
        if (this.grunddaten.unterschrift) {
          formData.append("unterschrift", this.grunddaten.unterschrift);
        }

        const response = await fetch("http://127.0.0.1:8000/generate-pdf", {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
          },
          body: formData,
        });

        if (!response.ok) {
          const errorDetails = await response.json();
          if (errorDetails.detail && Array.isArray(errorDetails.detail)) {
            const errorMessages = errorDetails.detail
              .map((err) => `Feld: ${err.loc.join(" -> ")}, Fehler: ${err.msg}`)
              .join("\n");
            throw new Error(`Fehler beim Speichern:\n${errorMessages}`);
          } else {
            throw new Error("Unbekannter Fehler beim Speichern.");
          }
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);

        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", "joker_antrag_ausgefuellt.pdf");
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        alert("Antrag erfolgreich erstellt!");
        this.$router.push({ name: "dashboard" });
      } catch (error) {
        console.error("Fehler:", error.message);
        alert(`Fehler: ${error.message}`);
      }
    },
    goBack() {
      this.$router.push({ name: "form-selector" });
    },
    checkDoppelstudium() {
      if (this.weiterfuehrendeDaten.jokerStatus !== "doppelstudium") {
        this.weiterfuehrendeDaten.doppelstudiumBachelor = "";
      }
    },
  },
  async created() {
    await this.fetchCurrentUser();
  },
};
</script>


<style scoped>

.main-container {
  display: flex;
  width: 100%;
  padding: 40px;
  gap: 60px;

}

.form-section {
  width: 800px;
  margin-left: 2000px;
}

.form-container {
  max-width: 800px;
  margin: auto;
  padding: 20px;
}

.pdf-container {
  width: 1000px; /* Etwas schmaler für bessere Proportion */
  height: 800px; /* Feste Höhe bis zur mittleren Markierung */
  margin-right: 40px;
  margin-top: 100px; /* Abstand zur oberen Markierung */
  background-color: #fff;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.pdf-container iframe {
  width: 100%;
  height: 100%;
  border: none;
}

.preview-modal {
  display: none;
}

/* Anpassungen für den aktiven Vorschau-Zustand */
.preview-active .form-section {
  margin-left: 20px;
}


h1 {
  text-align: center;
  color: #80ba24;
}

.preview-active .pdf-container {
  right: 0;
}

.grunddaten-container,
.weiterfuehrende-daten-container {
  margin-bottom: 20px;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  background-color: #fff;
}

.form-group {
  margin-bottom: 15px;
}

input[type='text'],
select,
input[type='file'] {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
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
  margin-top: 20px;
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

.pdf-container {
  flex: 0 0 45%;
  height: calc(100vh - 40px);
  position: fixed;
  right: 20px;
  top: 20px;
  background-color: white;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
  overflow: auto;
}

.form-section {
  width: 800px;
  margin: auto;
  transition: transform 0.3s ease;
}

iframe {
  border: none;
}
</style>