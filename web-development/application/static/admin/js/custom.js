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

    // mascara para campos de data
    var inpDate = document.querySelectorAll('.mask-date');
    if (inpDate) {
        inpDate.forEach(function(el) {
            VMasker(el).maskPattern('99-99-9999 99:99:99');
        });
    }


    // input datepicker
    if ($('input.date, .input-group.date').length) {
        $('input.date, .input-group.date').datetimepicker({
            format: 'DD-MM-YYYY HH:mm:ss'
        });
    }
    

});