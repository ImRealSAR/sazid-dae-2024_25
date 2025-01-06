import React, { useState } from "react";
import Header from "./Header";
import Footer from "./Footer";
import Greeting from "./Greeting";
import Logo from "./Logo";

function App() {
  const [count, setCount] = useState(0);

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <Header />
      <Logo />
      <Greeting message="Hello, welcome to Sazid's DAE AI Project!" />
      <div style={{ margin: "20px 0" }}>
        <p>Count: {count}</p>
        <button onClick={() => setCount(count + 1)}>Increase Count</button>
      </div>
      <Footer />
    </div>
  );
}

export default App;