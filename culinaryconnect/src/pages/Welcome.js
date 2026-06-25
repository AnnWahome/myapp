import React from 'react'
import styled from 'styled-components'

function Welcome(){
  const username = localStorage.getItem('username') || 'Guest'
  return (
    <Wrap>
      <h2>Welcome, {username}</h2>
    </Wrap>
  )
}

const Wrap = styled.div`
  padding: 3rem;
  h2{font-size:2rem}
`

export default Welcome
