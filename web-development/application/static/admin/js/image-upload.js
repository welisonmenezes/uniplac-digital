document.addEventListener('DOMContentLoaded', function () {

    var result = document.querySelector('.cropp-result'),
        img_result = document.querySelector('.cropp-img-result'),
        save = document.querySelector('.cropp-save'),
        cropp = document.querySelector('.cropp-cropp'),
        cropped = document.querySelector('.cropp-cropped'),
        cropper = '',
        current_el = null,
        imgSrc = null;

    // botão de upload
    $('body').on('click', '.file-upload-browse', function () {
        $('.file-upload-default').click();
    });

    // dispara envio de imagem
    $('body').on('change', '.file-upload-default', function (e) {
        current_el = $(e.target);
        if (e.target.files.length) {
            var element = e.target;
            var file = element.files[0];
            if (file && file.name) {
                var filename = file.name;
                var extension = filename.slice((filename.lastIndexOf('.') - 1 >>> 0) + 2).toLowerCase();
                var accepts = element.getAttribute('accept').split(',');
                if (file.size <= 5017969) {
                    if (accepts.indexOf('.' + extension) > -1) {

                        // faz o cropp
                        const reader = new FileReader();
                        reader.onload = (e) => {
                            if (e.target.result) {
                                let img = document.createElement('img');
                                img.id = 'image';
                                img.src = e.target.result
                                result.innerHTML = '';
                                result.appendChild(img);
                                cropp.classList.remove('cropp-hide');
                                
                                if (current_el.hasClass('img-post')) {
                                    cropper = new Cropper(img, {
                                        autoCropArea: 0,
                                        strict: false,
                                        guides: false,
                                        highlight: false,
                                        dragCrop: false,
                                        cropBoxMovable: true,
                                        cropBoxResizable: true,
                                        aspectRatio: 16 / 8
                                    });
                                } else if (current_el.hasClass('multiple')) {
                                    cropper = new Cropper(img, {
                                        autoCropArea: 0,
                                        strict: false,
                                        guides: false,
                                        highlight: false,
                                        dragCrop: false,
                                        cropBoxMovable: true,
                                        cropBoxResizable: true,
                                        aspectRatio: 16 / 4
                                    });
                                } else {
                                    cropper = new Cropper(img, {
                                        autoCropArea: 0,
                                        strict: false,
                                        guides: false,
                                        highlight: false,
                                        dragCrop: false,
                                        cropBoxMovable: true,
                                        cropBoxResizable: true,
                                        aspectRatio: 16 / 16
                                    });
                                }
                            }
                        };
                        reader.readAsDataURL(e.target.files[0]);

                    } else {
                        element.value = null;
                        if (current_el.hasClass('multiple')) {
                            addMultipleImageHTML(null, 'Extensão inválida');
                        } else {
                            addImageHTML(null, 'Extensão inválida');
                        }
                    }
                } else {
                    element.value = null;
                    if (current_el.hasClass('multiple')) {
                        addMultipleImageHTML(null, 'Tamanho inválido');
                    } else {
                        addImageHTML(null, 'Tamanho inválido');
                    }
                }
            }

        }
    });

    // cropp on click
    if (cropp) {
        cropp.addEventListener('click', (e) => {
            e.preventDefault();

            if (current_el.hasClass('img-post')) {
                imgSrc = cropper.getCroppedCanvas({
                    width: 750
                }).toDataURL();
            } else if (current_el.hasClass('multiple')) {
                imgSrc = cropper.getCroppedCanvas({
                    width: 2000
                }).toDataURL();
            } else {
                imgSrc = cropper.getCroppedCanvas({
                    width: 300
                }).toDataURL();
            }

            cropped.classList.remove('cropp-hide');
            img_result.classList.remove('cropp-hide');
            save.classList.remove('cropp-hide');
            cropped.src = imgSrc;
        });
    }

    // save on click
    if (save) {
        save.addEventListener('click', (e) => {
            //current_el = null;
            cropped.classList.add('cropp-hide');
            save.classList.add('cropp-hide');
            img_result.classList.add('cropp-hide');
            result.innerHTML = '';
            cropp.classList.add('cropp-hide');
            sendFileToServer();
        });
    }

    // close o preview de imagem
    $('body').on('click', '.closePreviewImage', function () {
        var t = $(this);
        var parent = t.parent().parent().parent().parent();
        var container = parent.find('.image-container');
        var imageInput = parent.find('input[type=hidden]');
        container.html('');
        imageInput.val('');
    });

    // close o previw de imagem quando multi
    $('body').on('click', '.closePreviewImageMulti', function () {
        var t = $(this);
        var imgId = t.attr('data-image-id');
        var parent = t.parent().parent().parent().parent();
        var li = t.parent().parent();
        var container = parent.find('.ul-fig-banner');
        var imageInput = parent.find('input[type=hidden]');
        li.remove();
        removeValueFromImagesField(imageInput, imgId);
    });


    sendFileToServer = function () {
        var el = current_el;
        var file = imgSrc;
        fetch(GLOBALS.BASE_URL + 'api/image', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ image: file })
        })
            .then(data => data.json())
            .then(data => {
                if (data && data.id) {
                    if (el.hasClass('multiple')) {
                        addMultipleImageHTML(data.id);
                    } else {
                        addImageHTML(data.id);
                    }
                } else {
                    addImageHTML(null, data.message);
                }
            }, error => {
                if (el.hasClass('multiple')) {
                    addMultipleImageHTML(null, error);
                } else {
                    addImageHTML(null, error);
                }
                element.value = null;
            });
    }

    // adiciona o html de feedback (se sucesso, um preview, se erro, uma mensagem)
    addImageHTML = function (imageId, message) {
        var el = current_el;
        el.val(null);
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
                'src': GLOBALS.BASE_URL + 'api/media/' + imageId,
                'alt': 'User Avatar'
            }).appendTo(figure);
        } else {
            var feedback = $('<span/>', {
                'class': 'invalid-feedback',
                'text': message
            }).appendTo(container);
        }
    }

    // adiciona html de feedback (se sucesso, um preview, se error, a mensagem)
    addMultipleImageHTML = function (imageId, message) {
        var el = current_el;
        el.val(null);
        var parent = el.parent().parent().parent();
        var container = parent.find('.ul-fig-banner');
        var errorContainer = parent.find('.errorContainer');
        var imageInput = parent.find('input[type=hidden]');
        errorContainer.html('');
        if (imageId) {
            addNewValueToImagesField(imageInput, imageId);
            var li = $('<li/>').appendTo(container);
            var fig = $('<figure/>', {
                'class': 'fig-banner',
            }).appendTo(li);
            var icon = $('<i/>', {
                'class': 'mdi mdi-close-circle closePreviewImageMulti',
                'data-image-id': imageId
            }).appendTo(fig);
            var img = $('<img/>', {
                'src': GLOBALS.BASE_URL + 'api/media/' + imageId,
                'alt': 'User Avatar'
            }).appendTo(fig);
        } else {
            var feedback = $('<span/>', {
                'class': 'invalid-feedback',
                'text': message
            }).appendTo(errorContainer);
        }
    }

    // adiciona um dado valor no 'array' de value
    addNewValueToImagesField = function (imgInput, value) {
        var str = imgInput.val();
        str = str.replace('[', '').replace(']', '').replace(' ', '');
        var strArr = str.split(',').filter(function (el) {
            return el != '';
        });
        strArr.push(value);
        var newVal = '[' + strArr.join(',') + ']';
        imgInput.val(newVal);
    }

    // remove um dado valor do 'array' de value
    removeValueFromImagesField = function (imageInput, imgId) {
        var str = imageInput.val();
        str = str.replace('[', '').replace(']', '').replace(' ', '');
        var strArr = str.split(',').filter(function (el) {
            return el != '';
        });
        strArr = strArr.filter(function (el) {
            console.log(el, imgId)
            return el != imgId;
        });
        var newVal = '[' + strArr.join(',') + ']';
        imageInput.val(newVal);
    }

});