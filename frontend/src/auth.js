import api from "./api.js"; // Adjust the import path as necessary

export const checkAuth = async () => {
  try {
    const response = await api.get("check-auth/", {
      withCredentials: true, //  Ensures cookies (JWT tokens) are sent
    });

    if (response.data.authenticated) {
      console.log(" User is authenticated:", response.data);
      return response.data; // Returns user authentication info
    } else {
      console.log(" User is not authenticated");
      return null;
    }
  } catch (error) {
    console.error(" Check Auth Failed:", error.response?.data || error.message);
    return null;
  }
};

export default checkAuth;
