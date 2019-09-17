import React, { Component } from 'react';
import FormFilter from '../Shared/FormFilter/FormFilter';

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

	getPosts = () => {
		return [
			{
				id: 1,
				title: 'Ford clever bed stops your sleeping partner hogging the whole',
				data: '10-10-2001'
			},
			{
				id: 2,
				title: 'Ford clever bed stops your sleeping partner hogging the whole',
				data: '10-10-2001'
			},
			{
				id: 3,
				title: 'Ford clever bed stops your sleeping partner hogging the whole',
				data: '10-10-2001'
			},
			{
				id: 4,
				title: 'Ford clever bed stops your sleeping partner hogging the whole',
				data: '10-10-2001'
			},
			{
				id: 5,
				title: 'Ford clever bed stops your sleeping partner hogging the whole',
				data: '10-10-2001'
			},
			{
				id: 6,
				title: 'Ford clever bed stops your sleeping partner hogging the whole',
				data: '10-10-2001'
			},
		];
	}

	render() {
		return (
			<div className="AdminPosts">
				<div className="row">
						<div className="col-lg-12 grid-margin stretch-card">
							<div className="card">
								<div className="card-body">
									<h4 className="card-title">Notícias</h4>

									<FormFilter />

									<div className="table-responsive">
										<table className="table table-striped">
											<thead>
												<tr>
													<th>ID</th>
													<th>Noticia</th>
													<th>Data</th>
													<th>Ver/Editar/Deletar</th>
												</tr>
											</thead>
											<tbody>
												{ this.getPosts().map(post => {
													return (<tr key={post.id}>
														<td>{ post.id }</td>
														<td>{ post.title }</td>
														<td>{ post.data }</td>
														<td>
															<a href="../single-blog.html" target="_blank">
																<i className="mdi mdi-television-guide view"></i>
															</a>
															<a href="post-form.html">
																<i className="mdi mdi-border-color edit"></i>
															</a>
															<i className="mdi mdi-delete-forever delete"></i>
														</td>
													</tr>)
												}) }
											</tbody>
										</table>
									</div>
									<div className="table-pagination">
										<div className="btn-group" role="group" aria-label="Basic example">
											<button type="button" className="btn btn-primary">1</button>
											<button type="button" className="btn btn-primary">2</button>
											<button type="button" className="btn btn-primary">3</button>
										</div>
									</div>
								</div>
							</div>

						</div>

					</div>
			</div>
		);
	}
}


export default AdminPosts;
