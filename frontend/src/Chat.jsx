import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "./api.js"; // Adjust the import path as necessary
import checkAuth from "./auth.js";

function Chat() {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [isAuthenticated, setIsAuthenticated] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchAuthStatus = async () => {
      const result = await checkAuth();
      setIsAuthenticated(result);
      if (!result) {
        navigate("/chat"); // ✅ Redirect to login if not authenticated
      }
    };
    fetchAuthStatus();
  }, [navigate]);

  const sendMessage = async () => {
    if (!message.trim()) return; // Prevent sending empty messages

    // Add user message to chat
    setChatHistory((prevChat) => [
      ...prevChat,
      { sender: "user", text: message },
    ]);

    try {
      const res = await api.post("messages/", { message }); // ✅ Sends message with cookies

      // Add AI response to chat
      setChatHistory((prevChat) => [
        ...prevChat,
        { sender: "user", text: message },
        { sender: "ai", text: res.data.response },
      ]);

      setMessage(""); // Clear input after sending
    } catch (error) {
      setChatHistory((prevChat) => [
        ...prevChat,
        { sender: "ai", text: "Error getting response." },
      ]);
    }
  };

  const handleLogout = async () => {
    try {
      await api.post("logout/"); // ✅ Logout request
      alert("Logged out successfully");
      navigate("/login"); // ✅ Redirect to login
    } catch (error) {
      console.error("Logout failed", error);
    }
  };

  return (
    <div className="h-screen flex items-center justify-center bg-cover bg-center bg-[url('https://cdn.dribbble.com/userupload/21283768/file/original-c5e90ec70201619922fb31dc6c408525.gif')]">
      <div className="w-1000 flex flex-col items-center justify-center bg-gray-100 p-4">
        <div className="w-full max-w-lg bg-white p-6 rounded-lg shadow-lg">
          <h2 className="text-2xl mb-4">Chat</h2>
          <div className="bg-gray-200 p-4 rounded-md h-64 overflow-auto mb-4">
            {chatHistory.map((chat, index) => (
              <div
                key={index}
                className={`p-2 my-1 rounded ${
                  chat.sender === "user"
                    ? "bg-blue-300 text-right"
                    : "bg-gray-300 text-left"
                }`}
              >
                <strong>{chat.sender === "user" ? "You" : "AI"}:</strong>{" "}
                {chat.text}
              </div>
            ))}
          </div>
          <textarea
            className="w-full p-2 border mb-2"
            placeholder="Type a message..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
          ></textarea>
          <button
            onClick={sendMessage}
            className="w-full bg-blue-500 text-white py-2"
          >
            Send
          </button>
          {/* AI Response Box */}
          <div className="bg-gray-200 p-4 rounded-md h-32 overflow-auto mb-4">
            {response ? response : "Waiting for response..."}
          </div>
          <button
            onClick={handleLogout}
            className="absolute top-4 right-4 bg-red-500 text-white px-4 py-2 rounded-md hover:bg-red-600"
          >
            Logout
          </button>
        </div>
      </div>
    </div>
  );
}

export default Chat;
