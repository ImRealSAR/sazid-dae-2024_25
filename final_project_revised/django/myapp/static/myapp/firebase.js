import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.1/firebase-app.js";
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/9.6.1/firebase-auth.js";
import { getFirestore, doc, setDoc } from "https://www.gstatic.com/firebasejs/9.6.1/firebase-firestore.js";
// 🔐
const firebaseConfig = {
  apiKey: "AIzaSyCFnxD9pC691dV3QFwUUFhCyRr-FZmpHaw",
  authDomain: "intelesense-sar.firebaseapp.com",
  projectId: "intelesense-sar",
  storageBucket: "intelesense-sar.appspot.com",
  messagingSenderId: "149988638839",
  appId: "1:149988638839:web:084070ed33754a233c0672",
  measurementId: "G-BCBF4SJXK1"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

document.addEventListener("DOMContentLoaded", () => {
  const signupForm = document.getElementById("signup-form");
  const loginForm = document.getElementById("login-form");

  if (signupForm) {
    signupForm.addEventListener("submit", (e) => {
      e.preventDefault();
      const email = signupForm.email.value;
      const password = signupForm.password.value;
      createUserWithEmailAndPassword(auth, email, password)
        .then(() => alert("Signup successful!"))
        .catch(err => alert(err.message));
    });
  }

  if (loginForm) {
    loginForm.addEventListener("submit", (e) => {
      e.preventDefault();
      const email = loginForm.email.value;
      const password = loginForm.password.value;
      signInWithEmailAndPassword(auth, email, password)
        .then(() => alert("Login successful!"))
        .catch(err => alert(err.message));
    });
  }


const db = getFirestore(app);

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("onboarding-form");

  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();

      const aiName = document.getElementById("aiName").value;
      const tone = document.getElementById("tone").value;
      const user = auth.currentUser;

      if (!user) {
        alert("You must be logged in to save preferences.");
        return;
      }

      await setDoc(doc(db, "users", user.uid), {
        ai_name: aiName,
        tone: tone
      });

      alert("Saved!");
      window.location.href = "/generate-ai/";
    });
  }
});

});
