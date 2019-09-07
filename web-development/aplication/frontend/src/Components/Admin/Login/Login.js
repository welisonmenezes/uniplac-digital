import React, { Component } from 'react';
import { Redirect } from 'react-router-dom';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';

import { setUserLogginStatus } from '../../../Redux/Actions/UserActions';

class Login extends Component {

  constructor(props) {
    super(props);
    this.state = {
      email: '',
      password: '',
      messageError: null,
      redirect: false
    };
  }
  
  handleChange = (e) => {
    this.setState({[e.target.name]: e.target.value});
  }

  login = (e) => {
    e.preventDefault();
    if (this.state.email === 'test@email.com' && this.state.password === '123456') {
        localStorage.setItem('islogged', true);
        this.props.setUserLogginStatus(true);
        this.setState({
            redirect: true
        });
    } else {
        this.setState({messageError: 'Email ou senha inválidos'});
    }
  }

  render() {
    return (
      <div className="Login">
        <div className="container">
          <div className="row justify-content-md-center">
            <div className="col-md-6">
              <h1>Login</h1>
              { (this.state.redirect) && <Redirect to="/admin" /> }
              <form onSubmit={this.login} noValidate>
                  <div className="form-group">
                      <input type="email" name="email" className="form-control" placeholder="Enter email" onChange={this.handleChange} />
                  </div>
                  <div className="form-group">
                      <input type="password" name="password" className="form-control" placeholder="Password" onChange={this.handleChange} />
                  </div>
                  <button type="submit" className="btn btn-primary">Submit</button>
                  { (this.state.messageError) && <p>{this.state.messageError}</p> }
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
