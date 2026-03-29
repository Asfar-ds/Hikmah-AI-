import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyA0Rs0xMBjPLhxaUgTJB3YfffJiDIsPJrg",
  authDomain: "db-project-bd190.firebaseapp.com",
  projectId: "db-project-bd190",
  storageBucket: "db-project-bd190.firebasestorage.app",
  messagingSenderId: "785116033607",
  appId: "1:785116033607:web:a1a86728f4e23193e23762"
// 290fb5e0553c3e18e30f982ff2f12a8c5e7daed7
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
