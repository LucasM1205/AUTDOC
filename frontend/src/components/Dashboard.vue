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
      <ul class="antrags-liste">
        <li v-for="antrag in antraege" :key="antrag.antrag_id">
          <div class="antrag">
            <h3>Antrag (ID: {{ antrag.antrag_id }}): {{ antrag.fach || "Unbekanntes Fach" }}</h3>
            <p>Status: {{ antrag.status }}</p>
            <p>Erstellt am: {{ formatDate(antrag.datum_erstellung) }}</p>

            <!-- Button-Gruppe mit Ein-/Ausklappen -->
            <div class="button-group">
              <button @click="toggleDetails(antrag.antrag_id)">
                {{ expandedAntragId === antrag.antrag_id ? "Details ausblenden" : "Details anzeigen" }}
              </button>
              <button
                v-if="user.role === 'Sekretariat'"
                @click="bearbeiteAntrag(antrag)"
                class="bearbeiten-button"
              >
                Bearbeiten
              </button>
              <button
                v-if="user.role === 'Prüfungsausschuss'"
                @click="bearbeiteAntrag(antrag)"
                class="bearbeiten-button"
              >
                Bearbeiten
              </button>
            </div>

            <!-- Erweiterte Details -->
            <div v-if="expandedAntragId === antrag.antrag_id" class="details">
              <p><strong>Prüfungsnummer:</strong> {{ antrag.pruefungsnummer || "Nicht angegeben" }}</p>
              <p><strong>Prüfer:</strong> {{ antrag.pruefer || "Nicht angegeben" }}</p>
              <p><strong>Bemerkungen:</strong> {{ antrag.bemerkungen || "Keine Bemerkungen" }}</p>
              <p><strong>Joker verwendet:</strong> {{ antrag.joker_verwendet ? "Ja" : "Nein" }}</p>
              <p><strong>Doppelstudium:</strong> {{ antrag.doppelstudium ? "Ja" : "Nein" }}</p>
              <p><strong>Letzte Änderung:</strong> {{ formatDate(antrag.letzte_aenderung) || "Keine Änderungen" }}</p>
              <p><strong>Name des Studierenden:</strong> {{ antrag.student_name || "Nicht angegeben" }}</p>
              <p><strong>Vorname des Studierenden:</strong> {{ antrag.student_vorname || "Nicht angegeben" }}</p>
              <p><strong>Matrikelnummer:</strong> {{ antrag.student_matrikelnummer || "Nicht angegeben" }}</p>
              <p><strong>Studiengang:</strong> {{ antrag.student_studiengang || "Nicht angegeben" }}</p>
            </div>
          </div>
        </li>
      </ul>
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
</style>
