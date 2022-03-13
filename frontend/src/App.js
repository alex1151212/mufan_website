

import { useContext } from "react";
import { AuthContext } from "./context/AuthContext";
import React from 'react';

import Layout from "./components/Layout";
import Login from './components/Login';
import Register from './components/Register';
import Home from './components/Home';
import LinkPage from './components/LinkPage';
import RequiredAuth from './components/RequiredAuth';
import Missing from "./components/Missing";
import Unauthorized from "./components/Unauthorized";
import Admin from "./components/Admin"

import { Route, Routes } from "react-router-dom";

const ROLES = {
  'User': "User",
  'Editor':"Editor" ,
  'Admin': "Admin"
}


// import { Routes, Route } from 'react-router-dom';
function App() {
  const [token] = useContext(AuthContext);
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        {/* Public routes */}
        <Route path="register" element={<Register />} />
        <Route path="login" element={<Login />} />
        <Route path="linkpage" element={<LinkPage />} />
        <Route path="unauthorized" element={<Unauthorized/>}/>

        <Route element={<RequiredAuth allowedRoles={[ROLES.User]}/>} >
          <Route path="/" element={<Home />} />
        </Route>

        <Route element={<RequiredAuth allowedRoles={[ROLES.Admin]}/>} >
          <Route path="admin" element={<Admin />} />
        </Route>

        {/* <Route path="*" element={<Missing/>}/> */}

      </Route>
    </Routes>

  );
}

export default App;