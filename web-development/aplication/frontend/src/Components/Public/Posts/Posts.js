import React, { Component } from 'react';
import FormFilter from '../Shared/FormFilter/FormFilter';
import Breadcrumb from '../Shared/Breadcrumb/Breadcrumb';

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
				<Breadcrumb />
				<FormFilter />
			</div>
		);
	}
}


export default Posts;
