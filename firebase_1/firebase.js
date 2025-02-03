// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.5/firebase-app.js";
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword, sendEmailVerification, deleteUser } from "https://www.gstatic.com/firebasejs/10.12.5/firebase-auth.js";
import { getStorage, ref, uploadBytes, getDownloadURL } from "https://www.gstatic.com/firebasejs/10.12.5/firebase-storage.js";
import { getFirestore, doc, setDoc, getDoc, updateDoc, deleteDoc } from "https://www.gstatic.com/firebasejs/10.12.5/firebase-firestore.js";

// Your web app's Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyDHCuWQE5DgQBxT5rYh97j2KO6GAOqbCrs",
    authDomain: "soute-sardev.firebaseapp.com",
    projectId: "soute-sardev",
    storageBucket: "soute-sardev.appspot.com",
    messagingSenderId: "761868083764",
    appId: "1:761868083764:web:05d6473183b78a318da061",
    measurementId: "G-3WWKCGYE0J"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const storage = getStorage(app); // Initialize Firebase Storage
const db = getFirestore(app); // Initialize Firestore

// Function to log message to console and display as an alert
function logAndAlert(message) {
    console.log(message);
    alert(message);
}

// Event listeners after DOM content is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Sign Up
    document.getElementById('signUp')?.addEventListener('click', () => {
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        createUserWithEmailAndPassword(auth, email, password)
            .then((userCredential) => {
                logAndAlert('User signed up: ' + userCredential.user.email);
                sendVerificationEmail(userCredential.user); // Send verification email
            })
            .catch((error) => {
                logAndAlert('Sign-up error: ' + error.message);
            });
    });

    // Sign In
    document.getElementById('signIn')?.addEventListener('click', () => {
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        signInWithEmailAndPassword(auth, email, password)
            .then((userCredential) => {
                logAndAlert('User signed in: ' + userCredential.user.email);
            })
            .catch((error) => {
                logAndAlert('Sign-in error: ' + error.message);
            });
    });

    // Delete Account
    document.getElementById('deleteAccount')?.addEventListener('click', () => {
        const user = auth.currentUser;
        deleteUser(user)
            .then(() => {
                logAndAlert('User account deleted.');
            })
            .catch((error) => {
                logAndAlert('Error deleting user account: ' + error.message);
            });
    });

    // View User Profile
    document.getElementById('showProfile')?.addEventListener('click', () => {
        const user = auth.currentUser;
        if (user) {
            logAndAlert('User email: ' + user.email);
        } else {
            logAndAlert('No user is signed in.');
        }
    });

    // Upload File to Firebase Storage
    document.getElementById('uploadButton')?.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            uploadFile(file).then((url) => {
                logAndAlert('File uploaded successfully. Download URL: ' + url);
            });
        }
    });

    // Firestore Create Document
    document.getElementById('createDocument')?.addEventListener('click', async () => {
        const docId = document.getElementById('docId').value;
        const data = { name: "Sample Name", description: "Sample Description" };
        try {
            await setDoc(doc(db, "collectionName", docId), data);
            logAndAlert('Document created successfully.');
        } catch (error) {
            logAndAlert('Error creating document: ' + error.message);
        }
    });

    // Firestore Read Document
    document.getElementById('readDocument')?.addEventListener('click', async () => {
        const docId = document.getElementById('docId').value;
        try {
            const docRef = doc(db, "collectionName", docId);
            const docSnap = await getDoc(docRef);
            if (docSnap.exists()) {
                logAndAlert('Document data: ' + JSON.stringify(docSnap.data()));
            } else {
                logAndAlert('No such document!');
            }
        } catch (error) {
            logAndAlert('Error reading document: ' + error.message);
        }
    });

    // Firestore Update Document
    document.getElementById('updateDocument')?.addEventListener('click', async () => {
        const docId = document.getElementById('docId').value;
        const updatedData = { description: "Updated Description" };
        try {
            const docRef = doc(db, "collectionName", docId);
            await updateDoc(docRef, updatedData);
            logAndAlert('Document updated successfully.');
        } catch (error) {
            logAndAlert('Error updating document: ' + error.message);
        }
    });

    // Firestore Delete Document
    document.getElementById('deleteDocument')?.addEventListener('click', async () => {
        const docId = document.getElementById('docId').value;
        try {
            const docRef = doc(db, "collectionName", docId);
            await deleteDoc(docRef);
            logAndAlert('Document deleted successfully.');
        } catch (error) {
            logAndAlert('Error deleting document: ' + error.message);
        }
    });
});

// Function to send email verification
function sendVerificationEmail(user) {
    sendEmailVerification(user)
        .then(() => {
            logAndAlert('Verification email sent.');
        })
        .catch((error) => {
            logAndAlert('Error sending verification email: ' + error.message);
        });
}

// Function to upload file to Firebase Storage
async function uploadFile(file) {
    const storageRef = ref(storage, 'uploads/' + file.name);
    try {
        const snapshot = await uploadBytes(storageRef, file);
        logAndAlert('Uploaded a file!');
        const downloadURL = await getDownloadURL(storageRef);
        return downloadURL;
    } catch (error) {
        console.error('Upload failed', error);
    }
}

// Function to download file from Firebase Storage
async function downloadFile(filePath) {
    const storageRef = ref(storage, filePath);
    try {
        const downloadURL = await getDownloadURL(storageRef);
        logAndAlert('File available at ' + downloadURL);
    } catch (error) {
        console.error('Download failed', error);
    }
}
