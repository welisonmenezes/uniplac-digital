import React, { Component } from 'react';
import { Switch, Route } from 'react-router-dom';
import { TransitionGroup, CSSTransition } from "react-transition-group";

import Navigation from './Shared/Navigation/Navigation';

import Home from './Home/Home';
import NotFound from './NotFound/NotFound';
import Posts from './Posts/Posts';
import Post from './Posts/Post/Post';

import Login from '../Admin/Login/Login';

class Public extends Component {

    render() {
        return (
            <div className="Public">
                <Navigation></Navigation>
                <Route render={({ location }) => (
                    <TransitionGroup>
                        <CSSTransition key={location.key} classNames="fade" timeout={300} transitionAppear={true} transitionEnter={false} transitionLeave={false}>
                            <Switch location={location}>
                                <Route path="/" exact={true} component={Home} />
                                <Route path="/noticias" exact={true} component={Posts} />
                                <Route path="/noticias/:id" exact={true} component={Post} />
                                <Route path="/anuncios" exact={true} component={Posts} />
                                <Route path="/anuncios/:id" exact={true} component={Post} />
                                <Route path="/avisos" exact={true} component={Posts} />
                                <Route path="/avisos/:id" exact={true} component={Post} />
                                <Route path='/login' exact={true} component={Login} />
                                <Route path='*' component={NotFound} />
                            </Switch>
                        </CSSTransition>
                    </TransitionGroup>
                )} />
            </div>
        );
    }
}

export default Public;
