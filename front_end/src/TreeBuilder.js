import './TreeBuilder.css';
import React, { useState } from 'react';
import { Button } from 'react-bootstrap';
import AppBar from './AppBar';
import Modal from 'react-bootstrap/Modal';
import Form from 'react-bootstrap/Form';

const TreeBuilder = ({ treeTitle, setTreeBuilder, setLoggedIn, getUsername }) => {

    const [showDeleteModal, setShowDeleteModal] = useState(false);

    const handleAddPerson = () => {
        // display an editing view for a Person
    }

    const handleDeleteTree = () => {
        // delete the tree from the database
        //TODO: add an "are you sure?" dialog
        fetch("http://localhost:5002/api/remove_tree", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ username: getUsername(), tree_name: treeTitle }),
        })
        .then((response) => {
            return response.json().then((data) => ({ status: response.ok, data }));
        })
        .then(({ status, data }) => {
            if (!status) {
                console.error("Error deleting tree:", data.message);
                alert("Failed to delete tree. Please try again.");
            } else {
                setTreeBuilder(false);
            }
        })
        .catch((error) => {
            console.error("Error deleting tree:", error);
            alert("Failed to delete tree. Please try again.");
        });
    }

    return (
        <React.Fragment>
            <Modal show = {showDeleteModal} onHide = {() => {setShowDeleteModal(false)}}>
                <Modal.Header closeButton>
                    <Modal.Title>Are you sure?</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>Are you sure you want to delete "{treeTitle}" and all of its data? This is irreversible.</Modal.Body>
                    <Modal.Footer>
                        <Button variant="secondary" onClick = {() => {setShowDeleteModal(false)}}>
                            Cancel
                        </Button>
                        <Button variant="primary" onClick = {handleDeleteTree} style = {{backgroundColor : "red", borderColor : "red"}}>
                            Delete Tree
                        </Button>
                    </Modal.Footer>
            </Modal>
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
            <Button onClick = {() => {setShowDeleteModal(true)}}>
                Delete tree
            </Button>
        </React.Fragment>
       
    );
};

export default TreeBuilder;

