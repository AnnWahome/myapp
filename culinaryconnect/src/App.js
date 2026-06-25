import Pages from "./pages/Pages";
import Category from "./components/Category"
import {BrowserRouter} from "react-router-dom"
import Search from "./components/Search"
import { Link } from "react-router-dom";
import styled from "styled-components";
import { GiKnifeFork } from "react-icons/gi";
import { useState, useEffect } from 'react'
import LoginModal from './components/LoginModal'


function App() {
  const [showLogin, setShowLogin] = useState(false)
  const [isLoggedIn, setIsLoggedIn] = useState(false)

  useEffect(() => {
    const username = localStorage.getItem('username')
    setIsLoggedIn(!!username)
  }, [])

  const handleLogout = () => {
    localStorage.removeItem('username')
    setIsLoggedIn(false)
    // We can't use useNavigate here (hook), so we'll navigate using window.location
    window.location.href = '/'
  }

  const handleLoginSuccess = () => {
    setIsLoggedIn(true)
    setShowLogin(false)
  }

  return (
    <div className="bg">
      <BrowserRouter>
        <Nav>
          <GiKnifeFork />
          <Logo to={'/'}>Culinary-Connect</Logo>
          <div style={{marginLeft:'auto'}}>
            {isLoggedIn ? (
              <button onClick={handleLogout}>Logout</button>
            ) : (
              <button onClick={()=>setShowLogin(true)}>Login</button>
            )}
          </div>
        </Nav>
        <Search />
        <Category />
        <Pages />
        {showLogin && <LoginModal onClose={()=>setShowLogin(false)} onLoginSuccess={handleLoginSuccess} />}
      </BrowserRouter>
    </div>
  );
}


const Logo = styled(Link)`
  text-decoration: none;
  font-size: 1.5rem;
  font-weight: 400;
  
`
const Nav = styled.div`
  padding: 4rem 0rem;
  display: flex;
  justify-content: flex-start;
  align-item: center
  svg{
    font-size:2rem;
  }
`

export default App;
