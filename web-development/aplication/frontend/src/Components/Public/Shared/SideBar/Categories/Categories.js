import React, { Component } from 'react';

class Categories extends Component {

    render() {
        return (
            <aside className="Categories single_sidebar_widget post_category_widget">
                <h4 className="widget_title">Categoria</h4>
                <ul className="list cat-list">
                    <li>
                        <a href="#" className="d-flex">
                            <p>Notícias</p>
                            <p>(43)</p>
                        </a>
                    </li>
                    <li>
                        <a href="#" className="d-flex">
                            <p>Anúncios</p>
                            <p>(27)</p>
                        </a>
                    </li>
                    <li>
                        <a href="#" className="d-flex">
                            <p>Avisos</p>
                            <p>(111)</p>
                        </a>
                    </li>
                </ul>
            </aside>
        );
    }
}

export default Categories;
