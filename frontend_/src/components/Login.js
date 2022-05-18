import { useEffect, useState } from "react";
import axios from '../api/axios';

import { Link, useNavigate} from 'react-router-dom';

const LOGIN_URL = "/login";

const Login = () => {

    const navigate = useNavigate();
    // const location = useLocation();

    const [user, setUser] = useState();
    const [pwd, setPwd] = useState();

    useEffect(() => {
        // console.log(JSON.stringify(`grant_type=&username=${user}&password=${pwd}&scope=&client_id=&client_secret=`));
    }, []);

    const OnSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await axios.post(
                LOGIN_URL,
                JSON.stringify(`grant_type=&username=${user}&password=${pwd}&scope=&client_id=&client_secret=`),
                {
                    header: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    withCredentials: true
                }
            );
            console.log(response?.data.roles);
            
            navigate("/")
        }
        catch(err) {
            console.log(err);
        }
    }

    return (
        <section>
            <h1>Sign In</h1>
            <form onSubmit={OnSubmit}>
                <label htmlFor="username">Username:</label>
                <input
                    type="text"
                    id="username"
                    onChange={(e)=> setUser(e.target.value)}
                    required
                />
                <br />
                <label htmlFor="password">Password:</label>
                <input
                    type="text"
                    id="password"
                    onChange={(e)=> setPwd(e.target.value)}
                    required
                />
                <br />
                <button>Sign In</button>
            </form>
            <p>
                Need an Account?<br />
                <span className="">
                    <Link to="/register">Sign Up</Link>
                </span>
            </p>
        </section>


    );
}

export default Login;