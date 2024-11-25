import './App.css';
import React, { useState } from 'react';
import Button from 'react-bootstrap/Button';

const TreeSelector = ({ setLoggedIn }) => {
    return (
        <div>
            Your Tressss
            <Button id = 'logoutButton' className = 'mt-2' variant="light" onClick={() => {setLoggedIn()}}>
                    sign out
            </Button>
        </div>
    );
};

export default TreeSelector;

