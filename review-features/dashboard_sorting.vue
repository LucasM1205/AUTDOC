<template>
    <div class="dashboard">
      <header class="dashboard-header">
        <h1>Willkommen, {{ user.name }}!</h1>
        <p>Rolle: {{ user.role }}</p>
        <button class="logout-button" @click="logout">Abmelden</button>
      </header>
  
      <!-- Bearbeiten-Komponente für Sekretariat -->
      <antrag-bearbeiten
        v-if="selectedAntrag && user.role === 'Sekretariat'"
        :antrag="selectedAntrag"
        @update-success="handleUpdateSuccess"
        @cancel-edit="handleCancelEdit"
      ></antrag-bearbeiten>
  
      <!-- Bearbeiten-Komponente für Prüfungsausschuss -->
      <antrag-bearbeiten-ausschuss
        v-if="selectedAntrag && user.role === 'Prüfungsausschuss'"
        :antrag="selectedAntrag"
        @update-success="handleUpdateSuccess"
        @cancel-edit="handleCancelEdit"
      ></antrag-bearbeiten-ausschuss>
  
      <!-- Antragsliste wird nur angezeigt, wenn kein Antrag bearbeitet wird -->
      <div v-else-if="antraege.length">
        <h2>Deine Anträge:</h2>
  
        <!-- Sortieroptionen -->
        <div class="sort-options">
          <label for="sort-by">Sortieren nach:</label>
          <select id="sort-by" v-model="sortCriteria" @change="sortAntraege">
            <option value="status">Status</option>
            <option value="date-asc">Erstellungsdatum (alt → neu)</option>
            <option value="date-desc">Erstellungsdatum (neu → alt)</option>
          </select>
        </div>
  
        <!-- Gruppierung der Anträge nach Status -->
        <div class="status-group">
          <!-- Offene Anträge -->
          <h3>Offene Anträge</h3>
          <ul class="antrags-liste" v-if="filteredAntraege.offen.length">
            <li v-for="antrag in filteredAntraege.offen" :key="antrag.antrag_id">
              <div class="antrag">
                <h3>Antrag (ID: {{ antrag.antrag_id }}): {{ antrag.fach || "Unbekanntes Fach" }}</h3>
                <p :class="statusClass(antrag.status)">Status: {{ antrag.status }}</p>
                <p>Erstellt am: {{ formatDate(antrag.datum_erstellung) }}</p>
                <div class="button-group">
                  <button @click="toggleDetails(antrag.antrag_id)">
                    {{ expandedAntragId === antrag.antrag_id ? "Details ausblenden" : "Details anzeigen" }}
                  </button>
                </div>
                <div v-if="expandedAntragId === antrag.antrag_id" class="details">
                  <!-- Details anzeigen -->
                  <p><strong>Bemerkungen:</strong> {{ antrag.bemerkungen || "Keine Bemerkungen" }}</p>
                </div>
              </div>
            </li>
          </ul>
          <p v-else>Keine offenen Anträge.</p>
  
          <!-- Abgeschlossene Anträge -->
          <h3>Abgeschlossene Anträge</h3>
          <ul class="antrags-liste" v-if="filteredAntraege.abgeschlossen.length">
            <li v-for="antrag in filteredAntraege.abgeschlossen" :key="antrag.antrag_id">
              <div class="antrag">
                <h3>Antrag (ID: {{ antrag.antrag_id }}): {{ antrag.fach || "Unbekanntes Fach" }}</h3>
                <p :class="statusClass(antrag.status)">Status: {{ antrag.status }}</p>
                <p>Erstellt am: {{ formatDate(antrag.datum_erstellung) }}</p>
                <div class="button-group">
                  <button @click="toggleDetails(antrag.antrag_id)">
                    {{ expandedAntragId === antrag.antrag_id ? "Details ausblenden" : "Details anzeigen" }}
                  </button>
                </div>
                <div v-if="expandedAntragId === antrag.antrag_id" class="details">
                  <!-- Details anzeigen -->
                  <p><strong>Bemerkungen:</strong> {{ antrag.bemerkungen || "Keine Bemerkungen" }}</p>
                </div>
              </div>
            </li>
          </ul>
          <p v-else>Keine abgeschlossenen Anträge.</p>
  
          <!-- Abgelehnte Anträge -->
          <h3>Abgelehnte Anträge</h3>
          <ul class="antrags-liste" v-if="filteredAntraege.abgelehnt.length">
            <li v-for="antrag in filteredAntraege.abgelehnt" :key="antrag.antrag_id">
              <div class="antrag">
                <h3>Antrag (ID: {{ antrag.antrag_id }}): {{ antrag.fach || "Unbekanntes Fach" }}</h3>
                <p :class="statusClass(antrag.status)">Status: {{ antrag.status }}</p>
                <p>Erstellt am: {{ formatDate(antrag.datum_erstellung) }}</p>
                <div class="button-group">
                  <button @click="toggleDetails(antrag.antrag_id)">
                    {{ expandedAntragId === antrag.antrag_id ? "Details ausblenden" : "Details anzeigen" }}
                  </button>
                </div>
                <div v-if="expandedAntragId === antrag.antrag_id" class="details">
                  <!-- Details anzeigen -->
                  <p><strong>Bemerkungen:</strong> {{ antrag.bemerkungen || "Keine Bemerkungen" }}</p>
                </div>
              </div>
            </li>
          </ul>
          <p v-else>Keine abgelehnten Anträge.</p>
        </div>
      </div>
      <p v-else>Du hast noch keine Anträge.</p>
  
      <footer>
        <button @click="ladeAntraege">Aktualisieren</button>
      </footer>
    </div>
  </template>
  
  <script>
  import AntragBearbeiten from "./AntragBearbeiten.vue"; // Komponente für Sekretariat
  import AntragBearbeitenAusschuss from "./AntragBearbeitenAusschuss.vue"; // Neue Komponente für Prüfungsausschuss
  
  export default {
    components: {
      AntragBearbeiten,
      AntragBearbeitenAusschuss,
    },
    data() {
      return {
        user: {
          name: "Benutzer",
          role: "Student", // Standardwert
        },
        antraege: [], // Liste der Anträge
        expandedAntragId: null, // Aktuell geöffneter Antrag für Details
        selectedAntrag: null, // Aktuell ausgewählter Antrag zum Bearbeiten
        sortCriteria: "status", // Standardkriterium für die Sortierung
        filteredAntraege: {
          offen: [],
          abgeschlossen: [],
          abgelehnt: [],
        }, // Gruppierte Anträge
      };
    },
    async created() {
      try {
        await this.ladeBenutzerDaten();
        await this.ladeAntraege();
      } catch (error) {
        console.error("Fehler beim Initialisieren:", error);
      }
    },
    methods: {
      async ladeBenutzerDaten() {
        try {
          const token = localStorage.getItem("access_token");
          if (!token) {
            this.$router.push({ name: "login" });
            return;
          }
  
          const response = await fetch("http://127.0.0.1:8000/api/me", {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
  
          if (!response.ok) {
            const errorText = await response.text();
            console.error("DEBUG: Fehlertext beim Abrufen der Benutzerdaten:", errorText);
            throw new Error("Fehler beim Laden der Benutzerdaten");
          }
  
          this.user = await response.json();
          console.log("DEBUG: Benutzerdaten geladen:", this.user);
        } catch (error) {
          console.error("Fehler beim Laden der Benutzerdaten:", error);
          alert("Fehler beim Laden der Benutzerdaten. Bitte erneut anmelden.");
          this.$router.push({ name: "login" });
        }
      },
      async ladeAntraege() {
        try {
          const token = localStorage.getItem("access_token");
          let endpoint;
  
          // Dynamischen Endpunkt basierend auf der Benutzerrolle setzen
          if (this.user.role === "Sekretariat") {
            endpoint = "http://127.0.0.1:8000/api/antraege/sekretariat";
          } else if (this.user.role === "Student") {
            endpoint = "http://127.0.0.1:8000/api/antraege/student";
          } else if (this.user.role === "Prüfungsausschuss") {
            endpoint = "http://127.0.0.1:8000/api/antraege/pruefungsausschuss";
          } else {
            throw new Error("Unbekannte Rolle");
          }
  
          console.log(`DEBUG: API-Endpunkt für Anträge: ${endpoint}`);
  
          const response = await fetch(endpoint, {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });
  
          if (!response.ok) {
            const errorText = await response.text();
            console.error("DEBUG: Fehlertext beim Abrufen der Anträge:", errorText);
            throw new Error("Fehler beim Laden der Anträge");
          }
  
          this.antraege = await response.json();
          this.sortAndGroupAntraege(); // Gruppiere und sortiere die Anträge
          console.log("DEBUG: Anträge geladen:", this.antraege);
        } catch (error) {
          console.error("Fehler beim Laden der Anträge:", error);
          alert("Fehler beim Abrufen der Anträge.");
        }
      },
      toggleDetails(antragId) {
        this.expandedAntragId = this.expandedAntragId === antragId ? null : antragId;
      },
      bearbeiteAntrag(antrag) {
        this.selectedAntrag = antrag;
      },
      formatDate(dateString) {
        if (!dateString) return "Nicht angegeben";
        const date = new Date(dateString);
        return date.toLocaleDateString("de-DE");
      },
      handleUpdateSuccess() {
        this.selectedAntrag = null;
        this.ladeAntraege();
      },
      handleCancelEdit() {
        this.selectedAntrag = null;
      },
      logout() {
        localStorage.removeItem("access_token");
        this.$router.push({ name: "login" });
      },
      /**
       * Gibt die CSS-Klasse basierend auf dem Status des Antrags zurück.
       * @param {string} status - Der Status des Antrags.
       * @returns {string} - Die CSS-Klasse für den Status.
       */
      statusClass(status) {
        switch (status) {
          case "Ausstehend":
          case "Antrag durch Sekretariat genehmigt; Rückmeldung durch Prüfungsausschuss ausstehend":
            return "status-yellow";
          case "Antrag genehmigt durch Prüfungsausschuss":
            return "status-green";
          case "Antrag abgelehnt durch Prüfungsausschuss":
          case "Antrag durch Sekretariat abgelehnt":
            return "status-red";
          default:
            return ""; // Fallback, falls der Status unbekannt ist
        }
      },
      /**
       * Gruppiert und sortiert die Anträge nach Status und Sortierkriterium.
       */
      sortAndGroupAntraege() {
        // Gruppierung der Anträge
        this.filteredAntraege.offen = this.antraege.filter((antrag) =>
          ["Ausstehend", "Antrag durch Sekretariat genehmigt; Rückmeldung durch Prüfungsausschuss ausstehend"].includes(
            antrag.status
          )
        );
        this.filteredAntraege.abgeschlossen = this.antraege.filter(
          (antrag) => antrag.status === "Antrag genehmigt durch Prüfungsausschuss"
        );
        this.filteredAntraege.abgelehnt = this.antraege.filter((antrag) =>
          ["Antrag abgelehnt durch Prüfungsausschuss", "Antrag durch Sekretariat abgelehnt"].includes(antrag.status)
        );
  
        // Sortierung der Gruppen basierend auf dem Sortierkriterium
        const sortByDate = (a, b) =>
          this.sortCriteria === "date-asc"
            ? new Date(a.datum_erstellung) - new Date(b.datum_erstellung)
            : new Date(b.datum_erstellung) - new Date(a.datum_erstellung);
  
        this.filteredAntraege.offen.sort(sortByDate);
        this.filteredAntraege.abgeschlossen.sort(sortByDate);
        this.filteredAntraege.abgelehnt.sort(sortByDate);
      },
    },
  };
  </script>
  
  
  <style scoped>
  .dashboard {
    max-width: 800px;
    margin: auto;
    padding: 20px;
  }
  
  .dashboard-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
  }
  
  .antrags-liste {
    list-style-type: none;
    padding: 0;
  }
  
  .antrag {
    padding: 10px;
    border: 1px solid #ccc;
    margin: 10px 0;
    border-radius: 5px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  }
  
  .antrag h3 {
    margin: 0 0 5px;
  }
  
  .antrag p {
    margin: 0 0 10px;
  }
  
  .button-group {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  button {
    padding: 8px 12px;
    background-color: var(--primary-color);
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: var(--secondary-color);
  }
  
  .bearbeiten-button {
    margin-left: auto; /* Schiebt den Bearbeiten-Button nach rechts */
  }
  
  .details-container {
    margin-top: 10px;
    padding: 10px;
    border-top: 1px solid #ccc;
    background-color: #f9f9f9;
  }
  
  .details-container p {
    margin: 5px 0;
  }
  
  .logout-button {
    background-color: red;
  }
  
  .logout-button:hover {
    background-color: darkred;
  }
  
  /* Neue Klassen für Statusfarben */
  .status-yellow {
    color: #F4AA01; /* Gelb */
    font-weight: bold;
  }
  
  .status-green {
    color: #80ba24; /* Grün */
    font-weight: bold;
  }
  
  .status-red {
    color: #9E1B32; /* Rot */
    font-weight: bold;
  }
  </style>
  
  