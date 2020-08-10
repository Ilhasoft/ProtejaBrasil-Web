/**
 * Created by teehamaral on 21/09/15.
 */

$(document).ready(function () {
    var SPMaskBehavior = function (val) {
            return val.replace(/\D/g, '').length === 11 ? '(00) 0 0000-0000' : '(00) 0000-00009';
        },
        spOptions = {
            onKeyPress: function (val, e, field, options) {
                field.mask(SPMaskBehavior.apply({}, arguments), options);
            }
        };

    $('.telefone').mask(SPMaskBehavior, spOptions);
    $('.celular').mask(SPMaskBehavior, spOptions);
    $('.cep').mask('00000-000');

    $('.geoposition-search input').attr('placeholder', 'Comece inserindo um endereço');
    $('.geoposition-search input').addClass('form-control');
    $('.geoposition').addClass('form-control').attr('required', '');

    $('input.datefield').datepicker({
        format: "dd/mm/yyyy",
        autoclose: true,
        todayHighlight: true,
        language: 'pt-BR'
    });

});
