import logo from './logo.svg';
import './App.css';
import Keycloak from "keycloak-js";
import {useEffect, useState} from 'react';
import axios from 'axios';

let keycloak_options = {
  url: 'http://localhost:8080',
  realm: 'master',
  clientId: 'vot-web-service'
}

let keycloak = new Keycloak(keycloak_options)

keycloak.init({
  onLoad: "login-required",
  checkLoginIframe: false,
  pkceMethod: "S256"
}).then((auth) => {
  if(!auth) {
    window.location.reload();
  } else {
    console.log("Access token: ", keycloak.token)
  }
}, () => {
  console.log("Authentication error")
  console.log(keycloak)
})

function App() {
  const [responseBody, setResponseBody] = useState([{}])

  useEffect(() => {
    axios.post("http://localhost:5000/", {
      headers: {
        "Authorization": `Bearer ${keycloak.token}`
      }
    }).then(response => {
      setResponseBody(response.data);
    })
  }, [])

  return (
    <>
      Hello, {responseBody.body}
    </>
  );
}

export default App;
