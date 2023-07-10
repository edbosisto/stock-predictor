import "./App.css";
import Heading from "./components/Heading";
import MarketDisplay from "./components/MarketDisplay";

function App() {
  return (
    <div className="App">
      <Heading text="Day Trader" />
      <MarketDisplay />
    </div>
  );
}

export default App;
