(function ($){
    var
        initialize = function () {
            $('div.profile-picture > a.icon-camera').bind('click', addImage);
            $('div.profile-picture > a.icon-check-empty, div.profile-picture > a.icon-check')
                .bind('click', removeImage);
        },
        addImage = function (e) {
            $('input[name="profile_picture"]').trigger('click');
        },
        removeImage = function (e) {
            if ($(this).hasClass('icon-check-empty')) {
                $(this).removeClass('icon-check-empty').addClass('icon-check');
                $('input[name="picture_delete"]').attr('checked', true);
            } else {
                $(this).removeClass('icon-check').addClass('icon-check-empty');
                $('input[name="picture_delete"]').attr('checked', false);
            }
        }
        ;
    initialize();
})(jQuery);