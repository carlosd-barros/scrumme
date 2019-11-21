(function ($) {
    $('input[data-toggle="datetimepicker"]').each(function () {
        var date = moment($(this).val(), ['DD/MM/YYYY', 'DD/MM/YYYY HH:mm', 'YYYY-MM-DD', 'YYYY-MM-DD HH:mm']);
        var format = $(this).data('format') ? $(this).data('format') : 'L LT';
    
        if (!date.isValid()) {
            date = moment();
        }
    
        $(this).datetimepicker({
            date: date,
            sideBySide: true,
            locale: 'pt-br',
            format: format,
        });
    });
  })(jQuery);
  