import React, { Component } from 'react';
import ReactQuill from 'react-quill';
import 'react-quill/dist/quill.snow.css';
import './RichEditor.css';
import {
    IsInt,
    OpenFullscreen,
    CloseFullscreen,
    GetYoutubeVideoId,
    GetFileExtension } from '../../../../Utils/Utils';
import Toolbar from './Toolbar';
import './MyImage';
import './MyVideo';

class RichEditor extends Component {

    /* eslint-disable */
    self = null;

    toolbarConfig = {
        'container': '#toolbar',
        'handlers': {
            'my-image': function (value) {
                self.toggleImagePanel();
            },
            'my-video': function (value) {
                self.toggleVideoPanel();
            },
            'fullscreen': function (value) {
                self.openFullscreen();
            }
        }
    };

    constructor(props) {
        super(props);
        this.quillRef = null;
        this.reactQuillRef = null;
        this.state = {
            text: '',
            currentImage: null,
            currentVideo: null,
            width: 'auto',
            height: 'auto',
            position: 'normal'
        };
        this.handleEditorChange = this.handleEditorChange.bind(this);
        self = this;
    }

    componentDidMount() {
        this.attachQuillRefs()
    }

    componentDidUpdate() {
        this.attachQuillRefs()
    }

    attachQuillRefs = () => {
        if (typeof this.reactQuillRef.getEditor !== 'function') return;
        this.quillRef = this.reactQuillRef.getEditor();
    }

    insertImageIntoEditor(editor) {
        editor.focus();
        var range = editor.getSelection();
        if (range) {
            editor.insertEmbed(range.index, 'myimage', this.getImageConfigurations());
        }
        this.toggleImagePanel();
    }

    insertVideoIntoEditor(editor) {
        editor.focus();
        var range = editor.getSelection();
        if (range) {
            editor.insertEmbed(range.index, 'myvideo', this.getVideoConfigurations());
        }
        this.toggleVideoPanel();
    }

    handleAddImage() {
        this.insertImageIntoEditor(this.quillRef);
    }

    handleAddVideo() {
        if ((GetYoutubeVideoId(this.state.currentVideo))){
            this.insertVideoIntoEditor(this.quillRef);
        } else {
            alert('Apenas vídeos do youtube');
        }
    }

    handleEditorChange(value) {
        this.setState({ text: value });
    }

    handleChangeWidth(e) {
        self.setState({ width: e.target.value });
    }

    handleChangeHeight(e) {
        self.setState({ height: e.target.value });
    }

    handleChangePosition(e) {
        self.setState({ position: e.target.value });
    }

    handleVideoUrl(e) {
        self.setState({ currentVideo: e.target.value });
    }

    openFullscreen() {
        const el = document.querySelector('.RichEditor');
        if (el.classList.contains('is-fullscreen')) {
            CloseFullscreen();
            el.classList.remove('is-fullscreen');
        } else {
            OpenFullscreen(el);
            el.classList.add('is-fullscreen');
        }
        
    }

    resetImageFields() {
        this.setState({
            currentImage: null,
            width: 'auto',
            height: 'auto',
            position: 'normal'
        });
        document.getElementById('RichEditorInputFile').value = null;
    }

    resetVideoFields() {
        this.setState({
            currentVideo: null,
            width: 'auto',
            height: 'auto',
            position: 'normal'
        });
        document.getElementById('RichEditorFieldVideo').value = null;
    }

    toggleImagePanel() {
        const el = document.getElementById('ImageEditor');
        if (el.classList.contains('opened')) {
            el.classList.remove('opened');
            self.resetImageFields();
        } else {
            el.classList.add('opened');
        }
    }

    toggleVideoPanel() {
        const el = document.getElementById('VideoEditor');
        if (el.classList.contains('opened')) {
            el.classList.remove('opened');
            self.resetVideoFields();
        } else {
            el.classList.add('opened');
        }
    }

    getImageConfigurations() {
        let width = (IsInt(this.state.width)) ? this.state.width + 'px' : 'auto';
        let height = (IsInt(this.state.height)) ? + this.state.height + 'px' : 'auto';
        return {
            width,
            height,
            position: this.state.position,
            url: this.state.currentImage
        };
    }

