import React, { useState } from "react";
import Header from "./header";
import Footer from "./footer";
import Greeting from "./wsg";
import Logo from "./image";

function App() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <Header />
      <Logo />
      <Greeting message="Hello" />
      <p style={{ textAlign: "center" }}>
        Count: {count}{" "}
        <button onClick={() => setCount(count + 1)}>Increase Count</button>
      </p>
      <Footer />
    </div>
  );
}

export default App;
