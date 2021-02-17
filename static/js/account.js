$('#id_profile').on('click', function() {
    window.history.pushState({}, "", "/account/setting/");
})

$('#id_review').on('click', function() {
    window.history.pushState({}, "", "/account/my-list/");
})

