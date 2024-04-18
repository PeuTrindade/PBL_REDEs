import { useEffect, useState } from "react";
import List from "./components/List";
import Navbar from "./components/Navbar";

function App() {
  const [devices, setDevices] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000//devices');

        if (response.ok) {
          const result = await response.json();
          const resultValues = Object.values(result)
          const formattedResult = { title: resultValues[0].addressInfo[0], temperature: resultValues[0].sentMessages.temperature, on: resultValues[0].sentMessages.on}

          setDevices([formattedResult]);
        }
      } catch (error) {
        console.info(error);
      }
    };

    fetchData();

    const intervalId = setInterval(fetchData, 3000);

    return () => clearInterval(intervalId);
  }, []);

  return (
    <>
      <Navbar />
      <div style={{ marginTop: '60px'}} className='container col-6'>
        <h3>Meus ar condicionados</h3>
        {devices.length > 0 ? <List items={devices} /> : <p>Não há dispositivos conectados no momento!😓</p>}
      </div>
    </>
  );
}

export default App;
