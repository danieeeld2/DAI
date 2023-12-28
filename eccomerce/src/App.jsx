import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Menu from './components/Menu.jsx'
import Resultados from './components/Resultados.jsx'
import { useEffect } from 'react'; // Add missing import statement
import { PrimeReactProvider, PrimeReactContext } from 'primereact/api';

function App() {
  const [productos, setProductos] = useState([])
  const [productosF, setProductosF] = useState([])
  const [categorias, setCategorias] = useState([]); 

  const cambiado = (evento) => {
    if (evento.target.value !== "") {
      const filteredProductos = productos.filter((producto) => producto.title.includes(evento.target.value))
      setProductosF(filteredProductos)
    } else {
      setProductosF(productos)
    }

    console.log(evento.target.value)
  }

  useEffect(() => {
    fetch("http://localhost:8000/api/products?since=0&to=100")
      .then((response) => response.json())
      .then((prods) => {
        setProductos(prods)
        const uniqueCategorias = Array.from(new Set(prods.map((producto) => producto.category)));
        setCategorias(uniqueCategorias);
        setProductosF(prods)
      });
  }, [])

  return (
    <>
      <Menu cambiado={cambiado} categorias={categorias}/>
      <Resultados productos={productosF}/>
    </>
  )
}

export default App
