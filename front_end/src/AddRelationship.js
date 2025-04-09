import './AddRelationship.css';
import React, { useEffect, useState } from 'react';
import Button from 'react-bootstrap/Button';
import { Form } from 'react-bootstrap';

const AddRelationship = ({ setShowAddRelationship, setShowModifyNodeModal, person }) => {

    const [loading, setLoading] = useState(true);
    const [newRelationship, setNewRelationship] = useState(() => {
        return localStorage.getItem("newRelationship") ?? "";
    });
    const [coParent, setCoParent] = useState("");
    const [coParentOptions, setCoParentOptions] = useState([]);
    const [relationshipOptions, setRelationshipOptions] = useState(["parent", "child", "partner"]);
    const [newPersonName, setNewPersonName] = useState(() => {
        return localStorage.getItem("newPersonName") ?? "";
    });
    const [newPersonGender, setNewPersonGender] = useState(() => {
        return localStorage.getItem("newPersonGender") ?? "";
    });
    const [newPersonNickname, setNewPersonNickname] = useState(() => {
        return localStorage.getItem("newPersonNickname") ?? "";
    });
    const [newPersonNotes, setNewPersonNotes] = useState(() => {
        return localStorage.getItem("newPersonNotes") ?? "";
    });
    const [parentStatus, setParentStatus] = useState(() => {
        return localStorage.getItem("parentStatus") ?? "";
    });
    const [warningChecked, setWarningChecked] = useState(() => {
        return localStorage.getItem("warningChecked") === "true";
    });
    const [singleChildrenChecks, setSingleChildrenChecks] = useState([]);
    
    //get information about the in-focus person from database
    const [partner, setPartner] = useState({});
    const [formerPartners, setFormerPartners] = useState([]);
    const [parents, setParents] = useState([]);
    const [children, setChildren] = useState([]);
    const [childrenSingleParent, setChildrenSingleParent] = useState([]);
    const [siblings, setSiblings] = useState([]);

    useEffect(() => {
        //TODO gather relationship data from database about the in-focus
            //person we are adding a relationship to instead of hard-coding

        //get partner info (current partner as Person)
        let partner = {name : "C", gender : "male", nickname : "", notes : "", id : 2};
        // let partner = {};
        setPartner(partner);

        //get ex-partner info (previous partner(s) as Person[])
        let formerPartners = [{name : "EX", gender : "female", nickname : "evil", notes : "", id : 7}];
        // let formerPartners = [];
        setFormerPartners(formerPartners);

        let coParentOptionsData = [];
        if (Object.hasOwn(partner, "name")) {
            coParentOptionsData = [partner.name];
        }
        formerPartners.forEach(element => {
            coParentOptionsData.push(element.name);
        });
        setCoParentOptions(coParentOptionsData)

        //get parent info as Person[]
        let parentsData = [{name : "A", gender : "male", nickname : "Man", notes : "", id : 0},
            {name : "B", gender : "female", nickname : "Woman", notes : "", id : 1}];
        // let parentsData = [{name : "A", gender : "male", nickname : "Man", notes : "", id : 0}];
        // let parentsData = [];
        setParents(parentsData);
        if (parentsData.length === 2) {
            setRelationshipOptions(["child", "partner"]);
        }

        //get children info as Person[] in current birth order
        let childrenData = {"C" : [{name : "G", gender : "female", nickname : "", notes : "", id : 6}],
            "null" : [{name : "H", gender : "male", nickname : "", notes : "", id : 8},
            {name : "I", gender : "female", nickname : "", notes : "", id : 9}]};
        setChildren(childrenData);
        // let childrenSingleParentData = [{name : "H", gender : "male", nickname : "", notes : "", id : 8},
        //     {name : "I", gender : "female", nickname : "", notes : "", id : 9}]
        let childrenSingleParentData = [];
        if (Object.hasOwn(childrenData, "null")) {
            childrenSingleParentData = childrenData["null"];
        }
        setChildrenSingleParent(childrenSingleParentData);
        setSingleChildrenChecks(new Array(childrenSingleParentData.length).fill(false))

        //get siblings info as Person[] in birth order
        setSiblings([{name : "E", gender : "male", nickname : "", notes : "", id : 4}, 
            {name : "F", gender : "male", nickname : "", notes : "", id : 5}]);

        setLoading(false);
    },[]);

    const handleSingleChildCheck = (index) => {
        const updatedState = [...singleChildrenChecks];
        updatedState[index] = !updatedState[index];
        setSingleChildrenChecks(updatedState);
    };

    const handleAddPerson = () => {

        //check if warning checkbox needs to be acknowledged
        if (newRelationship === "partner" && Object.hasOwn(partner, "name")) {
            if (!warningChecked) {
                alert("Please acknowledge warning and check box before adding "
                    + "relationship.");
                return
            }
        }

        if (newRelationship === "child" && coParent === "") {
            alert("Please select parent for child (or not listed if parent not in list).")
            return;
        }

        console.log("checks:");
        console.log(singleChildrenChecks);


        //TOOD: add person to database
        setShowModifyNodeModal();
        setShowAddRelationship();
        clearLocalStorage();
    };

    const handleCancel = () => {
        setShowModifyNodeModal();
        setShowAddRelationship();
        clearLocalStorage();
    }
    
    const clearLocalStorage = () => {
        localStorage.setItem("newRelationship", "");
        localStorage.setItem("newPersonName", "");
        localStorage.setItem("newPersonGender", "");
        localStorage.setItem("newPersonNickname", "");
        localStorage.setItem("newPersonNotes", "");
        localStorage.setItem("parentStatus", "");
        localStorage.setItem("warningChecked", "");
    }
   
    return (
        loading ?
        <div>
        </div>
        :
        <React.Fragment>
            <div className = 'd-flex'>
                <div className = 'mx-2 mt-3'>
                    Add a
                </div>
                <Form.Select value = {newRelationship}
                    onChange = {(e) => {
                        setNewRelationship(e.target.value);
                        localStorage.setItem("newRelationship", e.target.value);
                    }}
                    style = {{ width: "125px" }}
                    className = 'm-2'>
                    <option key = "chooseOptionOne" value = "">choose...</option>
                    {relationshipOptions.map((option) => (
                        <option key = {option} value = {option}>
                            {option}
                        </option>
                    ))}
                </Form.Select>
                <div className = 'mx-2 mt-3'>
                    for {person.name}
                </div>
            </div>

            {(newRelationship === "parent") ? 
                parents.length === 1 ? 
                <div className = 'd-flex'>
                    <div className = 'mx-2 mt-3'>
                        {parents[0].name} and this new parent are
                    </div>
                    <Form.Select value = {parentStatus}
                        onChange = {(e) => {
                            setParentStatus(e.target.value);
                            localStorage.setItem("parentStatus", e.target.value);
                        }}
                        style = {{ width: "125px" }}
                        className = 'mt-2'>
                        <option value = ""> choose... </option>
                        <option value = "together"> together. </option>
                        <option value = "separated"> separated. </option>
                    </Form.Select>
                </div>
                 : 
                <div></div>
                :
                newRelationship === "child" ?
                    <React.Fragment>
                        <div className = 'd-flex'>
                            <div className = 'mx-2 my-3'>
                                Other parent is
                            </div>
                            <Form.Select value = {coParent}
                                onChange = {(e) => {
                                    setCoParent(e.target.value);
                                    localStorage.setItem("coParent", e.target.value);
                                }}
                                style = {{ width: "125px" }}
                                className = 'm-2'>
                                <option value = ""> choose... </option>
                                {coParentOptions.map((option) => (
                                    <option key = {option} value = {option}>
                                        {option}.
                                    </option>
                                ))}
                                <option value = "null"> not listed. </option>
                            </Form.Select>
                        </div>
                    </React.Fragment>
                    :
                    newRelationship === "partner" ?
                        <React.Fragment>
                            {Object.hasOwn(partner, "name") ?
                                    <div className = 'd-flex mx-2 my-3'>
                                        <Form.Check 
                                            type = "checkbox"
                                            id = "controlled-checkbox"
                                            label = ""
                                            checked = {warningChecked}
                                            onChange = {(e) => {
                                                setWarningChecked(e.target.checked);
                                                localStorage.setItem("warningChecked", e.target.checked ? "true" : "false");
                                            }}
                                        />
                                        <div>
                                            Warning: please acknowledge adding this partner will separate
                                            {" "} {person.name} from {partner.name}.
                                        </div>
                                    </div>
                                    :
                                    <div></div>}
                            {childrenSingleParent.length !== 0 ?
                                <div className = 'mx-2 my-3'>
                                    <div>
                                        Please select any of {person.name}'s children that are also children of this new person:
                                    </div>
                                    {childrenSingleParent.map((child, index) => (
                                        <Form.Check
                                            type = "checkbox"
                                            id = {"check" + child.id}
                                            label = {child.name}
                                            key = {"childCheck" + child.id}
                                            onChange = {() => {handleSingleChildCheck(index)}}
                                            checked = {singleChildrenChecks[index]}
                                        />
                                    ))}
                                </div> 
                                :
                                <div></div>}
                        </React.Fragment>
                        :
                        <div></div>
                
            }

            <Form className = 'my-3 mx-2' style = {{ width: "250px" }}>
                <Form.Control type = "text" placeholder = "Name"
                onChange = {(e) => {
                    setNewPersonName(e.target.value);
                    localStorage.setItem("newPersonName", e.target.value);
                }}/>
            </Form>

            <Form.Select value = {newPersonGender} 
                onChange={(e) => {
                    setNewPersonGender(e.target.value);
                    localStorage.setItem("newPersonGender", e.target.value);
                }}
                style = {{ width: "250px" }}
                className = 'mx-2'>
                <option value = "">Choose...</option>
                <option value = "option1">Female</option>
                <option value = "option2">Male</option>
            </Form.Select>

            <Form className = 'my-3 mx-2' style = {{ width: "250px" }}>
                <Form.Control type = "text" placeholder = "Nickname"
                onChange = {(e) => {
                    setNewPersonNickname(e.target.value);
                    localStorage.setItem("newPersonNickname", e.target.value);
                }}/>
            </Form>

            <Form className = 'my-3 mx-2' style = {{ width: "250px" }}>
                <Form.Control as = "textarea" placeholder = "Notes"
                onChange = {(e) => {
                    setNewPersonNotes(e.target.value);
                    localStorage.setItem("newPersonNotes", e.target.value);
                }}
                style = {{height : '100px', justifyContent : 'flex-start'}}/>
            </Form>
            
            <Button onClick = {handleCancel}
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

