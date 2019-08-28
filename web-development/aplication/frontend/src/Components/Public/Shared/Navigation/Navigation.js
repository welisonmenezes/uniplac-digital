import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';

import { setUserLogginStatus } from '../../../../Redux/Actions/UserActions';

class Navigation extends Component {

    handleLogout = () => {
        localStorage.removeItem('islogged');
        this.props.setUserLogginStatus(false);
        console.log('this.props.isUserLoggedin: ', this.props.isUserLoggedin)
    };

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
                                <Link to="/login">
                                    <span className="nav-link">Login</span>
                                </Link>
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
