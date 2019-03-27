// create.html & update.html JS ////////////////////////////////////////////////////////////////////////////////////////////////////
//The Begin

var imageCount = 0;
var uniqId = "";

// Add image to ad on submit
$('#ad_image_submit_btn').click(function (event) {

    imageCount++;

    if (imageCount > 6) {
        $('#ad_image_submit_btn').attr('disabled', true);
    };
    event.preventDefault();
    addImageAd();
});


$('#remove_image_submit_btn').click(function (event) {

    event.preventDefault();
    if (imageCount > 0) {
        var $div = $('#ad_image_add_div_' + imageCount);
        $div.remove();
        imageCount--;
    };

    if (imageCount < 7) {
        $('#ad_image_submit_btn').attr('disabled', false);
    };

});


function addImageAd() {

    var $newImage = $('#ad_image_add_div_0').clone();

    $newImage.attr("id", "ad_image_add_div_" + imageCount);
    // set input id and name attrs
    $newImage.find("#id_form-0-img").attr("id", "id_form-" + imageCount + "-img");
    $newImage.find("#id_form-" + imageCount + "-img").attr("name", "form-" + imageCount + "-img");
    $newImage.find("#id_form-" + imageCount + "-img").val("");
    $newImage.find(".custom-file-label").html("");
    // set hidden input id and name attrs
    $newImage.find("#id_form-0-id").attr("id", "id_form-" + imageCount + "-id");
    $newImage.find("#id_form-" + imageCount + "-id").attr("name", "form-" + imageCount + "-id");
    // set label for attr
    $newImage.find(".custom-file-label").attr("for", "id_form-" + imageCount + "-img");


    $("#images_list_div").append($newImage);

    $("#id_form-" + imageCount + "-img").on('change', function () {

        var fileName = $(this).val();

        $(this).next(".custom-file-label").html(fileName);

        var inputValue = $("#id_form-" + imageCount + "-img").val();

    });

};
//The End
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


$(document).ready(function () {
// create.html & update.html JS //////////////////////////////////////////////
//The Begin


    $("#id_form-" + imageCount + "-img").on('change', function () {

        var fileName = $(this).val();

        $(this).next(".custom-file-label").html(fileName);

        $("#ad_image_add_div_" + imageCount).find(".custom-file-label").html(fileName);

    });

//The End
///////////////////////////////////////////////////////////////////////////////////
});