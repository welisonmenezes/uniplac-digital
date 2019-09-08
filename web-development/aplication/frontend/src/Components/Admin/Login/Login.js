import React, { Component } from 'react';
import { Redirect } from 'react-router-dom';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';

import { setUserLogginStatus } from '../../../Redux/Actions/UserActions';

class Login extends Component {

    constructor(props) {
        super(props);
        this.state = {
            registry: '',
            password: '',
            messageError: null,
            redirect: false
        };
    }

    handleChange = (e) => {
        this.setState({ [e.target.name]: e.target.value });
    }

    login = (e) => {
        e.preventDefault();
        if (this.state.email !== '' && this.state.password !== '') {
            const payload = {
                method: 'POST',
                headers: {
                    'Accept': 'application/json, text/plain, */*',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    'registry': this.state.registry,
                    'password': this.state.password
                })
            };
            fetch('http://127.0.0.1:5000/api/auth', payload)
                .then(data => data.json())
                .then(data => {
                    if (data.error) {
                        this.setState({ messageError: data.message });
                    } else {
                        localStorage.setItem('token', data.token);
                        this.props.setUserLogginStatus(true);
                        this.setState({
                            redirect: true
                        });
                    }
                }, error => {
                    console.log(error)
                });
        } else {
            this.setState({ messageError: 'Campos obrigatórios' });
        }
    }

    render() {
        return (
            <div className="Login">
                <div className="container">
                    <div className="row justify-content-md-center">
                        <div className="col-md-6">
                            <h1>Login</h1>
                            {(this.state.redirect) && <Redirect to="/admin" />}
                            <form onSubmit={this.login} noValidate>
                                <div className="form-group">
                                    <input type="text" name="registry" className="form-control" placeholder="Matrícula" onChange={this.handleChange} />
                                </div>
                                <div className="form-group">
                                    <input type="password" name="password" className="form-control" placeholder="Senha" onChange={this.handleChange} />
                                </div>
                                <button type="submit" className="btn btn-primary">Submit</button>
                                {(this.state.messageError) && <p>{this.state.messageError}</p>}
                            </form>
                            <p>
                                <small>Para teste use: <b>email:</b> test@email.com e <b>senha:</b> 123456</small>
                            </p>
                        </div>
                    </div>
                </div>
            </div>
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

export default connect(mapStateToProps, mapDispatchToProps)(Login);
