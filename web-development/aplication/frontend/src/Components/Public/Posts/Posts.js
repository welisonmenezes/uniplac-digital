import React, { Component } from 'react';

import Navigation from '../Shared/Navigation/Navigation';

class Posts extends Component {

	constructor(props) {
		super(props);
		this.state = {
			currentPath: this.props.location.pathname
		};
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
			<div className="Posts">
				<Navigation></Navigation>
				<div className="container">
					<div className="row">
						<div className="col-md-12">
							<h1>Posts: { this.state.currentPath }</h1>
						</div>
					</div>
				</div>
			</div>
		);
	}
}


export default Posts;
