import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.1/firebase-app.js";
import {
  getAuth,
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  onAuthStateChanged
} from "https://www.gstatic.com/firebasejs/9.6.1/firebase-auth.js";
import {
  getFirestore,
  doc,
  setDoc
} from "https://www.gstatic.com/firebasejs/9.6.1/firebase-firestore.js";

const firebaseConfig = {
  apiKey: "AIzaSyCFnxD9pC691dV3QFwUUFhCyRr-FZmpHaw",
  authDomain: "intelesense-sar.firebaseapp.com",
  projectId: "intelesense-sar",
  storageBucket: "intelesense-sar.appspot.com",
  messagingSenderId: "149988638839",
  appId: "1:149988638839:web:084070ed33754a233c0672"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

document.addEventListener("DOMContentLoaded", () => {
  const signupForm = document.getElementById("signup-form");
  const loginForm = document.getElementById("login-form");

  if (signupForm) {
    signupForm.addEventListener("submit", (e) => {
      e.preventDefault();
      const email = signupForm.email.value;
      const pw = signupForm.password.value;
      const cpw = signupForm.confirm_password.value;
      if (pw !== cpw) return alert("Passwords don't match.");

      createUserWithEmailAndPassword(auth, email, pw)
        .then(() => window.location.href = "/onboarding/")
        .catch(err => alert("Signup error: " + err.message));
    });
  }

  if (loginForm) {
    loginForm.addEventListener("submit", (e) => {
      e.preventDefault();
      const email = loginForm.email.value;
      const pw = loginForm.password.value;

      signInWithEmailAndPassword(auth, email, pw)
        .then(() => window.location.href = "/generate-ai/")
        .catch(err => alert("Login error: " + err.message));
    });
  }
});
