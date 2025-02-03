$(document).on('click', '.like-btn', function () {
    const likeButton = $(this);
    const postId = likeButton.data('post-id');
    const likesCount = likeButton.closest('.like-container').find('.like-count');

    function getCSRFToken() {
        return document.cookie.split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
    }

    likeButton.prop('disabled', true);  // Deshabilitar mientras procesa

    $.ajax({
        url: `/post/${postId}/like/`,
        method: 'POST',
        headers: { "X-CSRFToken": getCSRFToken() },  // CSRF correcto
        success: function (response) {
            if (response.liked) {
                likeButton.text('Unlike');
            } else {
                likeButton.text('Like');
            }
            likesCount.text(response.likes_count);
        },
        complete: function () {
            likeButton.prop('disabled', false);  // Habilitar de nuevo
        }
    });
});
