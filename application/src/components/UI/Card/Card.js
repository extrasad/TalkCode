import React from 'react';
import classes from './Card.css';

const card = (props) => (
  <div className={classes.Card}>
    <div>{props.children}</div>
  </div> 
)

export default card;