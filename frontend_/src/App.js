import { Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';

//Components
import Login from './components/Login';
import Test from './components/Test';
import RequireAuth from './components/RequireAuth'

const ROLES = {
  'User': "1",
  'Editor': "2",
  'Admin': "3"
}

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route path="login" element={<Login/>} />
        <Route path="test" element={<Test/>} />
        <Route element={<RequireAuth allowedRoles={[ROLES.User]} />}>
            <Route path="/test" element={<Test />} />
        </Route>
      </Route>
    </Routes>
  );
}

export default App;
