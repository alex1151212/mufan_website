import { useEffect, useState } from "react";
import useAxiosPrivate  from "../hook/useAxiosPrivate";
import { Link, useNavigate} from 'react-router-dom';


const Profile_URL = "/profile"

const Profile = () => {

    const navigate = useNavigate();
    const [user, setUser] = useState();
    const axiosPrivate = useAxiosPrivate();

    useEffect(() => {

        const getProfile = async () => {
            try {
                const response = await axiosPrivate.get(Profile_URL);
                console.log(response.data);
                setUser(response.data.username);
                console.log(typeof(response.data));
                
            } catch (err) {
                console.error(err);
                navigate('/login');
            }
        }
        
        getProfile();

        console.log(user);
        
    }, [])

    return (
        <div>
            <h1>Profile Page</h1>
            {user}
        </div>


    );
}

export default Profile;