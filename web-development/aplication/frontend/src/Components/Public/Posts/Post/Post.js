import React, { Component } from 'react';

class Post extends Component {

    constructor(props) {
        super(props);
        this.state = {};
    }

    render() {
        return (
            <div className="Post blog_left_sidebar">
                <article className="blog_item">
                    <div className="blog_item_img">
                        <img className="card-img rounded-0" src={this.props.post.image} alt="" />
                    </div>
                    <div className="blog_details">
                        <a className="d-inline-block" href="#">
                            <h2>{this.props.post.title}</h2>
                        </a>
                        <p>{this.props.post.description}</p>
                        <a href="#" className="blog_btn">
                            Ver Mais <span className="ml-2 ti-arrow-right"></span>
                        </a>
                    </div>
                </article>
            </div>
        );
    }
}


export default Post;
