import { useEffect, useState } from "react";
import { apiRequest } from "./services/api";

function App() {
  const [message, setMessage] = useState("");

  useEffect(() => {
    apiRequest("/")
      .then((data) => setMessage(data.message))
      .catch(() => setMessage("Backend not reachable"));
  }, []);

  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>
      <h1>ModelDock</h1>
      <p>Backend response:</p>
      <b>{message}</b>
    </div>
  );
}

export default App;