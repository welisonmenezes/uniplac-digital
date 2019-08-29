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
    IsSoundCloudUrl,
    IsAnUrl,
    CreateYoutubeIframe,
    CreateSoundCloudIframe } from '../../../../Utils/Utils';
import Toolbar from './Toolbar';
import './MyImage';
import './MyVideo';
import './MyAudio';
import './MyLink';

function Iframe(props) {
    return (<div dangerouslySetInnerHTML={ {__html:  props.iframe?props.iframe:""}} />);
  }

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
            'my-link': function (value) {
                self.toggleConfigurationPanel('link');
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
            currentLink: null,
            width: 'auto',
            height: 'auto',
            position: 'normal',
            target: '_self',
            title: null
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

    insertLinkIntoEditor(editor) {
        editor.focus();
        const range = editor.getSelection();
        if (range) {
            editor.formatText(range.index, range.length, 'mylink', this.getConfigurations());
        }
        this.toggleConfigurationPanel('link');
    }

    handleFakeUploadImage() {
        const element = document.getElementById('RichEditorInputFile');
        const file = element.files[0];
        const extension = GetFileExtension(file.name).toLowerCase();
        const accepts = element.getAttribute('accept').split(',');
        if (accepts.indexOf('.' + extension) > -1) {
            const reader = new FileReader();
            reader.onloadend = function () {
                self.setState({ currentImage: reader.result });
            }
            reader.readAsDataURL(file);
        } else {
            element.value = null;
            alert('Tipo de arquivo inválido. Apenas imagem.');
        }
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

    handleAddLink() {
        if (IsAnUrl(this.state.currentLink)) {
            this.insertLinkIntoEditor(this.quillRef);
        } else {
            alert('Apenas urls válidas.');
        }
    }

    handleEditorChange(value) {
        this.setState({ text: value });
        this.props.parentGettingTheEditorValue(this.state.text);
    }
    
    handleChange(e) {
        const stateName = e.target.getAttribute('data-state-name');
        self.setState({[stateName]: e.target.value});
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
            currentLink: null,
            width: 'auto',
            height: 'auto',
            position: 'normal',
            target: '_self',
            title: null
        });
        const els = document.querySelectorAll('.configuration-panel input, .configuration-panel select');
        if (els && els.length) {
            els.forEach(el => {
                el.value = null;
            });
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
            audioUrl: this.state.currentAudio,
            linkUrl: this.state.currentLink,
            title: this.state.title,
            target: this.state.target
        };
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
                                    onChange={() => { this.handleFakeUploadImage() }} />
                                <div>
                                    {(this.state.currentImage) &&
                                        <img id="previewImage" src={this.state.currentImage} alt="Preview da imagem" />
                                    }
                                </div>
                            </div>
                            <div className="col-md-6">
                                <div>
                                    <div>
                                        <input
                                            type="number"
                                            placeholder="Largura"
                                            data-state-name="width"
                                            onChange={this.handleChange} />
                                    </div>
                                    <div>
                                        <input
                                            type="number"
                                            placeholder="Largura"
                                            data-state-name="height"
                                            onChange={this.handleChange} />
                                    </div>
                                </div>
                                <div>
                                    <select
                                        data-state-name="position"
                                        onChange={this.handleChange}>
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
                                <input
                                    type="text"
                                    id="RichEditorFieldVideo"
                                    data-state-name="currentVideo"
                                    onChange={this.handleChange} />
                                <div>
                                    <Iframe iframe={'<iframe src="" id="previewVideo"></iframe>'} />
                                    {(this.state.currentVideo && GetYoutubeVideoId(this.state.currentVideo)) &&
                                        <div>
                                            { CreateYoutubeIframe(document.getElementById('previewVideo'), this.getConfigurations()) }
                                        </div>
                                    }
                                    {(!GetYoutubeVideoId(this.state.currentVideo)) && 
                                        <div className="hide">{ (setTimeout(() => {
                                            if (document.getElementById('previewVideo')) {
                                                document.getElementById('previewVideo').setAttribute('src','')
                                            }
                                        }, 1)) }</div>
                                    }
                                </div>
                            </div>
                            <div className="col-md-6">
                                <div>
                                    <div>
                                        <input
                                            type="number"
                                            placeholder="Largura"
                                            data-state-name="width"
                                            onChange={this.handleChange} />
                                    </div>
                                    <div>
                                        <input
                                            type="number"
                                            placeholder="Largura"
                                            data-state-name="height"
                                            onChange={this.handleChange} />
                                    </div>
                                </div>
                                <div>
                                    <select 
                                        data-state-name="position"
                                        onChange={this.handleChange}>
                                        <option value="normal">Normal</option>
                                        <option value="left">Esquerda</option>
                                        <option value="center">Centralizado</option>
                                        <option value="right">Direita</option>
                                    </select>
                                </div>
                                {(this.state.currentVideo && GetYoutubeVideoId(this.state.currentVideo)) &&
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
                                <input
                                    type="text"
                                    id="RichEditorFieldAudio"
                                    data-state-name="currentAudio"
                                    onChange={this.handleChange} />
                                <div>
                                    <Iframe iframe={'<iframe src="" id="previewAudio"></iframe>'} />
                                    {(this.state.currentAudio) && IsSoundCloudUrl(this.state.currentAudio) &&
                                        <div>
                                            { CreateSoundCloudIframe(document.getElementById('previewAudio'), this.getConfigurations()) }
                                        </div>
                                    }
                                    {(!IsSoundCloudUrl(this.state.currentAudio)) && 
                                        <div className="hide">{ (setTimeout(() => {
                                            if (document.getElementById('previewAudio')) {
                                                document.getElementById('previewAudio').setAttribute('src','')
                                            }
                                        }, 1)) }</div>
                                    }
                                </div>
                            </div>
                            <div className="col-md-6">
                                <div>
                                    <div>
                                        <input
                                            type="number"
                                            placeholder="Largura"
                                            data-state-name="width"
                                            onChange={this.handleChange} />
                                    </div>
                                    <div>
                                        <input
                                            type="number"
                                            placeholder="Largura"
                                            data-state-name="height"
                                            onChange={this.handleChange} />
                                    </div>
                                </div>
                                <div>
                                    <select
                                        data-state-name="position"
                                        onChange={this.handleChange}>
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
                <div id="LinkEditor" className="configuration-panel link">
                    <div>
                        <button onClick={() => this.toggleConfigurationPanel('link') }>Cancelar</button>
                        <div className="row">
                            <div className="col-md-6">
                                <div>
                                    <div>
                                        <input
                                            type="text"
                                            id="RichEditorFieldLink"
                                            data-state-name="currentLink"
                                            onChange={this.handleChange} />
                                        <div>
                                            {(this.state.currentLink) &&
                                                <p>link here</p>
                                            }
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div className="col-md-6">
                                <div>
                                    <div>
                                        <input
                                            type="text"
                                            placeholder="Título"
                                            data-state-name="title"
                                            onChange={this.handleChange} />
                                    </div>
                                    <div>
                                        <select
                                            data-state-name="target"
                                            onChange={this.handleChange}>
                                            <option value="_self">Abrir na mesma janela</option>
                                            <option value="_blank">Abrir em outra janela</option>
                                        </select>
                                    </div>
                                </div>
                                {(this.state.currentLink) &&
                                    <div>
                                        <button onClick={() => { this.handleAddLink() }}>Add link</button>
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
