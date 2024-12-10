// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyDGgOd-GSerBuo4440slhGT_nLu4-Jj2nw",
  authDomain: "dae-ai-project.firebaseapp.com",
  projectId: "dae-ai-project",
  storageBucket: "dae-ai-project.firebasestorage.app",
  messagingSenderId: "817424938335",
  appId: "1:817424938335:web:63e149b385b1a3d1d172ea",
  measurementId: "G-FWM0BRBTTQ"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);