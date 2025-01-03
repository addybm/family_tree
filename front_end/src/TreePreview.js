import './TreePreview.css';
import React, { useState } from 'react';
import AppBar from './AppBar';
import { Card, ModalTitle } from 'react-bootstrap';

const TreePreview = ({ title, idx }) => {

    const colorOptions = ['#FF9AA2', '#FFB7B2', '#FFDAC1', '#E2F0CB', '#B5EAD7', '#C7CEEA']

    return (
        <div className = 'TreePreview-body'>
            <Card>
                <Card.Body>
                    <div style = {{ 'color' : colorOptions[idx % 6] }}>
                        <span class="clarity--tree-line"></span>
                    </div>
                    <Card.Title>
                        {title}
                    </Card.Title>
                </Card.Body>
            </Card>
        </div>
    );
};

export default TreePreview;

