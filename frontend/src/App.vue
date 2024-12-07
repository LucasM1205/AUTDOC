<template>
  <div id="app" class="main-container">
    <header class="header">
      <img src="/THM_Logo_4c.png" alt="THM Logo" class="thm-logo" />
      <nav class="navigation">
        <router-link to="/" class="nav-link">Dashboard</router-link>
        <router-link to="/form-selector" class="nav-link">Formulare</router-link>
        <router-link to="/login" class="nav-link">Logout</router-link>
      </nav>
    </header>
    <router-view />
  </div>
</template>

<script>
export default {};
</script>

<style>
/* Globale CSS-Variablen für Primary, Secondary und Highlight Color */
:root {
  --primary-color: #80ba24;
  --secondary-color: #4a5c66;
  --highlight-color: #c1272d;
}

.main-container {
  margin-top: 20px;
  font-family: Arial, sans-serif;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  background-color: white;
  border-bottom: 1px solid #ccc;
}

.thm-logo {
  height: 60px;
}

.navigation {
  display: flex;
  gap: 1rem;
}

.nav-link {
  text-decoration: none;
  color: var(--primary-color);
  font-weight: bold;
}

.nav-link:hover {
  text-decoration: underline;
}

button {
  background-color: var(--primary-color);
  color: white;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
}

button:hover {
  background-color: #6da22d;
}

button.highlight {
  background-color: var(--highlight-color);
}

button.highlight:hover {
  background-color: #a02125;
}
</style>
