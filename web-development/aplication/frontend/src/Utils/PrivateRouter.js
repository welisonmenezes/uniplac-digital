import React from 'react';
import { Redirect, Route } from 'react-router-dom';

// utils/extras
import IsLoggedIn from './IsLoggedIn';

const PrivateRouter = ({ component: Component, ...rest }) => (
  <Route
    { ...rest }
    render={props =>
      (IsLoggedIn()) ? (
        <Component {...props}></Component>
      ): (
        <Redirect to={{pathname: '/login', state: {from: props.location}}}></Redirect>
      )
    }
    />
);

export default PrivateRouter;