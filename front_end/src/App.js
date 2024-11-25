import './App.css';
import React, { useEffect, useState } from 'react';
import LogIn from './LogIn'
import TreeSelector from './TreeSelector';


function App() {
    // set state variables
    const [loggedIn, setLoggedIn] = useState(() => {
        const loggedIn = localStorage.getItem('loggedIn') === "true";
        return loggedIn;
    });

    return (
        loggedIn ? 
        <TreeSelector setLoggedIn = {() => {
            localStorage.setItem('loggedIn', false)
            setLoggedIn(false);
        }}/>
        :
        <LogIn setLoggedIn = {() => {
            localStorage.setItem('loggedIn', true)
            setLoggedIn(true);
        }} />
    );
}

export default App;
