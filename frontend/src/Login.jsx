import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "./api.js"; // Adjust the import path as necessary
import { checkAuth } from "./auth.js"; // Adjust the import path as necessary

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      await api.post("login/", { username, password });
      alert("Login successful");
      navigate("/chat");
    } catch {
      alert("Login failed");
    }
  };

  return (
    <div className="h-screen flex items-center justify-center bg-cover bg-center bg-[url('https://cdn.dribbble.com/userupload/21283768/file/original-c5e90ec70201619922fb31dc6c408525.gif')]">
      <div className="w-500 flex items-center justify-center bg-gray-100">
        <div className="bg-white p-6 rounded-lg shadow-lg">
          <h2 className="text-2xl mb-4">Login</h2>
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="w-full p-2 mb-2 border"
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full p-2 mb-2 border"
          />
          <button
            onClick={handleLogin}
            className="w-full bg-blue-500 text-white py-2"
          >
            Login
          </button>
        </div>
      </div>
    </div>
  );
}
export default Login;
