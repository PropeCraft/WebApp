$(document).ready(function () {
    // Init
    $('.image-section').hide();
    $('.loader').hide();
    $('#result').hide();

    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').attr('src', e.target.result);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }

    function formatResult(data) {
    let result;
    for (let key in data) {
        if (Array.isArray(data[key])) {
            result += `**${key}:**\n\n`;
            data[key].forEach(item => {
                result += `* ${item}\n`;
            });
            result += "\n";
        } else {
            result += `**${key}:** ${data[key]}\n\n`;
        }
    }
    return result;
}

    $("#imageUpload").change(function () {
        $('.image-section').show();
        $('#btn-predict').show();
        $('#result').text('');
        $('#result').hide();
        readURL(this);

        var formData = new FormData();
        formData.append('image', this.files[0]);
        $.ajax({
            type: 'POST',
            url: '/upload',
            data: formData,
            contentType: false,
            cache: false,
            processData: false,
            success: function (data) {
                console.log(data);
            },
            error: function (err) {
                console.error(err);
            }
        });
    });

    // Predict
    $('#btn-predict-makeover').click(function () {
        var form_data = new FormData($('#upload-file')[0]);
        $(this).hide();
        $('.loader').show();
        $.ajax({
            type: 'POST',
            url: '/makeover_recommendations',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                $('.loader').hide();
                $('#result').fadeIn(600);
            let formattedResult = formatResult(data);
            $('#result').append(formattedResult);
            },
        });
    });
    $('#btn-predict-balcony').click(function () {
        var form_data = new FormData($('#upload-file')[0]);
        $(this).hide();
        $('.loader').show();
        $.ajax({
            type: 'POST',
            url: '/balcony_recommendations',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                $('.loader').hide();
                $('#result').fadeIn(600);
                let formattedResult = formatResult(data);
                $('#result').append(formattedResult);
            },
        });
    });

    $('#btn-predict-paints').click(function () {
        var form_data = new FormData($('#upload-file')[0]);
        $(this).hide();
        $('.loader').show();
        $.ajax({
            type: 'POST',
            url: '/painting_recommendations',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                $('.loader').hide();
                $('#result').fadeIn(600);
                let formattedResult = formatResult(data);
                $('#result').append(formattedResult);
            },
        });
    });

    $('#btn-predict-gardening').click(function () {
        var form_data = new FormData($('#upload-file')[0]);
        $(this).hide();
        $('.loader').show();
        $.ajax({
            type: 'POST',
            url: '/gardening_recommendations',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                $('.loader').hide();
                $('#result').fadeIn(600);
                let formattedResult = formatResult(data);
                $('#result').append(formattedResult);
            },
        });
    });
});
