import './App.css';
import React, { useEffect, useState } from 'react';
import LogIn from './LogIn'
import TreeSelector from './TreeSelector';
import TreeBuilder from './TreeBuilder';


function App() {
    // set state variables
    const [loggedIn, setLoggedIn] = useState(() => {
        const loggedIn = localStorage.getItem('loggedIn') === "true";
        return loggedIn;
    });

    const [treeBuilder, setTreeBuilder] = useState(() => {
        const treeBuilder = localStorage.getItem('treeBuilder') === "true";
        return treeBuilder;
    });
    const [treeTitle, setTreeTitle] = useState(() => {
        const treeTitle = localStorage.getItem('treeTitle');
        if (treeTitle != null) {
            return treeTitle;
        } else {
            return "";
        }
    })

    // testing flask connection:
    const [flaskMessage, setFlaskMessage] = useState("");

    useEffect(() => {
        fetch("http://localhost:5002/data")
            .then(response => response.json())
            .then(data => {
                setFlaskMessage(data.message)
                console.log("data fetched: " + data.message)
            });
    }, []);

    return (
        <div className="App">
            {flaskMessage}
        </div>
        // loggedIn ? 
        //     treeBuilder ?
        //         <TreeBuilder treeTitle = {treeTitle}
        //                      setTreeBuilder = {(treeBuilder) => {
        //                         localStorage.setItem('treeBuilder', treeBuilder);
        //                         setTreeBuilder(treeBuilder);
        //                      }}
        //                      setLoggedIn = {() => {
        //                 localStorage.setItem('loggedIn', false);
        //                 setLoggedIn(false);
        //             }}/>
        //         :
        //         <TreeSelector setLoggedIn = {() => {
        //                 localStorage.setItem('loggedIn', false);
        //                 setLoggedIn(false);
        //             }}
        //             setTreeBuilder = {(treeBuilder) => {
        //                 localStorage.setItem('treeBuilder', treeBuilder);
        //                 setTreeBuilder(treeBuilder);
        //             }}
        //             setTreeTitle = {(treeTitle) => {
        //                 localStorage.setItem('treeTitle', treeTitle);
        //                 setTreeTitle(treeTitle);
        //             }}/>
        // :
        // <LogIn setLoggedIn = {() => {
        //     localStorage.setItem('loggedIn', true)
        //     setLoggedIn(true);
        // }} />
    );
}

export default App;
