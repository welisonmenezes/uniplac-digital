import React, { Component } from 'react';

import Navigation from '../../Shared/Navigation/Navigation';

class PostForm extends Component {

    constructor(props) {
        super(props);
        this.state = {};

        console.log(props);
    }

    render() {
        return (
            <div className="PostForm">
                <Navigation></Navigation>
                <div className="container">
                    <div className="row">
                        <div className="col-md-12">
                            <h1>Admin post form</h1>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}


export default PostForm;
