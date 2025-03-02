import './CreateNewAccount.css';
import React, { useState } from 'react';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';

const CreateNewAccount = ({ setLoggedIn, setNewAccountPage }) => {

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const handleNewAccount = async (event) => {
        // stop page from reloading
        event.preventDefault();
        
        try {
            const response = await fetch("http://localhost:5002/api/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ username, password }),
            });

            const data = await response.json();
            const status_code = response.status;

            if (response.ok) {
                // successful creation
                if (data.message === "User registered successfully") {
                    setLoggedIn()
                    setNewAccountPage()
                }
            } else {
                // invalid login
                console.error("Error creating new account:", data.message)
                alert(data.message + " (response " + ((status_code == 409)
                    ? "\"username already in use\"" : status_code) + ")")
            }
        } catch (error) {
            console.error("Error creating new account:", error);
            alert("Account creation failed. Please try again.");
        }
    };

    return (
        <div className = 'App'>
            <header className = 'App-header'>
                <span class="clarity--tree-line-large"></span>
                <Form className = 'mb-1'>
                    <Form.Control type = 'username' placeholder = 'username' id = 'usnFrm'
                    onKeyDown={(e) => {
                        if (e.key === "Enter") {
                            e.preventDefault();
                            document.getElementById("pwdFrm").focus();
                        }
                    }}
                    onChange = {(e) => {
                        setUsername(e.target.value)
                    }}/>
                </Form>
                <Form className = 'mt-1 mb-2'>
                    <Form.Control type = 'password' id = 'pwdFrm' placeholder = 'password'
                    onKeyDown={(e) => {
                        if (e.key === "Enter") {
                            e.preventDefault();
                            document.getElementById("loginBtn").focus();
                        }
                    }}
                    onChange = {(e) => {
                        setPassword(e.target.value)
                    }}/>
                </Form>
                <Button id = 'newAcctBtn' className = 'mt-2' variant = "light" onClick={handleNewAccount} 
                    style = {{width : '200px'}}>
                    create account
                </Button>
                <Button id = 'newAcctBtn' className = 'mt-2' onClick={() => {setNewAccountPage()}}
                    style = {{width : '200px', background : '#282c34', border : '#282c34'}}>
                    cancel
                </Button>
            </header>
    </div>
    );
};

export default CreateNewAccount;