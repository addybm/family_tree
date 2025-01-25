import './TreePreview.css';
import React, { useState } from 'react';
import AppBar from './AppBar';
import { Card, ModalTitle } from 'react-bootstrap';

const TreePreview = ({ title, idx, handleClick }) => {

    const colorOptions = ['#FF9AA2', '#FFB7B2', '#FFDAC1', '#E2F0CB', '#B5EAD7', '#C7CEEA']

    return (
        <div className = 'TreePreview-body'>
            <Card className = 'text-center card-hover'
            style={{maxHeight : '150px', backgroundColor : title == '' ? '#d1dffc' : 'white'}}
            onClick = {() => handleClick(idx)}>
                <Card.Body>
                    <div style = {{ 'color' : title == '' ? 'black' : colorOptions[idx % 6]}}>
                        <span class="clarity--tree-line"></span>
                    </div>
                    {title == '' ? 
                        <Card.Title style={{textOverflow : 'ellipsis', overflow : 'hidden', whiteSpace : 'nowrap'}}>
                            Create Tree
                        </Card.Title> :
                        <Card.Title style={{textOverflow : 'ellipsis', overflow : 'hidden', whiteSpace : 'nowrap'}}>
                            {title}
                        </Card.Title>
                    }
                </Card.Body>
            </Card>
        </div>
    );
};

export default TreePreview;

