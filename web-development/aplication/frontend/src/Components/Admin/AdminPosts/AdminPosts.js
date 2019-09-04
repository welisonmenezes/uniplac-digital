import React, { Component } from 'react';

import Navigation from '../Shared/Navigation/Navigation';

class AdminPosts extends Component {

	constructor(props) {
		super(props);
		this.state = {};
	}

	componentDidMount() {
		this.setState({currentPath: this.props.location.pathname});
	}

	static getDerivedStateFromProps(nextProps, prevState) {
		if (nextProps.location.pathname !== prevState.currentPath) {
			return ({currentPath: nextProps.location.pathname});
		}
		return null;
	}

	render() {
		return (
			<div className="AdminPosts">
				<Navigation></Navigation>
				<div className="container">
					<div className="row">
						<div className="col-md-12">
							<h1>Admin posts: { this.state.currentPath }</h1>
						</div>
					</div>
				</div>
			</div>
		);
	}
}


export default AdminPosts;
