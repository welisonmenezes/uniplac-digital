import React, { Component } from 'react';

//import AudioIcon from './images/speaker.svg';

class Toolbar extends Component {
    render() {
        return (
            <div className='Toolbar' id='toolbar'>
            <span className='ql-formats'>
              <select className='ql-header'>
                <option value='2'>Título 2</option>
                <option value='3'>Título 3</option>
                <option value='4'>Título 4</option>
                <option value='5'>Título 5</option>
                <option value='6'>Título 6</option>
              </select>
              <select className='ql-size'>
                <option value='small'></option>
                <option value='normal'></option>
                <option value='large'></option>
                <option value='huge'></option>
              </select>
            </span>
            <span className='ql-formats'>
              <button className='ql-bold'></button>
              <button className='ql-italic'></button>
              <button className='ql-underline'></button>
              <button className='ql-strike'></button>
            </span>
            <span className='ql-formats'>
              <button className='ql-script' value='sub'></button>
              <button className='ql-script' value='super'></button>
            </span>
            <span className='ql-formats'>
              <select className='ql-align'>
                <option></option>
                <option value='center'></option>
                <option value='right'></option>
                <option value='justify'></option>
              </select>
              <button className='ql-list' value='ordered'></button>
              <button className='ql-list' value='bullet'></button>
            </span>
            <span className='ql-formats'>
              <button className='ql-blockquote'></button>
              <button className='ql-code-block'></button>
              <button className='ql-link'></button>
            </span>
            <span className='ql-formats'>
              <button className='ql-image'></button>
              <button className='ql-video'></button>
              <button className='ql-my-image' value='my-image'>
                I
              </button>
              <button className='ql-my-video' value='my-video'>
                V
              </button>
              <button className='ql-my-audio' value='my-audio'>
                A
              </button>
            </span>
            <span className='ql-formats'>
              <button className='ql-clean'></button>
              <button className='ql-fullscreen' value='fullscreen'>fullscreen</button>
            </span>
          </div>
        );
    }
}

export default Toolbar;