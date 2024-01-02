import React from 'react'
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Form from 'react-bootstrap/Form';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';



export default function Menu({ cambiado, categorias, cambiadoCat }) {
  return (
    <Navbar expand="lg" className="bg-body-tertiary" fixed="top">
      <Container fluid>
        <Navbar.Brand href="#">Tienda DAI</Navbar.Brand>
        <Navbar.Toggle aria-controls="navbarScroll" />
        <Navbar.Collapse id="navbarScroll">
          <Form className="d-flex ms-auto">
            <Form.Select
              className="me-2"
              aria-label="Categorías"
              onChange={(evento) => cambiadoCat(evento)}
            >
              <option value="">Categories</option>
              {categorias.map((categoria, index) => (
                <option key={index} value={categoria}>
                  {categoria}
                </option>
              ))}
            </Form.Select>
            <Form.Control
              type="search"
              placeholder="Search"
              className="me-2"
              aria-label="Search"
              onChange={(evento) => cambiado(evento)}
            />
            <Button variant="outline-success">Search</Button>
          </Form>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}