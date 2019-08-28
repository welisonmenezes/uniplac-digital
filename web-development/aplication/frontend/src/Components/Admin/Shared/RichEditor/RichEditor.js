import React, { Component } from 'react';
import ReactQuill from 'react-quill';
import 'react-quill/dist/quill.snow.css';
import './RichEditor.css';

import Toolbar from './Toolbar';


class RichEditor extends Component {

    /* eslint-disable */
    self = null;

    toolbarConfig = {
        'container': '#toolbar',
        'handlers': {
            'audio': function (value) {
                const el = document.getElementById('ImageEditor');
                el.classList.add('opened');
            }
        }
    };

    constructor(props) {
        super(props);
        this.quillRef = null;
        this.reactQuillRef = null;
        this.state = { text: '', currentImage: null };
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

    handleEditorChange(value) {
        this.setState({ text: value });
    }

    insertImageIntoEditor(editor) {
        editor.focus();
        const img = `<img src="${this.state.currentImage}" alt="test" style="width:200;float: none;" />`;
        const replaced = '##$$image$$##';
        const index = editor.getSelection().index;
        editor.insertText(index, replaced);
        let content = editor.root.innerHTML;
        content = content.replace(replaced, img);
        this.setState({text: content, currentImage: null});
        const el = document.getElementById('ImageEditor');
        el.classList.remove('opened');
    }

    handleAddImage() {
        this.insertImageIntoEditor(this.quillRef);
    }

    encodeImageFileAsURL() {
        var element = document.getElementById('RichEditorInputFile');
        var file = element.files[0];
        var reader = new FileReader();
        reader.onloadend = function () {
            self.setState({currentImage: reader.result});
            document.getElementById('RichEditorImage').src = reader.result;
        }
        reader.readAsDataURL(file);
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
                    <div className="row">
                        <div className="col-md-6">
                            <input type="file" id="RichEditorInputFile" name="files" onChange={() => { this.encodeImageFileAsURL() }} />
                            <div>
                                { (this.state.currentImage) &&
                                    <img id="RichEditorImage" src="" alt="Preview da imagem" />
                                }
                            </div>
                        </div>
                        <div className="col-md-6">
                            form config
                            <button onClick={() => { this.handleAddImage() }}>Add image</button>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}


export default RichEditor;
