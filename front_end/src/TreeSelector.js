import './App.css';
import React, { useState } from 'react';
import Button from 'react-bootstrap/Button';
import AppBar from './AppBar';

const TreeSelector = ({ setLoggedIn }) => {
    return (
        <React.Fragment>
            <AppBar/>
            <div>
                Your Tressss
                <Button id = 'logoutButton' className = 'mt-2' variant="light" onClick={() => {setLoggedIn()}}>
                        sign out
                </Button>
            </div>
        </React.Fragment>
    );
};

export default TreeSelector;

