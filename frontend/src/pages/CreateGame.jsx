import { useState } from "react";
import api from "../api";
import { useNavigate } from "react-router-dom";

export default function CreateGame() {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [price, setPrice] = useState("");
  const [stock, setStock] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    const user_id = localStorage.getItem("user_id");

    // Validaciones básicas
    if (!title.trim()) {
      alert("El título es obligatorio");
      return;
    }

    const priceFloat = parseFloat(price);
    if (isNaN(priceFloat)) {
      alert("El precio debe ser un número válido");
      return;
    }

    const stockInt = parseInt(stock) || 0;

    try {
      const res = await api.post("/games/", {
        user_id: parseInt(user_id),
        title: title.trim(),
        description: description.trim(),
        price: priceFloat,
        stock: stockInt,
      });

      alert(res.data.message || "Juego creado ✅");
      navigate("/"); // vuelve al Home
    } catch (err) {
      alert(err.response?.data?.error || "Error al crear juego ❌");
    }
  };

  return (
    <div style={{ maxWidth: "500px", margin: "auto", padding: "20px" }}>
      <h2>Crear Juego</h2>
      <form onSubmit={handleSubmit}>
        <input
          placeholder="Título del juego *"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />
        <textarea
          placeholder="Descripción del juego"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
        <input
          type="number"
          step="0.01"
          placeholder="Precio *"
          value={price}
          onChange={(e) => setPrice(e.target.value)}
          required
        />
        <input
          type="number"
          placeholder="Stock"
          value={stock}
          onChange={(e) => setStock(e.target.value)}
        />
        <button type="submit">Crear</button>
      </form>
    </div>
  );
}