    getVideoConfigurations() {
        let width = (IsInt(this.state.width)) ? this.state.width + 'px' : 'auto';
        let height = (IsInt(this.state.height)) ? + this.state.height + 'px' : 'auto';
        return {
            width,
            height,
            position: this.state.position,
            url: this.state.currentVideo
        };
    }

    encodeImageFileAsURL() {
        var element = document.getElementById('RichEditorInputFile');
        var file = element.files[0];
        const extension = GetFileExtension(file.name).toLowerCase();
        const accepts = element.getAttribute('accept').split(',');
        if (accepts.indexOf('.' + extension) > -1) {
            var reader = new FileReader();
            reader.onloadend = function () {
                self.setState({ currentImage: reader.result });
                document.getElementById('RichEditorImage').src = reader.result;
            }
            reader.readAsDataURL(file);
        } else {
            element.value = null;
            alert('Tipo de arquivo inválido. Apenas imagem.');
        }
    }

    render() {
        return (
            <div className='RichEditor'>
                <Toolbar />
                <ReactQuill
                    ref={(el) => { this.reactQuillRef = el }}
                    value={this.state.text}
                    modules={{ toolbar: this.toolbarConfig }}
                    onChange={this.handleEditorChange} />
                <div id="ImageEditor">
                    <div>
                        <button onClick={this.toggleImagePanel}>Cancelar</button>
                        <div className="row">
                            <div className="col-md-6">
                                <input
                                    type="file"
                                    id="RichEditorInputFile"
                                    name="files"
                                    accept=".jpg,.jpeg,.png,.gif"
                                    onChange={() => { this.encodeImageFileAsURL() }} />
                                <div>
                                    {(this.state.currentImage) &&
                                        <img id="RichEditorImage" src="" alt="Preview da imagem" />
                                    }
                                </div>
                            </div>
                            <div className="col-md-6">
                                <div>
                                    <div>
                                        <input
                                            type="number"
                                            placeholder="Largura"
                                            onChange={this.handleChangeWidth} />
                                    </div>
                                    <div>
                                        <input
                                            type="number"
                                            placeholder="Largura"
                                            onChange={this.handleChangeHeight} />
                                    </div>
                                </div>
                                <div>
                                    <select onChange={this.handleChangePosition}>
                                        <option value="normal">Normal</option>
                                        <option value="left">Esquerda</option>
                                        <option value="center">Centralizado</option>
                                        <option value="right">Direita</option>
                                    </select>
                                </div>
                                {(this.state.currentImage) &&
                                    <div>
                                        <button onClick={() => { this.handleAddImage() }}>Add image</button>
                                    </div>
                                }
                            </div>
                        </div>
                    </div>
                </div>
                <div id="VideoEditor">
                    <div>
                        <button onClick={this.toggleVideoPanel}>Cancelar</button>
                        <div className="row">
                            <div className="col-md-6">
                                <input type="text" id="RichEditorFieldVideo" onChange={this.handleVideoUrl} />
                                <div>
                                    {(this.state.currentVideo) &&
                                        <p>video here</p>
                                    }
                                </div>
                            </div>
                            <div className="col-md-6">
                                <div>
                                    <div>
                                        <input
                                            type="number"
                                            placeholder="Largura"
                                            onChange={this.handleChangeWidth} />
                                    </div>
                                    <div>
                                        <input
                                            type="number"
                                            placeholder="Largura"
                                            onChange={this.handleChangeHeight} />
                                    </div>
                                </div>
                                <div>
                                    <select onChange={this.handleChangePosition}>
                                        <option value="normal">Normal</option>
                                        <option value="left">Esquerda</option>
                                        <option value="center">Centralizado</option>
                                        <option value="right">Direita</option>
                                    </select>
                                </div>
                                {(this.state.currentVideo) &&
                                    <div>
                                        <button onClick={() => { this.handleAddVideo() }}>Add vídeo</button>
                                    </div>
                                }
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

export default RichEditor;
