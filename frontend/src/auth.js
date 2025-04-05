import api from "./api.js"; // Adjust the import path as necessary

export const checkAuth = async () => {
  try {
    const response = await api.get("check-auth/", {
      withCredentials: true, //  Ensures cookies (JWT tokens) are sent
    });

    if (response.data.authenticated) {
      console.log(" User is authenticated:", response.data);
      return response.data; // Returns user authentication info
    } else if (response.data.authenticated === false) {
      // refresh the token if not authenticated
      console.log(" User is not authenticated:", response.data);
      const refreshResponse = await refreshToken(); // Refresh the token
      if (refreshResponse) {
        console.log(" Token refreshed successfully:", refreshResponse);
        return refreshResponse; // Return the new token info
      } else {
        console.log(" Token refresh failed:", response.data);
        return null; // Return null if token refresh fails
      }
    }
  } catch (error) {
    console.error(" Check Auth Failed:", error.response?.data || error.message);
    return null;
  }
};

// Refresh the access token using the refresh token
export const refreshToken = async () => {
  try {
    const response = await axios.post("token/refresh/", null, {
      withCredentials: true, // Sends the refresh token from the cookies
    });

    console.log("Token refreshed:", response.data);
    return response.data;
  } catch (error) {
    console.error(
      "Error refreshing token:",
      error.response?.data || error.message
    );
  }
};

export default checkAuth;
