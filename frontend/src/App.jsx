import { useState, useEffect } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Home from "./pages/Home";
import CreateGame from "./pages/CreateGame";
import EditGame from "./pages/EditGame"; // Importa la nueva página

export default function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const user_id = localStorage.getItem("user_id");
    const is_admin = localStorage.getItem("is_admin");

    if (user_id) {
      setUser({ id: parseInt(user_id), is_admin: is_admin === "true" });
    }
  }, []);

  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/"
          element={user ? <Home user={user} setUser={setUser} /> : <Navigate to="/login" />}
        />
        <Route path="/login" element={<Login setUser={setUser} />} />
        <Route path="/register" element={<Register />} />
        
        {/* ✅ Ruta para crear juegos solo admins */}
        <Route
          path="/create-game"
          element={user && user.is_admin ? <CreateGame /> : <Navigate to="/" />}
        />

        {/* ✅ Ruta para editar juegos solo admins */}
        <Route
          path="/edit-game/:id"
          element={user && user.is_admin ? <EditGame /> : <Navigate to="/" />}
        />
      </Routes>
    </BrowserRouter>
  );
}

