var currentImageID = -1;
var canClickButtons = true;

$(document).on('click', '.image-preview', function() {
    var image_id = $(this).data('image-id');
    currentImageID = image_id;
    showImage(currentImageID);
});

function showImage(image_id) {
    var previewModal = document.getElementById('image-preview-modal');

    $('.image-content').html('<span class="loading loading-ring loading-lg"></span>');

    $.ajax({
        url: previewImageUrl,
        type: "GET",
        data: { 'image_id': image_id },
        success: function(response) {
            if(response.success) {
                $('.image-title').text(response.image_title);

                var img = $('<img src="' + response.image_url + '" class="h-screen object-contain mx-auto">');

                img.on('load', function() {
                    setTimeout(function() {
                        $('.image-content').html(img);
                    }, 500);
                });

                previewModal.showModal();
            } else {
                console.log('Error: ' + response.error);
            }
        },
        error: function(error) {
            console.log('AJAX error: ', error);
        }
    });
}
function getNextImageId() {
    var currentIndex = ids.indexOf(parseInt(currentImageID));
    if (currentIndex !== -1) {
        var nextIndex = (currentIndex + 1) % ids.length;
        return ids[nextIndex];
    }
    return null;
}

function getPrevImageId() {
    var currentIndex = ids.indexOf(parseInt(currentImageID));
    if (currentIndex !== -1) {
        var prevIndex = (currentIndex - 1 + ids.length) % ids.length;
        return ids[prevIndex];
    }
    return null;
}

function navigateImage(direction) {
    if (canClickButtons) {
        var imageId = direction === 'next' ? getNextImageId() : getPrevImageId();
        if(imageId !== null) {
            currentImageID = imageId;
            showImage(imageId);
            disableButtonsTemporarily();
        }
    }
}

$(document).on('click', '.next-button', function() {
    navigateImage('next');
});

$(document).on('click', '.prev-button', function() {
    navigateImage('prev');
});


$(document).keydown(function(e) {
    if (e.keyCode === 39) {
        navigateImage('next');
    }
    if (e.keyCode === 37) { // 
        navigateImage('prev');
    }
});

function disableButtonsTemporarily() {
    canClickButtons = false; 
    $('.next-button, .prev-button').prop('disabled', true); 
    setTimeout(function() {
        canClickButtons = true;
        $('.next-button, .prev-button').prop('disabled', false);
    }, 1000);
}

document.addEventListener("DOMContentLoaded", function() {
    const images = document.querySelectorAll('img');
    const skeletonWrap = document.getElementById('skeleton-wrap');
    let imagesLoaded = 0;

    images.forEach(img => {
        const checkAllImagesLoaded = () => {
            imagesLoaded++;

            if (imagesLoaded === images.length) {
                setTimeout(function() {
                    skeletonWrap.classList.add('hidden');
                    images.forEach(image => image.classList.remove('hidden'));
                }, 500);
            }
        };

        if (img.complete) {
            checkAllImagesLoaded();
        } else {
            img.addEventListener('load', checkAllImagesLoaded);
            img.addEventListener('error', checkAllImagesLoaded);
        }
    });
});