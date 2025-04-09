import './TreeBuilder.css';
import AddRelationship from './AddRelationship';
import React, { useState, useRef, useEffect } from 'react';
import { Button, Card } from 'react-bootstrap';
import AppBar from './AppBar';
import Modal from 'react-bootstrap/Modal';
import Form from 'react-bootstrap/Form';
import { Container, Row, Col } from 'react-bootstrap';

const TreeBuilder = ({ treeTitle, setTreeBuilder, setLoggedIn, getUsername }) => {

    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const [showDeletePersonModal, setShowDeletePersonModal] = useState(false);
    const [showAddPersonModal, setShowAddPersonModal] = useState(false);
    const [showModifyPersonModal, setShowModifyPersonModal] = useState(false);
    const [showAddRelationship, setShowAddRelationship] = useState(() => {
            const showAddRel = localStorage.getItem('showAddRelationship') === "true";
            return showAddRel;
        });
    const [newPersonName, setNewPersonName] = useState('');
    const [newPersonGender, setNewPersonGender] = useState('');
    const [newPersonNickname, setNewPersonNickname] = useState('');
    const [newPersonNotes, setNewPersonNotes] = useState('');

    //TODO: set to the initial in-focus person with an API call from back-end
    const [currPersonName, setCurrPersonName] = useState('D');
    const [currPersonGender, setCurrPersonGender] = useState('female');
    const [currPersonNickname, setCurrPersonNickname] = useState('In-Focus');
    const [currPersonNotes, setCurrPersonNotes] = useState('The best in the world');
    const [currPersonID, setCurrPersonID] = useState('3');

    const [showModifyNodeModal, setShowModifyNodeModal] = useState(false);
    const [clickedCoordinates, setClickedCoordinates] = useState([0,0]);

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
            {person : {name : "A", gender : "male", nickname : "Man", notes : "", id : 0}, in_focus : false},
             {},
             {person : {name : "B", gender : "female", nickname : "Woman", notes : "", id : 1}, in_focus : false},
             {},{}], 
             1 : [
             {person : {name : "C", gender : "male", nickname : "", notes : "", id : 2}, in_focus : false},
             {},
             {person : {name : "D", gender : "female", nickname : "In-Focus", notes : "An example of a really long set of notes so it's super long so I can see what happens when the notes are really long.", id : 3}, in_focus : true},
             {},
             {person : {name : "E", gender : "male", nickname : "", notes : "", id : 4}, in_focus : false},
             {},
             {person : {name : "F", gender : "male", nickname : "", notes : "", id : 5}, in_focus : false}
             ], 
             2 : [{},
             {person : {name : "G", gender : "female", nickname : "", notes : "", id : 6}, in_focus : false},
             {},{},{},{},{}
             ]});
    // const [familyTree, setFamilyTree] = useState({});

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

        //TODO: add a person
    }

    const handleNodeClick = (e) => {
        // console.log(e.target.getAttribute("data-name"));
        // console.log(e.target.getAttribute("data-in-focus"))
        // console.log(e.target.getAttribute("data-row"));
        // console.log(e.target.getAttribute("data-col"));

        //set clicked coordinates
        setClickedCoordinates([e.target.getAttribute("data-row"), e.target.getAttribute("data-col")]);

        //if node is not in focus, make it in focus
        if (e.target.getAttribute("data-in-focus") !== "true") {
            console.log("TODO: back-end will make this in focus");
            //call back-end function, which will return a new tree to render:
                // get in-focus node (+ row in tree) from the database
                // remove old in-focus from database
                // add new in-focus to database
                // use row # and name to find the new in-focus and change locally

            //TODO: call back-end to retrieve in-focus person and set state 
                // variables to match
        } else {
            //if node is already in focus, show modal
            setShowModifyNodeModal(true);
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

    const handleDeletePerson = () => {
        // delete the person from the database
        fetch("http://localhost:5002/api/delete_person", {
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
                console.error("Error deleting person:", data.message);
                alert("Failed to delete tree. Please try again.");
            } else {
                setShowDeletePersonModal(false);
            }
        })
        .catch((error) => {
            console.error("Error deleting tree:", error);
            alert("Failed to delete tree. Please try again.");
        });
    }

    const handleModifyPerson = () => {
        //for now (before back-end):
        console.log("ID: " + currPersonID);
        console.log("Name: " + currPersonName);
        console.log("Nickname: " + currPersonNickname);
        console.log("Gender: " + currPersonGender);
        console.log("Notes: " + currPersonNotes);


        //TODO: call back-end function to modify person

        //TODO: get tree from database and set familyTree

        setShowModifyPersonModal(false)
    }

    return (
        showAddRelationship ?
            <AddRelationship setShowAddRelationship = {() => {
                localStorage.setItem("showAddRelationship", "false");
                setShowAddRelationship(false);
            }}
            setShowModifyNodeModal = {() => {
                setShowModifyNodeModal(false);
            }}
            person = {{ name: currPersonName, gender: currPersonGender,
                 nickname: currPersonNickname, notes: currPersonNotes, id: currPersonID}}/> : 
            <React.Fragment>
                <Modal show = {showDeleteModal} onHide = {() => {setShowDeleteModal(false)}}>
                    <Modal.Header closeButton>
                    <Modal.Title>
                        Are you sure?
                    </Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        Are you sure you want to delete "{treeTitle}" and all of its data? This is irreversible.
                    </Modal.Body>
                    <Modal.Footer>
                        <Button variant = "secondary" onClick = {() => {setShowDeleteModal(false)}}>
                            Cancel
                        </Button>
                        <Button variant = "primary" onClick = {handleDeleteTree} 
                        style = {{backgroundColor : "crimson", borderColor : "crimson"}}>
                            Delete Tree
                        </Button>
                    </Modal.Footer>
                </Modal>
                <Modal show = {showDeletePersonModal} onHide = {() => {setShowDeletePersonModal(false)}}>
                    <Modal.Header closeButton>
                    <Modal.Title>Are you sure?</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>Are you sure you want to delete {" "}
                        { familyTree?.[clickedCoordinates?.[0]]?.[clickedCoordinates?.[1]]?.person?.name ?? "this person" } {" "}
                        and all of their data? This is irreversible.</Modal.Body>
                    <Modal.Footer>
                        <Button variant = "secondary" onClick = {() => {setShowDeletePersonModal(false)}}>
                            Cancel
                        </Button>
                        <Button variant = "primary" onClick = {handleDeletePerson} style = {{backgroundColor : "crimson", borderColor : "crimson"}}>
                            Delete Person
                        </Button>
                    </Modal.Footer>
                </Modal>
                <Modal show = {showModifyNodeModal} onHide = {() => {setShowModifyNodeModal(false)}}>
                    <Modal.Header className="d-flex justify-content-between align-items-center">
                        <Modal.Title> {familyTree?.[clickedCoordinates?.[0]]?.[clickedCoordinates?.[1]]?.person?.name ?? ""} </Modal.Title>
                        <div className="d-flex align-items-center">
                            <Button variant = "light" onClick={() => {
                                setShowModifyPersonModal(true);
                                setShowModifyNodeModal(false);
                                }}
                                 className="me-2">
                                <svg xmlns = "http://www.w3.org/2000/svg" width = "20" height = "20" viewBox = "0 0 24 24">
                                <path fill = "none" stroke = "currentColor"
                                d = "M21.174 6.812a1 1 0 0 0-3.986-3.987L3.842 16.174a2 2 0 0 0-.5.83l-1.321 4.352a.5.5 0 0 0 .623.622l4.353-1.32a2 2 0 0 0 .83-.497zM15 5l4 4"/></svg>
                            </Button>
                            <Button variant = "light" onClick = {() => {setShowModifyNodeModal(false)}} style={{ border: "none"}}>
                                ✖
                            </Button>
                        </div>
                    </Modal.Header>
                    <Modal.Body style={{ whiteSpace: "pre-wrap", overflowY: "auto", maxHeight: "70vh" }}>
                        <p><strong>Nickname:</strong> {familyTree?.[clickedCoordinates?.[0]]?.[clickedCoordinates?.[1]]?.person?.nickname ?? ""}</p>
                        <p><strong>Notes:</strong></p>
                        <p>{familyTree?.[clickedCoordinates?.[0]]?.[clickedCoordinates?.[1]]?.person?.notes ?? ""}</p>
                    </Modal.Body>
                    <Modal.Footer className = "d-flex justify-content-between">
                        <Button variant = "secondary" onClick = {() => setShowModifyNodeModal(false)}>
                            Cancel
                        </Button>
                        <Button onClick = {() => {
                            setShowModifyNodeModal(false);
                            setShowDeletePersonModal(true);
                        }} style = {{backgroundColor: "crimson", borderColor: "crimson"}}>
                            Delete Person
                        </Button>
                        <Button onClick={() => {
                            setShowAddRelationship(true);
                            localStorage.setItem("showAddRelationship", "true");
                            }} style = {{ backgroundColor: "steelblue", borderColor: "steelblue" }}>
                            Add Relationship
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
                    <Modal.Footer className = "d-flex justify-content-between">
                        <Button variant = "secondary" onClick = {handleAddPersonModalClose}>
                            Cancel
                        </Button>
                        <Button variant = "primary" onClick = {handleAddPerson}>
                            Add Person
                        </Button>
                    </Modal.Footer>
                </Modal>
                <Modal show = {showModifyPersonModal} onHide = {() => {setShowModifyPersonModal(false)}}>
                    <Modal.Header closeButton>
                        <Modal.Title>Modify {" "} {familyTree?.[clickedCoordinates?.[0]]?.[clickedCoordinates?.[1]]?.person?.name ?? "Person"}</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <Form className = 'my-3'>
                            <Form.Control type = "text" placeholder = "Name" 
                            value = {currPersonName}
                            onChange = {(e) => {setCurrPersonName(e.target.value)}}/>
                        </Form>
                        <Form.Select value = {currPersonGender} 
                            onChange={(e) => setCurrPersonGender(e.target.value)}>
                            <option value = "">Choose...</option>
                            <option value = "female">Female</option>
                            <option value = "male">Male</option>
                        </Form.Select> 
                        <Form className = 'my-3'>
                            <Form.Control type = "text" placeholder = "Nickname"
                            value = {currPersonNickname}
                            onChange = {(e) => {setCurrPersonNickname(e.target.value)}}/>
                        </Form>
                        <Form className = 'my-3'>
                            <Form.Control as = "textarea" placeholder = "Notes"
                            value = {currPersonNotes}
                            onChange = {(e) => {setCurrPersonNotes(e.target.value)}}
                            style = {{height : '100px', justifyContent : 'flex-start'}}/>
                        </Form>
                    </Modal.Body>
                    <Modal.Footer className = "d-flex justify-content-between">
                        <Button variant = "secondary" onClick = {() => {setShowModifyPersonModal(false)}}>
                            Cancel
                        </Button>
                        <Button variant = "primary" onClick = {handleModifyPerson}
                        style = {{ backgroundColor: "steelblue", borderColor: "steelblue" }}>
                            Save
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
                                            onClick = {handleNodeClick}
                                            data-name = {row[colIndex].person.name}
                                            data-in-focus = {row[colIndex].in_focus}
                                            data-row = {rowIndex}
                                            data-col = {colIndex}
                                            data-id = {row[colIndex].id}
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

