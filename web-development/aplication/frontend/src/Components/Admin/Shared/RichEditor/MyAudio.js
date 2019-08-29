import ReactQuill from 'react-quill';

const EmbedBlot = ReactQuill.Quill.import('blots/block/embed');

export class MyAudio extends EmbedBlot {

    static create(value) {
        if (typeof value === 'object' && value.audioUrl) {
            const node = super.create(value);
            const scUlr = `https://w.soundcloud.com/player/?url=${encodeURI(value.audioUrl)}`;
            node.setAttribute('src', scUlr);
            node.style.width = value.width;
            node.style.height = value.height;
            switch (value.position) {
                case 'left':
                    node.style.float = value.position;
                    break;
                case 'right':
                    node.style.float = value.position;
                    break;
                case 'center':
                    node.style.marginLeft = 'auto';
                    node.style.marginRight = 'auto';
                    node.style.display = 'flex';
                    break;
                default:
                    break;
            }
            return node;
        } else {
            return value;
        }
    }

    static value(node) {
        return node;
    }
}

MyAudio.blotName = 'myaudio';
MyAudio.tagName = 'iframe';
MyAudio.className = 'MyAudio';
ReactQuill.Quill.register(MyAudio);