import { useRef, useState, useEffect, useContext } from 'react'
import { Link ,useNavigate,useLocation} from "react-router-dom";
import { AuthContext } from '../context/AuthContext';
import axios from '../api/axios';
const LOGIN_URL = '/login';

const Login = () => {
    const userRef = useRef();
    const errRef = useRef();

    const [user, setUser] = useState('');
    const [pwd, setPwd] = useState('');
    const [errMsg, setErrMsg] = useState('');
    const[token,setToken] = useContext(AuthContext);


    const navigate = useNavigate();
    const location = useLocation();
    const from = location.state?.from?.pathname || "/";

    useEffect(() => {
        userRef.current.focus();
    }, [])

    useEffect(() => {
        setErrMsg('');
    }, [user, pwd])

    const handleSubmit = async (e) => {
        e.preventDefault();

        console.log(user, pwd);

        try {
            const response = await axios.post(LOGIN_URL,
                JSON.stringify(`grant_type=&username=${user}&password=${pwd}&scope=&client_id=&client_secret=`),
                {
                    header: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    withCredentials: true
                }
            );
            console.log(JSON.stringify(response?.data))

            const accessToken = response?.data?.access_token;
            // const roles = response?.data?.roles;
            setToken(accessToken);
            // console.log(response.data);
            // console.log(response.data.user)
            
            setUser('');
            setPwd("");
            navigate(from, { replace: true });
            console.log(location);
            
        } catch (err) {
            if(!err?.response){
                setErrMsg('No Server Response');
            }else if (err.response?.status === 400){
                setErrMsg('Missing Username or Password');
            }else if (err.response?.status === 401){
                setErrMsg('Unauthorized');
            }else {
                setErrMsg('Login Failed');
            }
            errRef.current.focus();
        }

    }

    return (
                <section>
                    <p ref={errRef} className={errMsg ? "errmsg" :
                        "offscreen"} aria-live="assertive">{errMsg}</p>
                    <h1>Sign In</h1>
                    <form onSubmit={handleSubmit}>
                        <label htmlFor='username'>Username:</label>
                        <input
                            type="text"
                            id="username"
                            ref={userRef}
                            autoComplete="off"
                            onChange={(e) => setUser(e.target.value)}
                            value={user}
                            required
                        />
                        <label htmlFor='password'>Password:</label>
                        <input
                            type="password"
                            id="password"
                            onChange={(e) => setPwd(e.target.value)}
                            value={pwd}
                            required
                        />
                        <button >Sign In</button>
                    </form>
                    <p>
                        Need an Account?<br />
                        <span className='line'>
                            {/*put router link here*/}
                            <Link to='/register'>Sign Up</Link>
                        </span>
                    </p>
                </section>
            )}

export default Login;
