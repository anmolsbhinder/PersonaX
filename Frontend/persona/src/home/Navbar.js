import React, {useState, useEffect} from 'react';
import logo from '../Resources/logo1.png';
import logoDark from '../Resources/logo copy.svg';
import { Link } from 'react-router-dom';
// import logo from '../Resources/SneakPeek/shoelogo.png';
// import logo2 from '../Resources/SneakPeek/shoelogo2.png';


export default function Navbar() {

  const [navbar,setNavbar] = useState(false);
  const [mx3,setText] = useState(false);

  const changeBackground = () => {
    if(window.scrollY > 80){
      setNavbar(true);
      setText(true);
    }
    else {
      setNavbar(false);
      setText(false);
    }
  }

  window.addEventListener('scroll', changeBackground);

  return (
    // <nav className= {navbar ? 'active' : 'navbar'}>
    <nav className= 'active'>
    <div className="">
      <Link to="/">
      <img className='logo' src={logo} alt='store logo' />
      </Link>
    </div>

    <div>
      <ul className='links-list'>

        <Link to="/" id='nav-links' >
          <li className='links'>Customers</li>
        </Link>

        <Link to="/segment" id='nav-links' >
          <li className='links'>Categories</li>
        </Link>

      </ul>
    </div>
  </nav>
  );
}
