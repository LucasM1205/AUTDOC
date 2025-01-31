<template>
  <div class="login-container">
    <h1>Anmeldung</h1>
    <form @submit.prevent="handleLogin">
      <div class="form-group">
        <label for="username">Benutzerkennung</label>
        <input
          type="text"
          id="username"
          v-model="loginData.username"
          placeholder="Benutzerkennung eingeben"
          required
        />
      </div>
      <div class="form-group">
        <label for="password">Passwort</label>
        <input
          type="password"
          id="password"
          v-model="loginData.password"
          placeholder="Passwort eingeben"
          required
        />
      </div>
      <div class="button-group">
        <button type="submit">Anmelden</button>
      </div>
    </form>
    <p v-if="errorMessage" class="error-message">
      {{ errorMessage }}. Bitte überprüfen Sie Ihre Benutzerkennung und Ihr Passwort.
    </p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      loginData: {
        username: "", // Geändert von "email" zu "username"
        password: "",
      },
      errorMessage: null,
    };
  },
  methods: {
    async handleLogin() {
      try {
        // Erstellung von Form-Daten für FastAPI
        const formData = new URLSearchParams();
        formData.append("username", this.loginData.username); // Geändert von "email"
        formData.append("password", this.loginData.password);

        // Fetch-Request an den Token-Endpunkt
        const response = await fetch("http://127.0.0.1:8000/token", {
          method: "POST",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
          body: formData,
        });

        if (!response.ok) {
          const errorDetails = await response.json();
          console.error("Fehlerdetails:", errorDetails);
          throw new Error(errorDetails.detail || "Anmeldung fehlgeschlagen.");
        }

        const data = await response.json();
        console.log("Token erhalten:", data.access_token);

        // Token im localStorage speichern
        localStorage.setItem("access_token", data.access_token);

        // Weiterleitung nach erfolgreicher Anmeldung zum Dashboard
        this.$router.push({ name: "dashboard" });
      } catch (error) {
        console.error("Fehler:", error);
        this.errorMessage = error.message || "Anmeldung fehlgeschlagen.";
      }
    },
  },
};
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
}
.form-group {
  margin-bottom: 1rem;
}
.form-group label {
  display: block;
  margin-bottom: 0.5rem;
}
.form-group input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.button-group {
  text-align: center;
}
.error-message {
  color: red;
  margin-top: 1rem;
  text-align: center;
}
</style>
