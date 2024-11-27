import './TreeSelector.css';
import React, { useState } from 'react';
import AppBar from './AppBar';
import { Row, Col, Card } from 'react-bootstrap';

const TreeSelector = ({ setLoggedIn }) => {
    const exampleTreeData = ["t1", "t2", "t3", "t4"];
    return (
        <div className='TreeSelector-body'>
            <AppBar setLoggedIn={setLoggedIn} />
            <div>
                Your Trees:
            </div>
            <Row>
                {exampleTreeData.map((tree, index) => (
                    <Col key={index} sm={12} md={6} lg={4} xl={3}>
                        <Card>
                            {tree}
                        </Card>
                    </Col>
                ))}
            </Row>
        </div>
    );
};

export default TreeSelector;

