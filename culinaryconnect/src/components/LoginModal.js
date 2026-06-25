import React, {useState} from 'react'
import styled from 'styled-components'
import { useNavigate } from 'react-router-dom'

function LoginModal({onClose, onLoginSuccess}){
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const navigate = useNavigate()

  async function submit(e){
    e.preventDefault()
    setError(null)
    if(!username || !password){
      setError('Username and password required')
      return
    }
    setLoading(true)
    try{
      const res = await fetch('/api/login', {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({username, password})
      })
      const data = await res.json()
      if(res.ok && data.success){
        localStorage.setItem('username', data.user.username)
        if(onLoginSuccess){
          onLoginSuccess()
        }
        navigate('/welcome')
        onClose()
      } else {
        setError(data.message || 'Login failed')
      }
    }catch(err){
      setError('Network error')
    }finally{
      setLoading(false)
    }
  }

  return (
    <Overlay>
      <Dialog>
        <h3>Login</h3>
        <form onSubmit={submit}>
          <label>Username</label>
          <input value={username} onChange={(e)=>setUsername(e.target.value)} />
          <label>Password</label>
          <input type="password" value={password} onChange={(e)=>setPassword(e.target.value)} />
          {error && <Error>{error}</Error>}
          <div style={{display:'flex', gap:8, marginTop:12}}>
            <button type="submit" disabled={loading}>{loading? 'Logging in...':'Login'}</button>
            <button type="button" onClick={onClose}>Cancel</button>
          </div>
        </form>
      </Dialog>
    </Overlay>
  )
}

const Overlay = styled.div`
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  display:flex;
  align-items:center;
  justify-content:center;
  z-index:1000;
`
const Dialog = styled.div`
  background: #fff;
  padding: 24px;
  border-radius: 8px;
  width: 320px;
  form{display:flex;flex-direction:column}
  input{padding:8px;margin-top:6px;border:1px solid #ddd;border-radius:4px}
  button{padding:8px 12px}
`
const Error = styled.div`
  color: #b00020;
  margin-top:8px;
`

export default LoginModal
