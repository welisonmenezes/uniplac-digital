import React, { Component } from 'react';
import { Switch, Route } from 'react-router-dom';

// public components
import Home from './Components/Public/Home/Home';
import NotFound from './Components/Public/NotFound/NotFound';
import Posts from './Components/Public/Posts/Posts';
import Post from './Components/Public/Posts/Post/Post';

// admin components
import Dashboard from './Components/Admin/Dashboard/Dashboard';
import Login from './Components/Admin/Login/Login';
import AdminPosts from './Components/Admin/AdminPosts/AdminPosts';
import PostForm from './Components/Admin/AdminPosts/PostForm/PostForm';
import AdminUsers from './Components/Admin/AdminUsers/AdminUsers';
import UserForm from './Components/Admin/AdminUsers/UserForm/UserForm';
import ConfigurationForm from './Components/Admin/ConfigurationForm/ConfigurationForm';

// utils/extras
import PrivateRouter from './Utils/PrivateRouter';

class App extends Component {
	render() {
		return (
			<div className="App">
				<Switch>
					// public components
					<Route path="/" exact={true} component={Home} />
					<Route path="/noticias" exact={true} component={Posts} />
					<Route path="/noticias/:id" exact={true} component={Post} />
					<Route path="/anuncios" exact={true} component={Posts} />
					<Route path="/anuncios/:id" exact={true} component={Post} />
					<Route path="/avisos" exact={true} component={Posts} />
					<Route path="/avisos/:id" exact={true} component={Post} />


					// admin components
					<Route path='/login' exact={true} component={Login} />
					<PrivateRouter path='/admin' exact={true} component={Dashboard} />
					<PrivateRouter path='/admin/noticias' exact={true} component={AdminPosts} />
					<PrivateRouter path='/admin/noticias/:id' exact={true} component={PostForm} />
					<PrivateRouter path='/admin/anuncios' exact={true} component={AdminPosts} />
					<PrivateRouter path='/admin/anuncios/:id' exact={true} component={PostForm} />
					<PrivateRouter path='/admin/avisos' exact={true} component={AdminPosts} />
					<PrivateRouter path='/admin/avisos/:id' exact={true} component={PostForm} />
					<PrivateRouter path='/admin/usuarios' exact={true} component={AdminUsers} />
					<PrivateRouter path='/admin/usuarios/:id' exact={true} component={UserForm} />
					<PrivateRouter path='/admin/configuracoes' exact={true} component={ConfigurationForm} />

					<Route path='*' component={NotFound} />
				</Switch>
			</div>
		);
	}
}

export default App;
