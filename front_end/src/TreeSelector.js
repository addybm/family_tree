import './TreeSelector.css';
import React, { useState } from 'react';
import AppBar from './AppBar';
import { Row, Col } from 'react-bootstrap';
import TreePreview from './TreePreview';

const TreeSelector = ({ setLoggedIn }) => {
    //array of titles
    // const exampleTreeData = [];
    const exampleTreeData = ['red', 'orange', 'yellow', 'green', 'blue', 'purple', 'red']
    return (
        <div className = 'TreeSelector-body'>
            <AppBar setLoggedIn={setLoggedIn} />
            <div>
                Your Trees:
            </div>
            {exampleTreeData.length == 0 ? 
                <div>
                    <TreePreview pic = {null} title = {null}/>
                </div>
                :
                <div>
                     <Row>
                        {exampleTreeData.map((title, index) => (
                            <Col key={index} sm={12} md={6} lg={4} xl={3}>
                                <TreePreview title = {title} idx = {index}/>
                            </Col>
                        ))}
                    </Row>
                </div>}
        </div>
    );
};

export default TreeSelector;

