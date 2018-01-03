import React from 'react';

import Logo from '../../assets/images/logo.png';
import classes from './Logo.css';

const logo = (props) => (
    <div className={classes.Logo} style={{height: props.height}}>
        <img src={Logo} alt="Talkcode Logo" />
    </div>
);

export default logo;