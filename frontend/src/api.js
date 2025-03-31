import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api/user/", // ✅ Your backend URL
  withCredentials: true, // ✅ Ensures cookies (JWT, CSRF) are sent with requests
  headers: {
    "Content-Type": "application/json",
    Accept: "application/json", // ✅ Helps with proper response parsing
  },
});

export default api;
