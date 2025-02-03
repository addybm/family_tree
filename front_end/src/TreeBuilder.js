import './TreeBuilder.css';
import React, { useState } from 'react';
import { Button } from 'react-bootstrap';

const TreeBuilder = ({ treeTitle, setTreeBuilder }) => {

    return (
        <React.Fragment>
            <p>
                {treeTitle}
            </p>
            <Button onClick = {() => setTreeBuilder(false)}>
                Back
            </Button>
        </React.Fragment>
       
    );
};

export default TreeBuilder;

