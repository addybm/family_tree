import './TreeSelector.css';
import React, { useState } from 'react';
import AppBar from './AppBar';
import { Row, Col } from 'react-bootstrap';
import TreePreview from './TreePreview';

const TreeSelector = ({ setLoggedIn }) => {
    //const exampleTreeData = [["pic1", "t1"], ["pic2", "t2"], ["pic3", "t3"], ["pic4", "t4"]];
    const exampleTreeData = [];
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
                        {exampleTreeData.map(([pic, title], index) => (
                            <Col key={index} sm={12} md={6} lg={4} xl={3}>
                                <TreePreview pic = {pic} title = {title}/>
                            </Col>
                        ))}
                    </Row>
                </div>}
        </div>
    );
};

export default TreeSelector;

