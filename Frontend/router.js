import { createRouter, createWebHistory } from "vue-router";
import TrinoConnectForm from "./components/TrinoConnectForm.vue";
import QueryPage from "./components/QueryPage.vue";
import HomePage from "./components/HomePage.vue";
import ConfigurationPage from "./components/ConfigurationPage.vue";
import ConfirmationPage from "./components/ConfirmationPage.vue";
import EditConfig from "./components/EditConfig.vue";
import LoadConfig from "./components/LoadConfig.vue";
import ConnectionPage from "./components/ConnectionPage.vue";
import AnalyticsPage from "./components/AnalyticsPage.vue";
import SettingsPage from "./components/SettingsPage.vue";
const routes = [
  {
    path: "/",
    name: "home",
    component: HomePage,
  },
  {
    path: "/connect",
    name: "connect",
    component: TrinoConnectForm,
  },
  {
    path: "/query",
    name: "query",
    component: QueryPage,
  },
  {
    path: '/configuration',
    name: 'configuration',
    component: ConfigurationPage,
  },
  {
    path: "/confirmation",
    name: "confirmation",
    component: ConfirmationPage,
  },
  {
    path: "/edit",
    name: "edit",
    component: EditConfig,
  },
  {
    path: "/load",
    name: "load",
    component: LoadConfig,
  },
  {
    path: "/connection",
    name: "connectionPage",
    component: ConnectionPage,
  },
  {
    path: "/analytics",
    name: "analyticsPage",
    component: AnalyticsPage,
  },
  {
    path: "/settings",
    name: "settingsPage",
    component: SettingsPage,
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
