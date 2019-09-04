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

// utils/extras
import PrivateRouter from './Utils/PrivateRouter';

class App extends Component {
	render() {
		return (
			<div className="App">
				<Switch>
					// public components
					<Route path="/" exact={true} component={Home} />
					<Route
						path="/noticias"
						exact={true}
						render={(props) => <Posts {...props} contentType="noticia" />} />
					<Route
						path="/anuncios"
						exact={true}
						render={(props) => <Posts {...props} contentType="anuncio" />} />
					<Route
						path="/avisos"
						exact={true}
						render={(props) => <Posts {...props} contentType="aviso" />} />
					<Route
						path="/noticia/:id"
						exact={true}
						render={(props) => <Post {...props} contentType="noticia" />} />
					<Route
						path="/anuncio/:id"
						exact={true}
						render={(props) => <Post {...props} contentType="anuncio" />} />
					<Route
						path="/aviso/:id"
						exact={true}
						render={(props) => <Post {...props} contentType="aviso" />} />


					// admin components
					<Route path='/login' exact={true} component={Login} />
					<PrivateRouter path='/admin' component={Dashboard} />

					<Route path='*' component={NotFound} />
				</Switch>
			</div>
		);
	}
}

export default App;
