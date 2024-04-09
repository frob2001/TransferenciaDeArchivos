import React from 'react';
import 'primereact/resources/themes/lara-light-indigo/theme.css'; // Tema de PrimeReact
import 'primereact/resources/primereact.min.css'; // Core de PrimeReact
import 'primeicons/primeicons.css'; // Iconos
import TablaSalarios from './TablaSalarios'; // Asegúrate de que la ruta sea correcta
import './App.css';


function App() {
  return (
    <div className="App">
      <TablaSalarios />
    </div>
  );
}

export default App;
