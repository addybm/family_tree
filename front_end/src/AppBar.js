import './AppBar.css';
import React from 'react';
import { Navbar, Container, Nav, NavDropdown } from 'react-bootstrap';


const AppBar = ({ setLoggedIn, showTreeBuilder, setShowTreeBuilder, handleDeleteTree }) => {

    return (
      <Navbar expand="lg" className="bg-body-tertiary">
        <div className="w-100 d-flex justify-content-between align-items-center">
          <Navbar.Brand className="ms-3">Family Tree</Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav" className="justify-content-end">
            <Nav>
              <NavDropdown title={<img className="pajamas--hamburger"/>} id="basic-nav-dropdown" align="end">
                {showTreeBuilder && <NavDropdown.Item onClick = {() => {setShowTreeBuilder(false)}}>Back</NavDropdown.Item>}
                {showTreeBuilder && <NavDropdown.Item onClick = {handleDeleteTree}>Delete Tree</NavDropdown.Item>}
                <NavDropdown.Item onClick={() => {
                  setLoggedIn(false);
                  setShowTreeBuilder(false);
                  }}>Sign Out</NavDropdown.Item>
              </NavDropdown>
            </Nav>
          </Navbar.Collapse>
        </div>
      </Navbar>
    );
  };
  
  export default AppBar;
  