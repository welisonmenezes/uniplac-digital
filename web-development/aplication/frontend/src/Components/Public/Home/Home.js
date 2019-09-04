import React, { Component } from 'react';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';

import { getUsers, getUsersSuccess, getUsersError } from '../../../Redux/Actions/UsersActions';

import Navigation from '../Shared/Navigation/Navigation';
import UploadButton from '../../Admin/Shared/UploadButton/UploadButton';

class Home extends Component {

	constructor(props) {
		super(props);
		this.state = {
			currentImage: null,
			uploadError: null,
			loadingImage: false
		};
	}

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

	getUploadButtonState = (childState) => {
		console.log(childState)
		this.setState({
			currentImage: childState.currentImage,
			uploadError: childState.uploadError,
			loadingImage: childState.loadingImage
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
				<div className="container">
					<div className="row">
						<div className="col-md-12">
							<h1>Home</h1>
							<hr />
							<UploadButton getUploadButtonState={this.getUploadButtonState} />
							<div className="form-group">
								{(this.state.currentImage) &&
									<img id="previewImage" src={this.state.currentImage} alt="Preview da imagem" />
								}
								{(this.state.loadingImage) &&
									<p>Enviado...</p>
								}
								{(this.state.uploadError) &&
									<p>{this.state.uploadError}</p>
								}
							</div>
							<hr />
							<button onClick={() => this.loadData()}>Carregar Dados</button>
							{(users) && users.map(user => {
								return <p key={user.id}><b>Name: </b>{user.employee_name}</p>
							})}
							{(loadingUsers) && <p>carregando</p>}
							{(errorUsers) && <p>{errorUsers}</p>}
						</div>
					</div>
				</div>
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
