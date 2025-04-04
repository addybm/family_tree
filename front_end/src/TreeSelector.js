import './TreeSelector.css';
import React, { useEffect, useState } from 'react';
import AppBar from './AppBar';
import { Row, Col, Container } from 'react-bootstrap';
import TreePreview from './TreePreview';
import Modal from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';

const TreeSelector = ({ setLoggedIn, setTreeBuilder, setTreeTitle, getUsername }) => {
    //retrieve the user's trees from the database
    const [loading, setLoading] = useState(true);
    const [treeData, setTreeData] = useState([]);
    const [showModal, setShowModal] = useState(false);
    const [newTreeName, setNewTreeName] = useState('');

    useEffect(() => {
        fetch("http://localhost:5002/api/trees?username=" + getUsername(), {
            method: "GET",
        })
        .then((response) => response.json())
        .then((data) => {
            let to_set = data.tree_names;
            to_set.push('');
            setTreeData(to_set);
            setLoading(false);
        })
        .catch((error) => {
            console.error("Error fetching tree data:", error);
            alert("Failed to fetch tree data. Please try again.");
        });
    }, []);

    const handleCardClick = (index) => {
        //check if clicked on "create tree" card
        if (treeData[index] == '') {
            setShowModal(true);
        } else {
            setTreeBuilder(true);
            setTreeTitle(treeData[index]);

            //modify the "last_opened" field in the database
            fetch("http://localhost:5002/api/modify_last_opened", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ username: getUsername(), tree_name: treeData[index] }),
            })
            .then((response) => {
                return response.json().then((data) => ({ status: response.ok, data }));
            })
            .then(({ status, data }) => {
                if (!status) {
                    console.error("Error updating last opened tree:", data.message);
                    alert("Failed to update last opened tree. Please try again.");
                }
            })
            .catch((error) => {
                console.error("Error updating last opened tree:", error);
                alert("Failed to update last opened tree. Please try again.");
            });
        }
    };

    // decide if a new tree is valid, and create it if yes
    const handleCreateTree = () => {
        // check that a tree name is entered
        if (newTreeName == '') {
            alert("Please enter a tree name.");
            return;
        }

        // add the new tree to the database
        fetch("http://localhost:5002/api/add_tree", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ username: getUsername(), tree_name: newTreeName }),
        })
        .then((response) => {
            return response.json().then((data) => ({ status: response.ok, data }));
        })
        .then(({ status, data }) => {
            if (!status) {
                console.error("Error creating tree:", data.message);
                alert("Failed to create tree. Please try again.");
            } else {
                setShowModal(false);
                setTreeBuilder(true);
                setTreeTitle(newTreeName);
            }
        })
        .catch((error) => {
            console.error("Error creating tree:", error);
            alert("Failed to create tree. Please try again.");
        });
    }

    return (
        loading ?
        <div>
        </div>
        :
        <>
            <Modal show = {showModal} onHide = {() => setShowModal(false)}>
                <Modal.Header closeButton>
                    <Modal.Title>Create Tree</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form>
                        <Form.Control type = "text" placeholder = "Enter Tree Name"
                        onChange = {(e) => {setNewTreeName(e.target.value)}}/>
                    </Form>
                </Modal.Body>
                <Modal.Footer>
                    <Button variant = "secondary" onClick = {() => setShowModal(false)}>Cancel</Button>
                    <Button variant = "primary" onClick = {handleCreateTree}>Create</Button>
                </Modal.Footer>
            </Modal>

            <div className = 'TreeSelector-body'>
                <AppBar setLoggedIn = {setLoggedIn} 
                    showTreeBuilder = {false}
                    setShowTreeBuilder = {()=> {}}
                    handleDeleteTree = {() => {}}/>
                <div>
                    Your Trees:
                </div>
                {treeData.length == 0 ? 
                    <div>
                        <TreePreview pic = {null} title = {null}/>
                    </div>
                    :
                    <Container>
                        <Row className = 'g-4'>
                            {treeData.map((title, index) => (
                                <Col key = {index} sm = {6} md = {5} lg = {4} xl = {2}>
                                    <TreePreview title = {title} idx = {index} handleClick = {handleCardClick}/>
                                </Col>
                            ))}
                        </Row>
                    </Container>}
                </div>
        </>
        
    );
};

export default TreeSelector;

