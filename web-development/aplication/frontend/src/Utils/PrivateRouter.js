import React from 'react';
import { Redirect, Route } from 'react-router-dom';

import { HasPermission } from './Utils';
import { Store } from '../Redux/Store';

const PrivateRouter = ({ component: Component, ...rest }) => {

    const handleSuccess = () => {
        return <Route {...rest} render={props => (<Component {...props} />)} />
    };

    const handleError = () => {
        localStorage.removeItem('token');
        Store.dispatch({ type: 'IS_USER_LOGGEDIN', payload: false });
        return <Route {...rest} render={props => (<Redirect to={{ pathname: '/login', state: { from: props.location } }} />)} />
    };
    
    if (rest['permissions']) {
        if (HasPermission(rest['permissions'])) {
            return handleSuccess();
        }
    }

    return handleError();
};

export default PrivateRouter;