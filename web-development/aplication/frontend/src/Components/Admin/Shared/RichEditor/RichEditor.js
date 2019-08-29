import React, { Component } from 'react';
import ReactQuill from 'react-quill';
import 'react-quill/dist/quill.snow.css';
import './RichEditor.css';

import Toolbar from './Toolbar';

const EmbedBlot = ReactQuill.Quill.import('blots/block/embed');

class MyImage extends EmbedBlot{
    static create(value) {
        console.log('value', value)
        if (typeof value === 'string') {
            var node =  super.create(value);
            node.setAttribute('src', 'https://www.hostinger.com.br/tutoriais/wp-content/uploads/sites/12/2018/03/o-que-e-html.png');
            node.style.float = 'right';
            return node;
        } else {
            return super.create(value);
        }
    }

    static value(node) {
        return {node: node};
    }
}
MyImage.blotName = 'myimage';
MyImage.tagName = 'img';
//MyImage.className = 'myimage';
ReactQuill.Quill.register('formats/myimage', MyImage);



class RichEditor extends Component {

    /* eslint-disable */
    self = null;

    toolbarConfig = {
        'container': '#toolbar',
        'handlers': {
            'audio': function (value) {
                var range = this.quill.getSelection();
                console.log('range; ', range)
                if (range) {      
                    this.quill.insertEmbed(range.index, 'myimage', 'https://www.hostinger.com.br/tutoriais/wp-content/uploads/sites/12/2018/03/o-que-e-html.png');
                }
                
                //const el = document.getElementById('ImageEditor');
                //el.classList.add('opened');
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
            width: 'auto',
            height: 'auto',
            position: 'left'
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
        const width = this.state.width + 'px';
        const height = this.state.height + 'px';
        const position = (this.state.position === 'left') ? 'left' : 'right';
        const img = `<img src="${this.state.currentImage}" alt="test" width="${this.state.width}" height="auto" />`;
        const replaced = '##$$image$$##';
        const index = editor.getSelection().index;
        editor.insertText(index, replaced);
        let content = editor.root.innerHTML;
        content = content.replace(replaced, img);
        console.log(content)
        this.setState({text: content, currentImage: null});
        const el = document.getElementById('ImageEditor');
        el.classList.remove('opened');
    }

    handleAddImage() {
        this.insertImageIntoEditor(this.quillRef);
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
                            <div>
                                <div>
                                    <input 
                                        type="number"
                                        placeholder="Largura"
                                        onChange={ this.handleChangeWidth } />
                                </div>
                                <div>
                                    <input
                                        type="number"
                                        placeholder="Largura"
                                        onChange={ this.handleChangeHeight } />
                                </div>
                            </div>
                            <div>
                                <select onChange={ this.handleChangePosition }>
                                    <option value="left">Esquerda</option>
                                    <option value="center">Centralizado</option>
                                    <option value="right">Direita</option>
                                </select>
                            </div>
                            { (this.state.currentImage) &&
                                <div>
                                    <button onClick={() => { this.handleAddImage() }}>Add image</button>
                                </div>
                            }
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}


export default RichEditor;
