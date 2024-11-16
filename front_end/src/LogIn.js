import './App.css';
import React, { useState } from 'react';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';

export function PhTreeLight(props) {
	return (<svg xmlns="http://www.w3.org/2000/svg" width="12em" height="12em" viewBox="0 0 256 256" {...props}><path fill="currentColor" d="M196.55 64.09a74 74 0 0 0-137.1 0A69.71 69.71 0 0 0 18 127.8c-.1 37.11 31.13 69.2 68.19 70.2a70.3 70.3 0 0 0 35.81-8.84V232a6 6 0 0 0 12 0v-42.84a70.1 70.1 0 0 0 34 8.84h1.77c37.1-1 68.33-33.1 68.23-70.2a69.71 69.71 0 0 0-41.45-63.71M169.5 186a57.88 57.88 0 0 1-35.5-11v-43.29l44.68-22.34a6 6 0 1 0-5.36-10.74L134 118.29V88a6 6 0 0 0-12 0v54.29l-39.32-19.66a6 6 0 0 0-5.36 10.74L122 155.71V175a58.1 58.1 0 0 1-35.5 11c-30.71-.77-56.58-27.4-56.5-58.14a57.78 57.78 0 0 1 36.37-53.67a6 6 0 0 0 3.39-3.51a62 62 0 0 1 116.48 0a6 6 0 0 0 3.39 3.51A57.77 57.77 0 0 1 226 127.83c.08 30.75-25.79 57.37-56.5 58.17"></path></svg>);
}

const LogIn = ({ setLoggedIn }) => {
    return (
        <div className = 'App'>
            <header className = 'App-header'>
                {PhTreeLight()}
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
                <Button id = 'loginBtn' className = 'mt-2' variant="light" onClick={() => {setLoggedIn(true)}}>
                    sign in
                </Button>
            </header>
    </div>
    );
};

export default LogIn;
