import React, { Component } from 'react';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';

import { getUsers, getUsersSuccess, getUsersError } from '../../../Redux/Actions/UsersActions';

import Navigation from '../Shared/Navigation/Navigation';

class Home extends Component {

  loadData = () => {
    this.props.getUsers(true);
    this.props.getUsersError(null);
    fetch("http://dummy.restapiexample.com/api/v1/employees")
      .then(data => data.json())
      .then(data => {
        this.props.getUsersSuccess(data);
        this.props.getUsers(false);
        console.log(data)
      }, error => {
        this.props.getUsersError('Error ao carregar');
        this.props.getUsers(false);
      });
  }

  render() {

    const { 
      users,
      loadingUsers,
      errorUsers
    } = this.props;

    return (
      <div className="Home">
        <Navigation></Navigation>
        <h1>Home</h1>
        <hr />
        <button onClick={() => this.loadData()}>Carregar Dados</button>
        { (users) && users.map(user => {
          return <p key={user.id}><b>Name: </b>{user.employee_name}</p>
        }) }
        { (loadingUsers) && <p>carregando</p> }
        { (errorUsers) && <p>{errorUsers}</p> }
      </div>
    );
  }
}

const mapStateToProps = store => ({
  users: store.usersState.users,
  loadingUsers: store.usersState.loadingUsers,
  errorUsers: store.usersState.errorUsers
});

const mapDispatchToProps = dispatch =>
  bindActionCreators({
    getUsers,
    getUsersSuccess,
    getUsersError
  }, dispatch);

export default connect(mapStateToProps, mapDispatchToProps)(Home);
