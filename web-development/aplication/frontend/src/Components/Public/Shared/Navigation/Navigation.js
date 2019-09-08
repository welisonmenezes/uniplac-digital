import React, { Component } from 'react';
import { Link, Redirect, NavLink } from 'react-router-dom';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';

import { setUserLogginStatus } from '../../../../Redux/Actions/UserActions';

class Navigation extends Component {

    constructor(props) {
        super(props);
        this.state = { redirect: false };
    }

    handleLogout = () => {
        localStorage.removeItem('token');
        this.props.setUserLogginStatus(false);
        if (/admin*/.test(window.location.pathname)) {
            this.setState({redirect: true});
        }
    };

    render() {

        console.log(this.props)

        return (
            <nav className="navbar navbar-expand-lg navbar-light bg-light">
                { (this.state.redirect) && <Redirect to="/admin" /> }
                <Link to="/">
                    <span className="navbar-brand">Navbar</span>
                </Link>
                <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>

                <div className="collapse navbar-collapse" id="navbarSupportedContent">
                    <ul className="navbar-nav mr-auto">
                        <li className="nav-item">
                            <NavLink to="/" activeClassName="active" exact>
                                <span className="nav-link">Home</span>
                            </NavLink>
                        </li>
                        <li className="nav-item">
                            <NavLink to="/noticias" activeClassName="active">
                                <span className="nav-link">Noticias</span>
                            </NavLink>
                        </li>
                        <li className="nav-item">
                            <NavLink to="/avisos" activeClassName="active">
                                <span className="nav-link">Avisos</span>
                            </NavLink>
                        </li>
                        <li className="nav-item">
                            <NavLink to="/anuncios" activeClassName="active">
                                <span className="nav-link">Anúncios</span>
                            </NavLink>
                        </li>
                        { (this.props.isUserLoggedin) && 
                            <li className="nav-item">
                                <Link to="/admin">
                                    <span className="nav-link">Admin</span>
                                </Link>
                            </li>
                        }
                        { (this.props.isUserLoggedin) && 
                            <li className="nav-item" onClick={this.handleLogout}>
                                <span className="nav-link">Logout</span>
                            </li>
                        }
                        { (!this.props.isUserLoggedin) && 
                            <li className="nav-item">
                                <NavLink to="/login" activeClassName="active">
                                    <span className="nav-link">Login</span>
                                </NavLink>
                            </li>
                        }
                    </ul>
                </div>
            </nav>
        );
    }

}

const mapStateToProps = store => ({
    isUserLoggedin: store.userState.isUserLoggedin
});

const mapDispatchToProps = dispatch =>
  bindActionCreators({
    setUserLogginStatus
  }, dispatch);

export default connect(mapStateToProps, mapDispatchToProps)(Navigation);
