import ReactQuill from 'react-quill';
import { GetYoutubeVideoId } from '../../../../Utils/Utils';

const EmbedBlot = ReactQuill.Quill.import('blots/block/embed');

export class MyVideo extends EmbedBlot {

    static create(value) {
        if (typeof value === 'object' && value.url) {
            var node = super.create(value);
            const ytUrl = `https://www.youtube.com/embed/${GetYoutubeVideoId(value.url)}`;
            node.setAttribute('src', ytUrl);
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

MyVideo.blotName = 'myvideo';
MyVideo.tagName = 'iframe';
MyVideo.className = 'MyVideo';
ReactQuill.Quill.register(MyVideo);