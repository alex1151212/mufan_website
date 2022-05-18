import useAuth from "../hook/useAuth";

import { Outlet, useLocation, Navigate } from "react-router-dom";

import { useEffect } from "react";


const RequireAuth = ({allowedRoles}) => {
    const {auth} = useAuth();

    // const location = useLocation();

    return (
        auth?.roles.find(role=> allowedRoles?.includes(role))
        ? <Outlet/>
        : auth?.user
            ?<Navigate to="/unauthorized" replace/>
            :<Navigate to="/login" replace/>
    )
}

export default RequireAuth;