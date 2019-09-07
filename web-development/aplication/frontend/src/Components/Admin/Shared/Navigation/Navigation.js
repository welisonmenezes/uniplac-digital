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
        localStorage.removeItem('islogged');
        this.props.setUserLogginStatus(false);
        if (/admin*/.test(window.location.pathname)) {
            this.setState({ redirect: true });
        }
    };

    render() {

        console.log(this.props)

        return (
            <nav className="navbar navbar-expand-lg navbar-light bg-light">
                {(this.state.redirect) && <Redirect to="/admin" />}
                <Link to="/admin">
                    <span className="navbar-brand">Navbar</span>
                </Link>
                <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>
                {(this.props.isUserLoggedin) &&
                    <div className="collapse navbar-collapse" id="navbarSupportedContent">
                        <ul className="navbar-nav mr-auto">
                            <li className="nav-item">
                                <NavLink to="/admin" activeClassName="active" exact>
                                    <span className="nav-link">Dashboard</span>
                                </NavLink>
                            </li>
                            <li className="nav-item">
                                <NavLink to="/admin/noticias" activeClassName="active">
                                    <span className="nav-link">Noticias</span>
                                </NavLink>
                            </li>
                            <li className="nav-item">
                                <NavLink to="/admin/avisos" activeClassName="active">
                                    <span className="nav-link">Avisos</span>
                                </NavLink>
                            </li>
                            <li className="nav-item">
                                <NavLink to="/admin/anuncios" activeClassName="active">
                                    <span className="nav-link">Anúncios</span>
                                </NavLink>
                            </li>
                            <li className="nav-item">
                                <NavLink to="/admin/usuarios" activeClassName="active">
                                    <span className="nav-link">Usuários</span>
                                </NavLink>
                            </li>
                            <li className="nav-item">
                                <NavLink to="/admin/configuracoes" activeClassName="active">
                                    <span className="nav-link">Configurações</span>
                                </NavLink>
                            </li>
                            <li className="nav-item">
                                <Link to="/">
                                    <span className="nav-link">Site</span>
                                </Link>
                            </li>
                            <li className="nav-item" onClick={this.handleLogout}>
                                <span className="nav-link">Logout</span>
                            </li>
                        </ul>
                    </div>
                }
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
