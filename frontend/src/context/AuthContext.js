import React, { createContext, useEffect, useState } from "react";
import axios from '../api/axios';

export const AuthContext = createContext();

export const AuthProvider = (props) => {
    const [token, setToken] = useState("");

    useEffect(() => {
        // console.log(token)
        const fetchUser = async () => {

            const response = await axios.get('/user/me',
                {
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: "Bearer " + token?.accessToken
                    },
                }
            ).then((response => {
                if (!response) {
                    setToken(null)
                }
                localStorage.setItem("OauthToken", token?.accessToken);
            }))




            
        };

        fetchUser().then(localStorage.setItem("OauthToken", token));
        console.log(token?.roles);
        console.log(token?.accessToken);
        console.log(token)
    }, [token]);

    return (
        <AuthContext.Provider value={[token, setToken]}>
            {props.children}
        </AuthContext.Provider>
    )

}


// axios.post(REGISTER_URL,
//     JSON.stringify({ username:user, password:pwd }),
//     {
//         headers: { 'Content-Type': 'application/json' },
//         withCredentials: true
//     }
// );