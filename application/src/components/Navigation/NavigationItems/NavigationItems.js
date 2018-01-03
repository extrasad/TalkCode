import React from 'react';

import classes from './NavigationItems.css';
import NavigationItem from './NavigationItem/NavigationItem';

const navigationItems = (props) => {
  return (
    <ul className={classes.NavigationItems}>
      <NavigationItem link="/" exact>Home</NavigationItem>
      <NavigationItem link="/profile">Profile</NavigationItem>
      <NavigationItem link="/new">New</NavigationItem>
      <NavigationItem link="/auth">Authenticate</NavigationItem>
      <NavigationItem link="/logout">Logout</NavigationItem>
    </ul>
  )
};

export default navigationItems;