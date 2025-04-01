import './TreeBuilder.css';
import React, { useState } from 'react';
import { Button, Card } from 'react-bootstrap';
import AppBar from './AppBar';
import Modal from 'react-bootstrap/Modal';
import Form from 'react-bootstrap/Form';

const TreeBuilder = ({ treeTitle, setTreeBuilder, setLoggedIn, getUsername }) => {

    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const [showAddPersonModal, setShowAddPersonModal] = useState(false);
    const [newPersonName, setNewPersonName] = useState('');
    const [newPersonGender, setNewPersonGender] = useState('');
    const [newPersonNickname, setNewPersonNickname] = useState('');
    const [newPersonNotes, setNewPersonNotes] = useState('');

    const handleAddPersonClick = () => {
        //display an editing view for a Person
        console.log("Add Person");
        setShowAddPersonModal(true);
    }

    const handleAddPerson = () => {
        //check that a name and gender are chosen
        if (newPersonName == "" || newPersonGender == "") {
            alert("Error: name and gender are required");
            return;
        }
    }

    const handleAddPersonModalClose = () => {
        setShowAddPersonModal(false);
        setNewPersonName('');
        setNewPersonGender('');
        setNewPersonNickname('');
        setNewPersonNotes('');
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
                        <Button variant = "secondary" onClick = {() => {setShowDeleteModal(false)}}>
                            Cancel
                        </Button>
                        <Button variant = "primary" onClick = {handleDeleteTree} style = {{backgroundColor : "red", borderColor : "red"}}>
                            Delete Tree
                        </Button>
                    </Modal.Footer>
            </Modal>
            <Modal show = {showAddPersonModal} onHide = {handleAddPersonModalClose}>
                <Modal.Header closeButton>
                    <Modal.Title>Add Person</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <Form className = 'my-3'>
                            <Form.Control type = "text" placeholder = "Name"
                            onChange = {(e) => {setNewPersonName(e.target.value)}}/>
                        </Form>
                        <Form.Select value={newPersonGender} 
                            onChange={(e) => setNewPersonGender(e.target.value)}>
                            <option value="">Choose...</option>
                            <option value="option1">Female</option>
                            <option value="option2">Male</option>
                        </Form.Select>
                        <Form className = 'my-3'>
                            <Form.Control type = "text" placeholder = "Nickname"
                            onChange = {(e) => {setNewPersonNickname(e.target.value)}}/>
                        </Form>
                        <Form className = 'my-3'>
                            <Form.Control as = "textarea" placeholder = "Notes"
                            onChange = {(e) => {setNewPersonNotes(e.target.value)}}
                            style = {{height : '100px', justifyContent : 'flex-start'}}/>
                        </Form>
                    </Modal.Body>
                    <Modal.Footer>
                        <Button variant = "secondary" onClick = {handleAddPersonModalClose}>
                            Cancel
                        </Button>
                        <Button variant = "primary" onClick = {handleAddPerson}>
                            Add Person
                        </Button>
                    </Modal.Footer>
            </Modal>
            <AppBar setLoggedIn = {setLoggedIn}
                    showTreeBuilder = {true}
                    setShowTreeBuilder = {setTreeBuilder}
                    handleDeleteTree = {() => {setShowDeleteModal(true)}}/>
            <p className = 'ms-3 mt-3 treeTitle'>
                {treeTitle}
            </p>
            <div className = 'm-3 node node-woman node-infocus' 
                onClick={handleAddPersonClick}>
                Add Person
            </div>
        </React.Fragment>
    );
};

export default TreeBuilder;

