import React, { Component } from 'react';
import { Collapse } from 'reactstrap';
//import { Link, Redirect, NavLink } from 'react-router-dom';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';

import './Navigation.css';

import { setUserLogginStatus } from '../../../../Redux/Actions/UserActions';

class Navigation extends Component {

    constructor(props) {
        super(props);
        this.state = {
            redirect: false,
            menuStatus: {
                news: false,
                ads: false,
                novices: false,
                users: false,
                categories: false,
                configurations: false
            }
        };
    }

    toggle = (item) => {
        let obj = { menuStatus: {
            news: false,
            ads: false,
            novices: false,
            users: false,
            categories: false,
            configurations: false
        } };
        obj.menuStatus[item] = !this.state.menuStatus[item];
        this.setState({ menuStatus: obj.menuStatus });
    }

    render() {

        return (
            <nav className="Navigation sidebar sidebar-offcanvas" id="sidebar">
                <ul className="nav">
                    <li className="nav-item">
                        <a className="nav-link" href="index.html">
                            <i className="mdi mdi-home menu-icon"></i>
                            <span className="menu-title">Dashboard</span>
                        </a>
                    </li>
                    <li className="nav-item">
                        <span className="nav-link" onClick={() => { this.toggle('news') }}>
                            <i className="mdi mdi-newspaper menu-icon"></i>
                            <span className="menu-title">Notícias</span>
                            <i className="menu-arrow"></i>
                        </span>
                        <Collapse isOpen={this.state.menuStatus.news}>
                            <ul className="nav flex-column sub-menu">
                                <li className="nav-item">
                                    <a className="nav-link" href="news.html">Ver todos</a>
                                </li>
                                <li className="nav-item">
                                    <a className="nav-link" href="post-form.html">Adicionar Novo</a>
                                </li>
                            </ul>
                        </Collapse>
                    </li>
                    <li className="nav-item">
                        <span className="nav-link" onClick={() => { this.toggle('ads') }}>
                            <i className="mdi mdi-bullhorn menu-icon"></i>
                            <span className="menu-title">Anúncios</span>
                            <i className="menu-arrow"></i>
                        </span>
                        <Collapse isOpen={this.state.menuStatus.ads}>
                            <ul className="nav flex-column sub-menu">
                                <li className="nav-item">
                                    <a className="nav-link" href="ads.html">Ver todos</a>
                                </li>
                                <li className="nav-item">
                                    <a className="nav-link" href="post-form.html">Adicionar Novo</a>
                                </li>
                            </ul>
                        </Collapse>
                    </li>
                    <li className="nav-item">
                        <span className="nav-link" onClick={() => { this.toggle('novices') }}>
                            <i className="mdi mdi-sim-alert menu-icon"></i>
                            <span className="menu-title">Avisos</span>
                            <i className="menu-arrow"></i>
                        </span>
                        <Collapse isOpen={this.state.menuStatus.novices}>
                            <ul className="nav flex-column sub-menu">
                                <li className="nav-item">
                                    <a className="nav-link" href="novices.html">Ver todos</a>
                                </li>
                                <li className="nav-item">
                                    <a className="nav-link" href="post-form.html">Adicionar Novo</a>
                                </li>
                            </ul>
                        </Collapse>
                    </li>
                    <li className="nav-item">
                        <span className="nav-link" onClick={() => { this.toggle('users') }}>
                            <i className="mdi mdi-account menu-icon"></i>
                            <span className="menu-title">Usuários</span>
                            <i className="menu-arrow"></i>
                        </span>
                        <Collapse isOpen={this.state.menuStatus.users}>
                            <ul className="nav flex-column sub-menu">
                                <li className="nav-item">
                                    <a className="nav-link" href="users.html">Ver todos</a>
                                </li>
                                <li className="nav-item">
                                    <a className="nav-link" href="user-form.html">Adicionar Novo</a>
                                </li>
                            </ul>
                        </Collapse>
                    </li>
                    <li className="nav-item">
                        <span className="nav-link" onClick={() => { this.toggle('categories') }}>
                            <i className="mdi mdi-tag menu-icon"></i>
                            <span className="menu-title">Categorias</span>
                            <i className="menu-arrow"></i>
                        </span>
                        <Collapse isOpen={this.state.menuStatus.categories}>
                            <ul className="nav flex-column sub-menu">
                                <li className="nav-item">
                                    <a className="nav-link" href="categories.html">Ver todas</a>
                                </li>
                                <li className="nav-item">
                                    <a className="nav-link" href="category-form.html">Adicionar Novo</a>
                                </li>
                            </ul>
                        </Collapse>
                    </li>
                    <li className="nav-item">
                        <span className="nav-link" onClick={() => { this.toggle('configurations') }}>
                            <i className="mdi mdi-settings menu-icon"></i>
                            <span className="menu-title">Configurações</span>
                            <i className="menu-arrow"></i>
                        </span>
                        <Collapse isOpen={this.state.menuStatus.configurations}>
                            <ul className="nav flex-column sub-menu">
                                <li className="nav-item">
                                    <a className="nav-link" href="configurations.html">Ver Detalhes</a>
                                </li>
                                <li className="nav-item">
                                    <a className="nav-link" href="config-form.html">Editar</a>
                                </li>
                            </ul>
                        </Collapse>
                    </li>
                </ul>
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
