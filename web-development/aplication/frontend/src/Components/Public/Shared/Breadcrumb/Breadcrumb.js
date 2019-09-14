import React, { Component } from 'react';

class Breadcrumb extends Component {

    render() {
        return (
            <section className="Breadcrumb banner_area">
                <div className="banner_inner d-flex align-items-center">
                    <div className="container">
                        <div className="banner_content d-md-flex justify-content-between align-items-center">
                            <div className="mb-3 mb-md-0">
                                <h2>{this.props.title}</h2>
                            </div>
                            <div className="page_link">
                                <a href="#">Home</a>
                                <strong>{this.props.title}</strong>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        );
    }
}

export default Breadcrumb;
