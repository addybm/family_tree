import './Login.css';
import React, { useState } from 'react';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';

const LogIn = ({ setLoggedIn, setNewAccountPage, setUsername }) => {

    // const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const handleLogin = async (event) => {
        // stop page from reloading
        event.preventDefault();
        let username = localStorage.getItem('username')
        
        try {
            const response = await fetch("http://localhost:5002/api/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ username, password }),
            });

            const data = await response.json();
            const status_code = response.status;

            if (response.ok) {
                // successful login
                if (data.message === "User credentials valid") {
                    setLoggedIn()
                }
            } else {
                // invalid login
                console.error("Error logging in:", data.message)
                alert(data.message + " (response " + status_code + ")")
            }
        } catch (error) {
            console.error("Error logging in:", error);
            alert("Login failed. Please try again.");
        }
    };

    return (
        <div className = 'App'>
            <header className = 'App-header'>
                <span className="clarity--tree-line-large"></span>
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
                <Button id = 'loginBtn' className = 'mt-2' variant="light" onClick={handleLogin} style = {{width : '200px'}}>
                    sign in
                </Button>
                <Button id = 'newAcctBtn' className = 'mt-2' variant="light" onClick={() => {setNewAccountPage()}} style = {{width : '200px'}}>
                    create new account
                </Button>
            </header>
    </div>
    );
};

export default LogIn;

