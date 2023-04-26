$('.btn-open').each(function() {
    var modalID = $(this).attr('href');
    var modalBg = $('.modal-bg');
  
    $(this).on('click', function(e) {
      e.preventDefault();

      modalBg.fadeIn();
      
      $(modalID).show();

      $('html').css({overflow: 'hidden'});
    });

    $('.modal-bg, .modal-close').on('click', function() {
      modalBg.fadeOut();
      $(modalID).hide();
      $(modalID).removeAttr('style');

      $('html').removeAttr('style');
    });
  });