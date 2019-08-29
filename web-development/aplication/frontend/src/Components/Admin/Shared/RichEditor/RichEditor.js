import React, { Component } from 'react';
import ReactQuill from 'react-quill';
import 'react-quill/dist/quill.snow.css';
import './RichEditor.css';
import {
    IsInt,
    OpenFullscreen,
    CloseFullscreen,
    GetYoutubeVideoId,
    GetFileExtension,
    IsSoundCloudUrl } from '../../../../Utils/Utils';
import Toolbar from './Toolbar';
import './MyImage';
import './MyVideo';
import './MyAudio';

class RichEditor extends Component {

    /* eslint-disable */
    self = null;

    toolbarConfig = {
        'container': '#toolbar',
        'handlers': {
            'my-image': function (value) {
                self.toggleConfigurationPanel('image');
            },
            'my-video': function (value) {
                self.toggleConfigurationPanel('video');
            },
            'my-audio': function (value) {
                self.toggleConfigurationPanel('audio');
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
            currentAudio: null,
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
        const range = editor.getSelection();
        if (range) {
            editor.insertEmbed(range.index, 'myimage', this.getConfigurations());
        }
        this.toggleConfigurationPanel('image');
    }

    insertVideoIntoEditor(editor) {
        editor.focus();
        const range = editor.getSelection();
        if (range) {
            editor.insertEmbed(range.index, 'myvideo', this.getConfigurations());
        }
        this.toggleConfigurationPanel('video');
    }

    insertAudioIntoEditor(editor) {
        editor.focus();
        const range = editor.getSelection();
        if (range) {
            editor.insertEmbed(range.index, 'myaudio', this.getConfigurations());
        }
        this.toggleConfigurationPanel('audio');
    }

    handleAddImage() {
        this.insertImageIntoEditor(this.quillRef);
    }

    handleAddVideo() {
        if ((GetYoutubeVideoId(this.state.currentVideo))){
            this.insertVideoIntoEditor(this.quillRef);
        } else {
            alert('Apenas vídeos do Youtube.');
        }
    }

    handleAddAudio() {
        if (IsSoundCloudUrl(this.state.currentAudio)) {
            this.insertAudioIntoEditor(this.quillRef);
        } else {
            alert('Apenas áudios do SoundCloud.')
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

    handleAudioUrl(e) {
        self.setState({ currentAudio: e.target.value });
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

    resetConfigurationFields() {
        this.setState({
            currentImage: null,
            currentAudio: null,
            currentVideo: null,
            width: 'auto',
            height: 'auto',
            position: 'normal'
        });
        const imageEl = document.getElementById('RichEditorInputFile');
        const videoEl = document.getElementById('RichEditorFieldVideo');
        const audioEl = document.getElementById('RichEditorFieldAudio');
        if (imageEl) {
            imageEl.value = null;
        }
        if (videoEl) {
            videoEl.value = null;
        }
        if (audioEl) {
            audioEl.value = null;
        }
    }

    toggleConfigurationPanel(type) {
        let extraClassName = '.' + type;
        const els = document.querySelectorAll('.configuration-panel'+extraClassName);
        if (els && els.length) {
            els.forEach(el => {
                if (el.classList.contains('opened')) {
                    el.classList.remove('opened');
                } else {
                    el.classList.add('opened');
                }
            });
            self.resetConfigurationFields();
        }
    }

    getConfigurations() {
        let width = (IsInt(this.state.width)) ? this.state.width + 'px' : 'auto';
        let height = (IsInt(this.state.height)) ? + this.state.height + 'px' : 'auto';
        return {
            width,
            height,
            position: this.state.position,
            imageUrl: this.state.currentImage,
            videoUrl: this.state.currentVideo,
            audioUrl: this.state.currentAudio
        };
    }

    encodeImageFileAsURL() {
        const element = document.getElementById('RichEditorInputFile');
        const file = element.files[0];
        const extension = GetFileExtension(file.name).toLowerCase();
        const accepts = element.getAttribute('accept').split(',');
        if (accepts.indexOf('.' + extension) > -1) {
            const reader = new FileReader();
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
                <div id="ImageEditor" className="configuration-panel image">
                    <div>
                        <button onClick={() => this.toggleConfigurationPanel('image') }>Cancelar</button>
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
                <div id="VideoEditor" className="configuration-panel video">
                    <div>
                        <button onClick={() => this.toggleConfigurationPanel('video') }>Cancelar</button>
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
                <div id="AudioEditor" className="configuration-panel audio">
                    <div>
                        <button onClick={() => this.toggleConfigurationPanel('audio') }>Cancelar</button>
                        <div className="row">
                            <div className="col-md-6">
                                <input type="text" id="RichEditorFieldAudio" onChange={this.handleAudioUrl} />
                                <div>
                                    {(this.state.currentAudio) &&
                                        <p>audio here</p>
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
                                {(this.state.currentAudio) &&
                                    <div>
                                        <button onClick={() => { this.handleAddAudio() }}>Add audio</button>
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
