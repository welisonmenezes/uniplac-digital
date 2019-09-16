import React, { Component } from "react";

class Dashboard extends Component {

    render() {
        return (
            <div className="Dashboard">
                <div className="row">
                    <div className="col-md-12 grid-margin">
                        <div className="d-flex justify-content-between flex-wrap">
                            <div className="d-flex align-items-end flex-wrap">
                                <div className="mr-md-3 mr-xl-5">
                                    <h2>Bem Vindo de Volta Biel</h2>
                                    <p className="mb-md-0">
                                        Confira as Atualizações abaixo{" "}
                                    </p>
                                </div>
                                <div className="d-flex">
                                    <p className="text-primary mb-0 hover-cursor">
                                        <a href="../index.html" target="_blank">
                                            <i className="mdi mdi-home text-muted hover-cursor" />
                                            Ver Site
                                        </a>
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div className="row">
                    <div className="col-md-4 grid-margin stretch-card">
                        <div className="card">
                            <div className="card-body">
                                <h4 className="card-title">
                                    Cadastrar Notícias
                                </h4>
                                <div className="media">
                                    <div className="media-body">
                                        <a href="post-form.html">
                                            <button
                                                type="button"
                                                className="btn btn-primary btn-icon-text"
                                            >
                                                Cadastrar Noticias
                                            </button>
                                        </a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="col-md-4 grid-margin stretch-card">
                        <div className="card">
                            <div className="card-body">
                                <h4 className="card-title">Cadastrar Avisos</h4>
                                <div className="media">
                                    <div className="media-body">
                                        <a href="post-form.html">
                                            <button
                                                type="button"
                                                className="btn btn-primary btn-icon-text"
                                            >
                                                Cadastrar Avisos
                                            </button>
                                        </a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="col-md-4 grid-margin stretch-card">
                        <div className="card">
                            <div className="card-body">
                                <h4 className="card-title">
                                    Cadastrar Anuncios
                                </h4>
                                <div className="media">
                                    <div className="media-body">
                                        <a href="post-form.html">
                                            <button
                                                type="button"
                                                className="btn btn-primary btn-icon-text"
                                            >
                                                Cadastrar Anuncios
                                            </button>
                                        </a>
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

export default Dashboard;
