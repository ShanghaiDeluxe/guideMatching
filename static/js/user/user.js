
changeImage = function (input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('div.profile-picture > img').attr('src', e.target.result);
        };
        reader.readAsDataURL(input.files[0]);
    }
};

(function ($){
    var
        initialize = function () {
            $('div.profile-picture > a.icon-camera').bind('click', addImage);
            $('div.profile-picture > a.icon-check-empty-after, div.profile-picture > a.icon-check-after')
                .bind('click', removeImage);
        },
        addImage = function (e) {
            $('input[name="profile_picture"]').trigger('click');
        },
        removeImage = function (e) {
            if ($(this).hasClass('icon-check-empty-after')) {
                $(this).removeClass('icon-check-empty-after').addClass('icon-check-after');
                $('input[name="picture_delete"]').attr('checked', true);
            } else {
                $(this).removeClass('icon-check-after').addClass('icon-check-empty-after');
                $('input[name="picture_delete"]').attr('checked', false);
            }
        }
        ;
    initialize();
})(jQuery);