import { createRouter, createWebHistory } from 'vue-router';
import Dashboard from '../components/Dashboard.vue';
import LoginForm from '../components/LoginForm.vue';
import FormSelector from '../components/FormSelector.vue';
import JokerAntragForm from '../components/JokerAntragForm.vue';
//import AbschlussarbeitExternForm from '../components/AbschlussarbeitExternForm.vue';

const routes = [
  { 
    path: '/', 
    name: 'dashboard', 
    component: Dashboard 
  }, 
  { 
    path: '/login', 
    name: 'login', 
    component: LoginForm 
  }, 
  { 
    path: '/form-selector', 
    name: 'form-selector', 
    component: FormSelector 
  },
  {
    path: '/joker',
    name: 'joker',
    component: JokerAntragForm,
  },
  {
    path: '/bpp',
    name: 'bpp',
    component: () => import('../components/BppForm.vue'),
  },
  {
    path: '/abschlussarbeit',
    name: 'abschlussarbeit',
    component: () => import('../components/AbschlussarbeitForm.vue'),
  },
  {
    path: '/abschlussarbeit-extern',
    name: 'abschlussarbeit-extern',
    component: () => import('../components/AbschlussarbeitExternForm.vue'),
  },
  {
    path: '/verlaengerung',
    name: 'verlaengerung',
    component: () => import('../components/VerlaengerungForm.vue'),
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Session-Initialisierung
if (!localStorage.getItem('session_initialized')) {
  localStorage.removeItem('access_token'); // Token löschen
  localStorage.setItem('session_initialized', 'true'); // Neue Session setzen
}

// Navigation Guards für geschützte Routen
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("access_token");

  if (!token && to.name !== "login") {
    next({ name: "login" }); // Weiterleitung zur Login-Seite
  } else if (token && to.name === "login") {
    next({ name: "dashboard" }); // Weiterleitung zum Dashboard
  } else {
    next(); // Fortfahren
  }
});

export default router;
