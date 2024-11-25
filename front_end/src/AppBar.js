import './AppBar.css';
import React from 'react';
import { Navbar, Container, Nav, NavDropdown } from 'react-bootstrap';


const AppBar = () => {
    return (
      <Navbar expand="lg" className="bg-body-tertiary">
        <div className="w-100 d-flex justify-content-between align-items-center">
          <Navbar.Brand className="ms-3">Family Tree</Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav" className="justify-content-end">
            <Nav>
              <NavDropdown title={<img className="pajamas--hamburger"/>} id="basic-nav-dropdown">
                <NavDropdown.Item href="#action/3.1">Action</NavDropdown.Item>
                <NavDropdown.Item href="#action/3.2">Another action</NavDropdown.Item>
                <NavDropdown.Item href="#action/3.3">Something</NavDropdown.Item>
                <NavDropdown.Divider />
                <NavDropdown.Item href="#action/3.4">Separated link</NavDropdown.Item>
              </NavDropdown>
            </Nav>
          </Navbar.Collapse>
        </div>
      </Navbar>
    );
  };
  
  export default AppBar;