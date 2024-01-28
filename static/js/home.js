var currentImageID = -1,
    canClickButtons = !0,
    currentClicks = -1,
    zoomAmount = 100;


function isMobileDevice() {
    return /Mobi|Android/i.test(navigator.userAgent);
}

function increaseZoom(){
    currentClicks++;
}

function zoom(e) {
    if (isMobileDevice()) {
        return;
    }

    var zoomer = e.currentTarget;
    
    switch(currentClicks){
        case 0:
            zoomAmount = 200;
            break;
        case 1:
            zoomAmount = 250;
            break;
        case 2:
            zoomAmount = 300;
            break;
        case 3:
            zoomAmount = 100;
            currentClicks = -1;
            break;
        default:
            zoomAmount = 100;
            currentClicks = -1;
            break;
    }

    zoomer.style.backgroundSize = zoomAmount + "% " + zoomAmount + "%";

    e.offsetX ? offsetX = e.offsetX : offsetX = e.touches[0].pageX;
    e.offsetY ? offsetY = e.offsetY : offsetX = e.touches[0].pageX;
    x = offsetX / zoomer.offsetWidth * 100;
    y = offsetY / zoomer.offsetHeight * 100;

    zoomer.style.backgroundPosition = x + "% " + y + "%";
}

function showImage(e) {
    var n = document.getElementById("image-preview-modal");
    $(".image-content").html('<span class="loading loading-ring loading-lg"></span>'), $.ajax({
        url: previewImageUrl,
        type: "GET",
        data: {
            image_id: e
        },
        success: function(e) {
            if (e.success) {
                $(".image-title").text(e.image_title);

                var imgTag = $('<img src="' + e.image_url + '" class="h-screen object-contain mx-auto" />');
                var zoomContainer = $(`<figure class="zoom" onmousemove="zoom(event)" style="height: auto; width: auto;"></figure>`);
                zoomContainer.css('background-image', 'url(' + e.image_url + ')');

                if (!isMobileDevice()) {
                    imgTag.attr('onclick', 'increaseZoom()');
                    zoomContainer.attr('onclick', 'zoom(event)');
                }

                var imgTagLoaded = new Promise((resolve) => {
                    imgTag.on('load', resolve);
                });

                var bgImageLoaded = new Promise((resolve) => {
                    $("<img/>").attr("src", e.image_url).on('load', resolve);
                });

                Promise.all([imgTagLoaded, bgImageLoaded]).then(function() {
                    zoomContainer.append(imgTag);
                    if (!isMobileDevice()) {
                        $(".image-content").html(zoomContainer);
                    }
                    else{
                        $(".image-content").html(imgTag);
                    }
                    
                    currentClicks = -1;
                });

                n.showModal();
            } else console.log("Error: " + e.error);
        },
        error: function(e) {
            console.log("AJAX error: ", e);
        }
    });
}


function getNextImageId() {
    var e = ids.indexOf(parseInt(currentImageID));
    if (-1 !== e) {
        var n = (e + 1) % ids.length;
        return ids[n]
    }
    return null
}

function getPrevImageId() {
    var e = ids.indexOf(parseInt(currentImageID));
    if (-1 !== e) {
        var n = (e - 1 + ids.length) % ids.length;
        return ids[n]
    }
    return null
}

function navigateImage(e) {
    if (canClickButtons) {
        var n = "next" === e ? getNextImageId() : getPrevImageId();
        null !== n && (currentImageID = n, showImage(n), disableButtonsTemporarily())
    }
}

function disableButtonsTemporarily() {
    canClickButtons = !1, $(".next-button, .prev-button").prop("disabled", !0), setTimeout(function() {
        canClickButtons = !0, $(".next-button, .prev-button").prop("disabled", !1)
    }, 1e3)
}
$(document).on("click", ".image-preview", function() {
    showImage(currentImageID = $(this).data("image-id"))
}), $(document).on("click", ".next-button", function() {
    navigateImage("next")
}), $(document).on("click", ".prev-button", function() {
    navigateImage("prev")
}), $(document).keydown(function(e) {
    39 === e.keyCode && navigateImage("next"), 37 === e.keyCode && navigateImage("prev")
}), document.addEventListener("DOMContentLoaded", function() {
    let e = document.querySelectorAll("img"),
        n = document.getElementById("skeleton-wrap"),
        t = 0;
    e.forEach(a => {
        let i = () => {
            ++t === e.length && setTimeout(function() {
                n.classList.add("hidden"), e.forEach(e => e.classList.remove("hidden"))
            }, 500)
        };
        a.complete ? i() : (a.addEventListener("load", i), a.addEventListener("error", i))
    })
});