import './TreePreview.css';
import React, { useState } from 'react';
import AppBar from './AppBar';
import { Card, ModalTitle } from 'react-bootstrap';

const TreePreview = ({ pic, title }) => {
    return (
        <div className = 'TreePreview-body'>
            <Card>
                <Card.Body>
                    <Card.Img variant = 'top' src = {pic}/>
                    <Card.Title>
                        {title}
                    </Card.Title>
                </Card.Body>
            </Card>
        </div>
    );
};

export default TreePreview;

