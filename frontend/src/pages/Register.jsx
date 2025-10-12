import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import api from "../api";

export default function Register() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [isAdmin, setIsAdmin] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await api.post("/auth/register", {
        username,
        password,
        is_admin: isAdmin,
      });

      alert(res.data.message || "Usuario registrado ✅");
      navigate("/login");
    } catch (err) {
      if (err.response?.data?.error) {
        alert("Error: " + err.response.data.error);
      } else {
        alert("Error al registrar usuario ❌");
      }
    }
  };

  return (
    <div style={{ maxWidth: "400px", margin: "auto", padding: "20px" }}>
      <h2 style={{ textAlign: "center" }}>Registro</h2>
      <form onSubmit={handleSubmit}>
        <input
          placeholder="Usuario"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
          style={{ width: "100%", padding: "8px", margin: "8px 0" }}
        />
        <input
          type="password"
          placeholder="Contraseña"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          style={{ width: "100%", padding: "8px", margin: "8px 0" }}
        />
        <label style={{ display: "flex", alignItems: "center", marginTop: "10px" }}>
          <input
            type="checkbox"
            checked={isAdmin}
            onChange={(e) => setIsAdmin(e.target.checked)}
            style={{ marginRight: "8px" }}
          />
          Registrar como Administrador
        </label>
        <button
          type="submit"
          style={{
            marginTop: "20px",
            width: "100%",
            padding: "10px",
            backgroundColor: "#4CAF50",
            color: "white",
            border: "none",
            cursor: "pointer",
          }}
        >
          Registrar
        </button>
      </form>

      {/* 👇 Enlace de vuelta al login */}
      <div style={{ textAlign: "center", marginTop: "20px" }}>
        <p>
          ¿Ya tienes cuenta?{" "}
          <Link to="/login" style={{ color: "#007bff", textDecoration: "none" }}>
            Inicia sesión aquí
          </Link>
        </p>
      </div>
    </div>
  );
}
