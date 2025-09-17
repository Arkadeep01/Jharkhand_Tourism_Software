// firebase.ts
import { initializeApp } from "firebase/app";
import { getstorage} from "firebase/storage";
import { getFirestore } from "firebase/firestore";
import {
  getAuth,
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signInWithPopup,
  GoogleAuthProvider,
  FacebookAuthProvider,
  RecaptchaVerifier,
  signInWithPhoneNumber,
} from "firebase/auth";

// Your Firebase config
const firebaseConfig = {
  apiKey: "AIzaSyBiA8vDo18bllLGTM79qGPRQdSDkRGKzSI",
  authDomain: "jharkhand-tourism-software.firebaseapp.com",
  projectId: "jharkhand-tourism-software",
  storageBucket: "jharkhand-tourism-software.firebasestorage.app",
  messagingSenderId: "372713701984",
  appId: "1:372713701984:web:cd593f276f1e2dbb917905"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const db = getFirestore(app);
export const auth = getAuth(app);
export const storage = getstorage(app);

// -----------------------
// Email/Password
// -----------------------
export const signUpWithEmail = async (email: string, password: string) => {
  const userCredential = await createUserWithEmailAndPassword(auth, email, password);
  return userCredential.user;
};

export const signInWithEmail = async (email: string, password: string) => {
  const userCredential = await signInWithEmailAndPassword(auth, email, password);
  return userCredential.user;
};

// -----------------------
// Google
// -----------------------
const googleProvider = new GoogleAuthProvider();
export const signInWithGoogle = async () => {
  const result = await signInWithPopup(auth, googleProvider);
  return result.user;
};

// -----------------------
// Facebook
// -----------------------
const facebookProvider = new FacebookAuthProvider();
export const signInWithFacebook = async () => {
  const result = await signInWithPopup(auth, facebookProvider);
  return result.user;
};

// -----------------------
// Phone
// -----------------------
export const setupRecaptcha = (containerId: string) => {
  return new RecaptchaVerifier(containerId, {
    size: "invisible", // or "normal" if you want the widget
    callback: (response: any) => {
      console.log("Recaptcha verified:", response);
    },
  }, auth);
};

export const sendOTP = async (phoneNumber: string, appVerifier: RecaptchaVerifier) => {
  return await signInWithPhoneNumber(auth, phoneNumber, appVerifier);
  // You can use confirmationResult.confirm(code) to complete sign-in with the code sent via SMS
};




export default app;
