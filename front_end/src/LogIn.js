import './Login.css';
import React, { useState } from 'react';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';

const LogIn = ({ setLoggedIn }) => {
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
                    }}/>
                </Form>
                <Form className = 'mt-1 mb-2'>
                    <Form.Control type = 'password' id = 'pwdFrm' placeholder = 'password'
                    onKeyDown={(e) => {
                        if (e.key === "Enter") {
                            e.preventDefault();
                            document.getElementById("loginBtn").focus();
                        }
                    }}/>
                </Form>
                <Button id = 'loginBtn' className = 'mt-2' variant="light" onClick={() => {setLoggedIn()}}>
                    sign in
                </Button>
            </header>
    </div>
    );
};

export default LogIn;

