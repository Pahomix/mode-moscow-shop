$(document).ready(function() {
    $('.update-form select').change(function() {
        var form = $(this).closest('form');
        var url = form.data('url');
        var quantity = $(this).val();
        $.ajax({
            url: url,
            method: 'POST',
            data: {
                'csrfmiddlewaretoken': '{{ csrf_token }}',
                'quantity': quantity,
                'update': true
            },
            success: function(response) {
                location.reload();  // Reload the page to update the cart
            },
            error: function(xhr, errmsg, err) {
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    });
});