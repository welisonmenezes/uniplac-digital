document.addEventListener('DOMContentLoaded', function() {
    
    // mascara para telefone
    var tel = document.querySelector('.mask-phone');
    if (tel) {
        function inputHandler(masks, max, event) {
            var c = event.target;
            var v = c.value.replace(/\D/g, '');
            var m = c.value.length > max ? 1 : 0;
            VMasker(c).unMask();
            VMasker(c).maskPattern(masks[m]);
            c.value = VMasker.toPattern(v, masks[m]);
        }
        var telMask = ['(99) 9999-99999', '(99) 99999-9999'];
        VMasker(tel).maskPattern(telMask[0]);
        tel.addEventListener('input', inputHandler.bind(undefined, telMask, 14), false);
    }

    // máscara para números
    var num = document.querySelector('.mask-number');
    if (num) {
        VMasker(num).maskNumber();
    }

    // botão de upload
    $('body').on('click', '.file-upload-browse', function(){
        $('.file-upload-default').click();
    });

    // dispara envio de imagem
    $('body').on('change', '.file-upload-default', function(evt) {
        enviaImagem(evt);
    });

    // close o preview de imagem
    $('body').on('click', '.closePreviewImage', function(){
        var t = $(this);
        var parent = t.parent().parent().parent().parent();
        var container = parent.find('.image-container');
        var imageInput = parent.find('input[type=hidden]');
        container.html('');
        imageInput.val('');
    });

    // metodo de envio de imagem
    enviaImagem = function(evt){
        var element = evt.target;
        var file = element.files[0];
        if (file && file.name) {
            var filename = file.name;
            var extension = filename.slice((filename.lastIndexOf('.') - 1 >>> 0) + 2).toLowerCase();
            var accepts = element.getAttribute('accept').split(',');
            if (file.size <= 5017969) {
                if (accepts.indexOf('.' + extension) > -1) {
                    var reader = new FileReader();
                    reader.onloadend = () => {
                        fetch(GLOBALS.BASE_URL+'api/image', {
                            method: 'POST',
                            headers: {
                                'Accept': 'application/json',
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({ image: reader.result })
                        })
                            .then(data => data.json())
                            .then(data => {
                                if (data && data.id) {
                                    addImageHTML(element, data.id);
                                } else {
                                    addImageHTML(element, null, data.message);
                                }
                            }, error => {
                                addImageHTML(element, null, error);
                                element.value = null;
                            });
                    }
                    reader.readAsDataURL(file);
                } else {
                    element.value = null;
                    addImageHTML(element, null, 'Extensão inválida');
                }
            } else {
                element.value = null;
                addImageHTML(element, null, 'Tamanho inválido');
            }
        }
    }

    // adiciona o html de feedback (se sucesso, um preview, se erro, uma mensagem)
    addImageHTML = function(element, imageId, message) {
        var el = $(element);
        var parent = el.parent().parent();
        var container = parent.find('.image-container');
        var imageInput = parent.find('input[type=hidden]');
        container.html('');
        if (imageId) {
            imageInput.val(imageId);
            var group = $('<div/>', {
                'class': 'form-group',
            }).appendTo(container);
            var figure = $('<figure/>', {
                'class': 'previewImage',
            }).appendTo(group);
            var icon = $('<i/>', {
                'class': 'mdi mdi-close-circle closePreviewImage'
            }).appendTo(figure);
            var img = $('<img/>', {
                'src': GLOBALS.BASE_URL+'api/media/' + imageId,
                'alt': 'User Avatar'
            }).appendTo(figure);
        } else {
            var feedback = $('<span/>', {
                'class': 'invalid-feedback',
                'text': message
            }).appendTo(container);
        }
    }
});