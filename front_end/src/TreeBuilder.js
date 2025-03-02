import './TreeBuilder.css';
import React, { useState } from 'react';
import { Button } from 'react-bootstrap';
import AppBar from './AppBar';

const TreeBuilder = ({ treeTitle, setTreeBuilder, setLoggedIn }) => {

    const handleAddPerson = () => {
        // display an editing view for a Person
    }

    return (
        <React.Fragment>
            <AppBar setLoggedIn = {setLoggedIn} />
            <p>
                {treeTitle}
            </p>
            <Button onClick = {() => setTreeBuilder(false)}>
                Back
            </Button>
            <Button
                style = {{backgroundColor : '#d1dffc', borderColor : '#d1dffc', color : "black"}}
                onClick = {() => {console.log("Add")}}
                className = 'rounded-circle mx-1'>
                +
            </Button>
        </React.Fragment>
       
    );
};

export default TreeBuilder;

