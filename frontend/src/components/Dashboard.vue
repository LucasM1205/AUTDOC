<template>
  <div class="dashboard">
    <header class="dashboard-header">
      <h1>Willkommen, {{ user.name }}!</h1>
      <p>Rolle: {{ user.role }}</p>
      <button class="logout-button" @click="logout">Abmelden</button>
    </header>

    <div v-if="antraege.length">
      <h2>Deine Anträge:</h2>
      <ul class="antrags-liste">
        <li v-for="antrag in antraege" :key="antrag.id">
          <div class="antrag">
            <h3>Antrag: {{ antrag.fach }}</h3>
            <p>Status: {{ antrag.status }}</p>
            <p>Erstellt am: {{ formatDate(antrag.datum_erstellung) }}</p>
            <button @click="zeigeDetails(antrag)">Details ansehen</button>
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
export default {
  data() {
    return {
      user: {
        name: "Benutzer",
        role: "Student",
      },
      antraege: [], // Liste der Anträge
    };
  },
  async created() {
    await this.ladeBenutzerDaten();
    await this.ladeAntraege();
  },
  methods: {
    async ladeBenutzerDaten() {
      try {
        const token = localStorage.getItem("access_token");
        if (!token) {
          this.$router.push({ name: "login" });
          return;
        }

        const userResponse = await fetch("http://127.0.0.1:8000/api/me", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!userResponse.ok) throw new Error("Fehler beim Laden der Benutzerdaten");
        this.user = await userResponse.json();
      } catch (error) {
        console.error("Fehler beim Laden der Benutzerdaten:", error);
        alert("Fehler beim Laden der Benutzerdaten. Bitte erneut anmelden.");
        this.$router.push({ name: "login" });
      }
    },
    async ladeAntraege() {
      try {
        const token = localStorage.getItem("access_token");
        const antragResponse = await fetch("http://127.0.0.1:8000/api/antraege", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!antragResponse.ok) throw new Error("Fehler beim Laden der Anträge");
        this.antraege = await antragResponse.json();
      } catch (error) {
        console.error("Fehler beim Laden der Anträge:", error);
        alert("Fehler beim Abrufen der Anträge.");
      }
    },
    zeigeDetails(antrag) {
      alert(`Details für Antrag ${antrag.id}: ${JSON.stringify(antrag, null, 2)}`);
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleDateString("de-DE");
    },
    logout() {
      localStorage.removeItem("access_token"); // Access Token löschen
      this.$router.push({ name: "login" }); // Weiterleitung zur Login-Seite
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

.logout-button {
  background-color: red;
}

.logout-button:hover {
  background-color: darkred;
}
</style>
