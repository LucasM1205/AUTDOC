import { createRouter, createWebHistory } from 'vue-router';
import FormSelector from '../components/FormSelector.vue';
import JokerAntragForm from '../components/JokerAntragForm.vue';

const routes = [
  { path: '/', name: 'form-selector', component: FormSelector },
  { path: '/joker', name: 'joker', component: JokerAntragForm },
  { path: '/bpp', name: 'bpp', component: () => import('../components/BppForm.vue') },
  { path: '/abschlussarbeit', name: 'abschlussarbeit', component: () => import('../components/AbschlussarbeitForm.vue') },
  { path: '/verlaengerung', name: 'verlaengerung', component: () => import('../components/VerlaengerungForm.vue') }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
