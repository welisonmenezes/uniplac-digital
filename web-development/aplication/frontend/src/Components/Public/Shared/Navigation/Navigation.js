import React, { Component } from 'react';
import { Link } from 'react-router-dom';

class Navigation extends Component {

    render() {
        return (
            <nav className="navbar navbar-expand-lg navbar-light bg-light">
                <Link to="/">
                    <span className="navbar-brand">Navbar</span>
                </Link>
                <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>

                <div className="collapse navbar-collapse" id="navbarSupportedContent">
                    <ul className="navbar-nav mr-auto">
                        <li className="nav-item">
                            <Link to="/">
                                <span className="nav-link">Home</span>
                            </Link>
                        </li>
                        <li className="nav-item">
                            <Link to="/not-found">
                                <span className="nav-link">NotFound</span>
                            </Link>
                        </li>
                        <li className="nav-item">
                            <Link to="/admin">
                                <span className="nav-link">Admin</span>
                            </Link>
                        </li>
                        <li className="nav-item">
                            <Link to="/login">
                                <span className="nav-link">Login</span>
                            </Link>
                        </li>
                    </ul>
                </div>
            </nav>
        );
    }

}

export default Navigation;
