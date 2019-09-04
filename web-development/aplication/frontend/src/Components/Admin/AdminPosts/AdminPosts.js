import React, { Component } from 'react';

import Navigation from '../Shared/Navigation/Navigation';

class AdminPosts extends Component {

	constructor(props) {
		super(props);
		this.state = {};

		console.log(props);
	}

	render() {
		return (
			<div className="AdminPosts">
				<Navigation></Navigation>
				<div className="container">
					<div className="row">
						<div className="col-md-12">
							<h1>Admin posts</h1>
						</div>
					</div>
				</div>
			</div>
		);
	}
}


export default AdminPosts;
