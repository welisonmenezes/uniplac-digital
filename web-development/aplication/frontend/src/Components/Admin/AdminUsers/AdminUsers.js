import React, { Component } from 'react';

class AdminUsers extends Component {

	constructor(props) {
		super(props);
		this.state = {};

		console.log(props);
	}

	render() {
		return (
			<div className="AdminUsers">
				<div className="container">
					<div className="row">
						<div className="col-md-12">
							<h1>Admin users</h1>
						</div>
					</div>
				</div>
			</div>
		);
	}
}


export default AdminUsers;
