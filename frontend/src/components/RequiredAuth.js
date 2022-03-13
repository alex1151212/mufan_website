import { useLocation, Navigate, Outlet } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";
import { useContext } from "react";

const RequireAuth = ({ allowedRoles }) => {
    const [token,] = useContext(AuthContext);
    const location = useLocation();
    // ?.find(role => allowedRoles?.includes(role))
    console.log(token?.roles.find(role => allowedRoles?.includes(role)))
    return (
        token?.roles?.find(role => allowedRoles?.includes(role))
            ?<Outlet />
            : token?.user
                ? <Navigate to="/unauthorized" state={{ from: location }} replace />
                : <Navigate to="/login" state={{ from: location }} replace />
    );
}

export default RequireAuth; 