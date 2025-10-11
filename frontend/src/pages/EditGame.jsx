import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../api";

export default function EditGame() {
  const { id } = useParams(); // ID del juego desde la URL
  const navigate = useNavigate();

  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [price, setPrice] = useState("");
  const [stock, setStock] = useState("");

  useEffect(() => {
    fetchGame();
  }, []);

  const fetchGame = async () => {
    try {
      const res = await api.get(`/games/${id}`);
      setTitle(res.data.title);
      setDescription(res.data.description || "");
      setPrice(res.data.price);
      setStock(res.data.stock);
    } catch (err) {
      alert("Error al cargar el juego ❌");
      navigate("/"); // vuelve al home si falla
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.put(`/games/${id}`, {
        title,
        description,
        price: parseFloat(price),
        stock: parseInt(stock),
      });
      alert("Juego actualizado ✅");
      navigate("/"); // vuelve a home
    } catch (err) {
      alert(err.response?.data?.error || "Error al actualizar juego ❌");
    }
  };

  return (
    <div style={{ maxWidth: "400px", margin: "auto", padding: "20px" }}>
      <h2 style={{ textAlign: "center" }}>Editar Juego</h2>
      <form onSubmit={handleSubmit}>
        <input
          placeholder="Título"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
          style={{ width: "100%", padding: "8px", margin: "8px 0" }}
        />
        <input
          placeholder="Descripción"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          style={{ width: "100%", padding: "8px", margin: "8px 0" }}
        />
        <input
          type="number"
          placeholder="Precio"
          value={price}
          onChange={(e) => setPrice(e.target.value)}
          required
          style={{ width: "100%", padding: "8px", margin: "8px 0" }}
        />
        <input
          type="number"
          placeholder="Stock"
          value={stock}
          onChange={(e) => setStock(e.target.value)}
          style={{ width: "100%", padding: "8px", margin: "8px 0" }}
        />
        <button
          type="submit"
          style={{
            marginTop: "15px",
            width: "100%",
            padding: "10px",
            backgroundColor: "#FFC107",
            color: "white",
            border: "none",
            cursor: "pointer",
          }}
        >
          Guardar Cambios
        </button>
      </form>
    </div>
  );
}
