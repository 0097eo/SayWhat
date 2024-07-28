import React from 'react'
import { NavLink } from 'react-router-dom'
import './NavBar.css'  // Import the CSS file

const NavBar = () => {
  return (
    <div className='navbar'>
      <h1>SayWhat</h1>
      <ul>
        <li>
          <NavLink to='/' className={({isActive}) => isActive ? 'home active' : 'home'}>Home</NavLink>
        </li>
        <li>
          <NavLink to='/about' className={({isActive}) => isActive ? 'about active' : 'about'}>About</NavLink>
        </li>
      </ul>
    </div>
  )
}

export default NavBar