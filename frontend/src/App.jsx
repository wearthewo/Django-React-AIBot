import { Routes, Route } from "react-router-dom";
import { useEffect, useState } from "react";
import { Navigate } from "react-router-dom";
import Home from "./Home";
import Login from "./Login";
import Register from "./Register";
import Chat from "./Chat";
import { checkAuth } from "./auth.js";

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(null);

  useEffect(() => {
    const fetchAuthStatus = async () => {
      const result = await checkAuth();
      setIsAuthenticated(result);
    };

    fetchAuthStatus();
  }, []);

  //if (isAuthenticated === null) return <div>Loading...</div>;
  return (
    <>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route
          path="/chat"
          element={<Chat />}
          //element={isAuthenticated ? <Chat /> : <Navigate to="/login" />}
        />
      </Routes>
    </>
  );
}

export default App;
