import './AddRelationship.css';
import React, { useState } from 'react';
import Button from 'react-bootstrap/Button';

const AddRelationship = ({ setShowAddRelationship, setShowModifyNodeModal }) => {

    const handleAddPerson = () => {
        //TOOD: add person to database
        setShowModifyNodeModal();
        setShowAddRelationship();
    }
   
    return (
        <React.Fragment>
            <div>
                Add Relationship
            </div>
            <Button onClick = {() => {
                    setShowModifyNodeModal();
                    setShowAddRelationship();
                }}
                variant = 'secondary'
                className = 'm-3'>
                Cancel
            </Button>
            <Button style = {{ backgroundColor: "steelblue", borderColor: "steelblue" }}
                onClick = {handleAddPerson}>
                Add Person
            </Button>
        </React.Fragment>
    );
};

export default AddRelationship;

