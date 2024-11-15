import './App.css';
import React, { useState } from 'react';
import LogIn from './LogIn'


function App() {
    // set state variables
    const [loggedIn, setLoggedIn] = useState(false);

    return (
        loggedIn ? 
        <div className = 'App'>
            Your trees
        </div>
        :
        <LogIn setLoggedIn={setLoggedIn} />
    );
}

export default App;
