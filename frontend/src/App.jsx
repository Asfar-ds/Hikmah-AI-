import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Fivelens from "./pages/FiveLens";
import Oppurtunity from "./pages/Oppurtunity";
import Relivency from "./pages/Relivency";
import Settings from "./pages/Settings"
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/fivelens" element={<Fivelens />} />
        <Route path="/relivency" element={<Relivency />} />
        <Route path="/opportunity" element={<Oppurtunity />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
