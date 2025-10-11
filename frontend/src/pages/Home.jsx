import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";

export default function Home({ user, setUser }) {
  const [games, setGames] = useState([]);
  const [cart, setCart] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    fetchGames();
  }, []);

  const fetchGames = async () => {
    try {
      const res = await api.get("/games/");
      setGames(res.data);
    } catch (err) {
      alert("Error al cargar los juegos ❌");
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("user_id");
    localStorage.removeItem("is_admin");
    setUser(null);
    navigate("/login");
  };

  const handleCreateGame = () => {
    navigate("/create-game");
  };

  const handleEditGame = (gameId) => {
    navigate(`/edit-game/${gameId}`);
  };

  const handleDeleteGame = async (gameId) => {
    if (!window.confirm("¿Estás seguro de eliminar este juego?")) return;

    try {
      await api.delete(`/games/${gameId}`);
      alert("Juego eliminado ✅");
      fetchGames();
    } catch (err) {
      alert(err.response?.data?.error || "Error al eliminar juego ❌");
    }
  };

  // -------------------------------
  // 📌 Carrito
  // -------------------------------
  const addToCart = (game) => {
    if (game.stock <= 0) {
      alert("No hay stock disponible ❌");
      return;
    }

    const existing = cart.find((item) => item.id === game.id);
    if (existing) {
      if (existing.quantity >= game.stock) {
        alert("No puedes añadir más de este juego, stock limitado ❌");
        return;
      }
      setCart(cart.map((item) => item.id === game.id ? {...item, quantity: item.quantity + 1} : item));
    } else {
      setCart([...cart, {...game, quantity: 1}]);
    }
  };

  const removeFromCart = (gameId) => {
    setCart(cart.filter((item) => item.id !== gameId));
  };

  const handleCheckout = async () => {
    if (cart.length === 0) {
      alert("Tu carrito está vacío ❌");
      return;
    }

    try {
      const user_id = localStorage.getItem("user_id");
      const orderItems = cart.map(item => ({
        game_id: item.id,
        quantity: item.quantity,
        price: item.price
      }));

      const total = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);

      const res = await api.post("/orders/", { user_id, items: orderItems, total });
      alert("Compra realizada ✅");

      setCart([]);
      fetchGames(); // actualizar stock
    } catch (err) {
      alert(err.response?.data?.error || "Error al realizar la compra ❌");
    }
  };

  return (
    <div style={{ maxWidth: "800px", margin: "auto", padding: "20px" }}>
      <h1>Bienvenido a la Tienda, Usuario #{user.id}!</h1>

      {user.is_admin && (
        <>
          <p>Eres administrador ✅</p>
          <button
            onClick={handleCreateGame}
            style={{ padding: "10px 15px", marginBottom: "20px", backgroundColor: "#2196F3", color: "white", border: "none", cursor: "pointer" }}
          >
            Crear Juego
          </button>
        </>
      )}

      <h2>Lista de Juegos</h2>
      {games.length === 0 && <p>No hay juegos disponibles.</p>}
      <ul style={{ listStyle: "none", padding: 0 }}>
        {games.map((game) => (
          <li key={game.id} style={{ border: "1px solid #ccc", padding: "10px", marginBottom: "10px", borderRadius: "5px" }}>
            <strong>{game.title}</strong> - ${game.price.toFixed(2)}
            {game.description && <p>{game.description}</p>}
            <p>Stock disponible: {game.stock}</p>

            <div style={{ marginTop: "10px" }}>
              {!user.is_admin && (
                <button
                  onClick={() => addToCart(game)}
                  style={{ marginRight: "10px", padding: "5px 10px", backgroundColor: "#4CAF50", color: "white", border: "none", cursor: "pointer" }}
                  disabled={game.stock <= 0}
                >
                  Añadir al carrito
                </button>
              )}
              {user.is_admin && (
                <>
                  <button
                    onClick={() => handleEditGame(game.id)}
                    style={{ marginRight: "10px", padding: "5px 10px", backgroundColor: "#FFC107", color: "white", border: "none", cursor: "pointer" }}
                  >
                    Editar
                  </button>
                  <button
                    onClick={() => handleDeleteGame(game.id)}
                    style={{ padding: "5px 10px", backgroundColor: "#f44336", color: "white", border: "none", cursor: "pointer" }}
                  >
                    Eliminar
                  </button>
                </>
              )}
            </div>
          </li>
        ))}
      </ul>

      {cart.length > 0 && (
        <div style={{ marginTop: "20px", border: "1px solid #2196F3", padding: "10px", borderRadius: "5px" }}>
          <h3>Carrito</h3>
          <ul>
            {cart.map(item => (
              <li key={item.id}>
                {item.title} x {item.quantity} - ${(item.price * item.quantity).toFixed(2)}
                <button onClick={() => removeFromCart(item.id)} style={{ marginLeft: "10px" }}>❌</button>
              </li>
            ))}
          </ul>
          <p><strong>Total: ${cart.reduce((sum, item) => sum + item.price * item.quantity, 0).toFixed(2)}</strong></p>
          <button onClick={handleCheckout} style={{ padding: "10px 15px", backgroundColor: "#4CAF50", color: "white", border: "none", cursor: "pointer" }}>Comprar</button>
        </div>
      )}

      <button
        onClick={handleLogout}
        style={{ padding: "10px 15px", backgroundColor: "#f44336", color: "white", border: "none", cursor: "pointer", marginTop: "20px" }}
      >
        Cerrar sesión
      </button>
    </div>
  );
}
