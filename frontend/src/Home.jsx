import React from "react";
import { Link } from "react-router-dom";
import "./index.css";

function Home() {
  return (
    <div className="h-screen flex items-center justify-center bg-cover bg-center bg-[url('https://cdn.dribbble.com/userupload/21283768/file/original-c5e90ec70201619922fb31dc6c408525.gif')]">
      <div className="bg-white bg-opacity-80 p-8 rounded-lg shadow-lg text-center max-w-md">
        <h1 className="text-4xl font-bold mb-4 text-gray-900">AI Chatbot</h1>
        <p className="text-gray-700 mb-6">
          Experience the power of AI conversations.
        </p>
        <div className="space-x-4">
          <Link to="/login">
            <button className="px-6 py-2 bg-blue-600 text-white rounded-lg shadow-md hover:bg-blue-700">
              Login
            </button>
          </Link>
          <Link to="/register">
            <button className="px-6 py-2 bg-green-600 text-white rounded-lg shadow-md hover:bg-green-700">
              Register
            </button>
          </Link>
        </div>
      </div>
    </div>
  );
}

export default Home;
