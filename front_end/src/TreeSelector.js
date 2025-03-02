import './TreeSelector.css';
import React, { useState } from 'react';
import AppBar from './AppBar';
import { Row, Col, Container } from 'react-bootstrap';
import TreePreview from './TreePreview';

const TreeSelector = ({ setLoggedIn, setTreeBuilder, setTreeTitle }) => {
    //array of titles
    // const exampleTreeData = [];
    const exampleTreeData = ['Larsen', 'Mannion', 'Mirliani', 'A Very Long Family Name As An Example Here', 'blue', 'purple', 'red'];

    //add a create_tree object to the list to map over
    exampleTreeData.push('');

    const handleCardClick = (index) => {
        setTreeBuilder(true);
        setTreeTitle(exampleTreeData[index]);
    };

    return (
        <div className = 'TreeSelector-body'>
            <AppBar setLoggedIn = {setLoggedIn} />
            <div>
                Your Trees:
            </div>
            {exampleTreeData.length == 0 ? 
                <div>
                    <TreePreview pic = {null} title = {null}/>
                </div>
                :
                <Container>
                     <Row className = 'g-4'>
                        {exampleTreeData.map((title, index) => (
                            <Col key = {index} sm = {6} md = {5} lg = {4} xl = {2}>
                                <TreePreview title = {title} idx = {index} handleClick = {handleCardClick}/>
                            </Col>
                        ))}
                    </Row>
                </Container>}
        </div>
    );
};

export default TreeSelector;

