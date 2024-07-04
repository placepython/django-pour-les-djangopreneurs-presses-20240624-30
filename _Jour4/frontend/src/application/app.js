import 'vite/modulepreload-polyfill';

// Importation and configuration of HTMX
import htmx from "htmx.org";
window.htmx = htmx;

// Importation and configuration of Alpine.js
import Alpine from 'alpinejs';
window.Alpine = Alpine;
Alpine.start();

// Entry point for CSS styles
import "../styles/app.css";

