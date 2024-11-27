import './AppBar.css';
import React from 'react';
import { Navbar, Container, Nav, NavDropdown } from 'react-bootstrap';


const AppBar = ({ setLoggedIn }) => {
    return (
      <Navbar expand="lg" className="bg-body-tertiary">
        <div className="w-100 d-flex justify-content-between align-items-center">
          <Navbar.Brand className="ms-3">Family Tree</Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav" className="justify-content-end">
            <Nav>
              <NavDropdown title={<img className="pajamas--hamburger"/>} id="basic-nav-dropdown" align="end">
                <NavDropdown.Item onClick={() => {setLoggedIn(false)}}>Sign Out</NavDropdown.Item>
              </NavDropdown>
            </Nav>
          </Navbar.Collapse>
        </div>
      </Navbar>
    );
  };
  
  export default AppBar;
  