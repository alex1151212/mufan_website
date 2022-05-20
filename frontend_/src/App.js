import { Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';

//Components
import Login from './components/Login';
import Test from './components/Test';
import RequireAuth from './components/RequireAuth'
import Unauthorized from './components/Unauthorized';
import Profile from './components/Profile';
const ROLES = {
  'User': "User",
  'Editor': "Editor",
  'Admin': "Admin"
}

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route path="login" element={<Login/>} />
        <Route path="unauthorized" element={<Unauthorized />} />

        <Route element={<RequireAuth allowedRoles={[ROLES.User]} />}>
            <Route path="profile" element={<Profile />} />
            <Route path="test" element={<Test />} />
        </Route>

      </Route>
    </Routes>
  );
}

export default App;
