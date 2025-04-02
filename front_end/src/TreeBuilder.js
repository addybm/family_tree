import './TreeBuilder.css';
import React, { useState, useRef, useEffect } from 'react';
import { Button, Card } from 'react-bootstrap';
import AppBar from './AppBar';
import Modal from 'react-bootstrap/Modal';
import Form from 'react-bootstrap/Form';
import { Container, Row, Col } from 'react-bootstrap';

const TreeBuilder = ({ treeTitle, setTreeBuilder, setLoggedIn, getUsername }) => {

    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const [showAddPersonModal, setShowAddPersonModal] = useState(false);
    const [newPersonName, setNewPersonName] = useState('');
    const [newPersonGender, setNewPersonGender] = useState('');
    const [newPersonNickname, setNewPersonNickname] = useState('');
    const [newPersonNotes, setNewPersonNotes] = useState('');

    const nodesRef = useRef({});
    const [lines, setLines] = useState([]);

    const marriages = [
        ['A', 'B'],
        ['C', 'D']
    ];

    const children = [
        ['A','B','D','E','F'],
        ['C','D','G']
    ];

    useEffect(() => {
        const updateLines = () => {
            // Recalculate marriage lines
            const newLines = marriages.map(([fromId, toId]) => {
                const from = nodesRef.current[fromId];
                const to = nodesRef.current[toId];
    
                if (from && to) {
                    const fromRect = from.getBoundingClientRect();
                    const toRect = to.getBoundingClientRect();
    
                    return {
                        x1: fromRect.right,
                        y1: fromRect.top + fromRect.height / 2,
                        x2: toRect.left,
                        y2: toRect.top + toRect.height / 2
                    };
                }
                return null;
            }).filter(line => line !== null);
    
            // Recalculate child lines
            const childLines = children.flatMap(([parentOne, parentTwo, ...childId]) => {
                const parentFirst = nodesRef.current[parentOne];
                const parentSecond = nodesRef.current[parentTwo];
                const childOne = nodesRef.current[childId[0]];
                const lastChild = nodesRef.current[childId[childId.length - 1]];
    
                if (parentFirst && parentSecond) {
                    const oneRect = parentFirst.getBoundingClientRect();
                    const twoRect = parentSecond.getBoundingClientRect();
                    const childOneRect = childOne.getBoundingClientRect();
                    const lastChildRect = lastChild.getBoundingClientRect();

                    let childUpwardsLines = [];
                    childId.forEach(element => {
                        let childElem = nodesRef.current[element];
                        let childRect = childElem.getBoundingClientRect();
                        childUpwardsLines.push({
                            x1: childRect.left + childRect.width / 2,
                            y1: twoRect.bottom + (childOneRect.top - oneRect.bottom) / 2,
                            x2: childRect.left + childRect.width / 2,
                            y2: childRect.top
                        });
                    });
    
                    return [...childUpwardsLines, ...[
                        {
                            x1: childOneRect.left + childOneRect.width / 2,
                            y1: twoRect.bottom + (childOneRect.top - oneRect.bottom) / 2,
                            x2: lastChildRect.left + lastChildRect.width / 2,
                            y2: twoRect.bottom + (childOneRect.top - oneRect.bottom) / 2
                        },
                        {
                            x1: oneRect.right + (twoRect.left - oneRect.right) / 2,
                            y1: oneRect.top + oneRect.height / 2,
                            x2: oneRect.right + (twoRect.left - oneRect.right) / 2,
                            y2: twoRect.bottom + (childOneRect.top - oneRect.bottom) / 2
                        },
                    ]];
                }
                return null;
            }).filter(line => line !== null);
    
            const updatedLines = [...newLines, ...childLines];
    
            // **Only update state if lines have changed**
            setLines(prevLines => {
                if (JSON.stringify(prevLines) !== JSON.stringify(updatedLines)) {
                    return updatedLines;
                }
                return prevLines;
            });
        };
    
        // Initial call to update lines
        updateLines();
    
        // Attach event listener to update lines on window resize
        window.addEventListener("resize", updateLines);
    
        // Cleanup function to remove the event listener when component unmounts
        return () => window.removeEventListener("resize", updateLines);
    }, [marriages, children]);


    //dictionary of arrays of Nodes (each Node in dictionary form)
    const [familyTree, setFamilyTree] = useState({
        0 : 
        [{},{},
            {person : {name : "A", gender : "male", nickname : "Man", notes : ""}, in_focus : false},
             {},
             {person : {name : "B", gender : "female", nickname : "Woman", notes : ""}, in_focus : false},
             {},{}], 
             1 : [
             {person : {name : "C", gender : "male", nickname : "", notes : ""}, in_focus : false},
             {},
             {person : {name : "D", gender : "female", nickname : "In-Focus", notes : "test"}, in_focus : true},
             {},
             {person : {name : "E", gender : "male", nickname : "", notes : ""}, in_focus : false},
             {},
             {person : {name : "F", gender : "male", nickname : "", notes : ""}, in_focus : false}
             ], 
             2 : [{},
             {person : {name : "G", gender : "female", nickname : "", notes : ""}, in_focus : false},
             {},{},{},{},{}
             ]});

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

        //add a person
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
            {/* <svg ref = {svgRef} className = "connector-svg" style = {{ position: "absolute", top: 0, left: 0, width: "100%", height: "100%", pointerEvents: "none", zIndex: -1 }}></svg> */}
            <svg style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', pointerEvents: 'none' }}>
                {lines.map((line, index) => (
                    <line key={index} x1={line.x1} y1={line.y1} x2={line.x2} y2={line.y2} 
                        stroke="black" strokeWidth="2" />
                ))}
            </svg>
            {Object.keys(familyTree).length === 0 ?
                <div className = 'm-3 node node-female node-infocus'
                    onClick={handleAddPersonClick}>
                    Add Person
                </div>
                :
                <Container className = "mt-3">
                    {Object.entries(familyTree).map(([rowIndex, row]) => (
                        <Row key = {rowIndex} className = ' justify-content-center'>
                            {[...Array(familyTree[rowIndex].length)].map((_, colIndex) => (
                                <Col key = {colIndex} className = ' d-flex justify-content-center align-items-center'>
                                    {(row[colIndex] && Object.keys(row[colIndex]).length !== 0) ? 
                                        <div ref = {el => nodesRef.current[row[colIndex].person.name] = el}
                                         className = {'m-3 node' + ' node-' + row[colIndex].person.gender + (row[colIndex].in_focus ? ' node-infocus' : '')}>
                                            {row[colIndex].person.nickname !== "" ? row[colIndex].person.nickname : row[colIndex].person.name}
                                        </div>
                                    : 
                                    <div></div>}
                                </Col>
                            ))}
                        </Row>
                    ))}
                </Container>
                }
        </React.Fragment>
    );
};

export default TreeBuilder;

