var currentImageID=-1,canClickButtons=!0,currentClicks=-1,zoomAmount=100,currentAjaxRequest=null;function isMobileDevice(){return/Mobi|Android/i.test(navigator.userAgent)}function increaseZoom(){currentClicks++}function zoom(e){if(!isMobileDevice()){var t=e.currentTarget;switch(currentClicks){case 0:zoomAmount=200;break;case 1:zoomAmount=250;break;case 2:zoomAmount=300;break;default:zoomAmount=100,currentClicks=-1}t.style.backgroundSize=zoomAmount+"% "+zoomAmount+"%",offsetX=e.offsetX?e.offsetX:e.touches[0].pageX,e.offsetY?offsetY=e.offsetY:offsetX=e.touches[0].pageX,x=offsetX/t.offsetWidth*100,y=offsetY/t.offsetHeight*100,t.style.backgroundPosition=x+"% "+y+"%"}}function showImage(e){currentAjaxRequest&&currentAjaxRequest.abort();var t=document.getElementById("image-preview-modal");$(".image-content").html('<span class="loading loading-ring loading-lg"></span>'),currentAjaxRequest=$.ajax({url:previewImageUrl,type:"GET",data:{image_id:e},success:function(e){if(e.success){$(".image-title").text(e.image_title);var n=$('<img src="'+e.image_url+'" class="h-screen object-contain mx-auto" />'),o=$('<figure class="zoom" onmousemove="zoom(event)" onmouseover="zoom(event)" style="height: auto; width: auto;"></figure>');o.css("background-image","url("+e.image_url+")"),isMobileDevice()||(n.attr("onclick","increaseZoom()"),o.attr("onclick","zoom(event)"));var a=new Promise(e=>{n.on("load",e)}),r=new Promise(t=>{$("<img/>").attr("src",e.image_url).on("load",t)});Promise.all([a,r]).then(function(){o.append(n),isMobileDevice()?$(".image-content").html(n):$(".image-content").html(o),currentClicks=-1}),t.showModal()}else console.log("Error: "+e.error)},error:function(e){console.log("AJAX error: ",e)}})}function abortAjaxRequest(){currentAjaxRequest&&currentAjaxRequest.abort()}function getNextImageId(){var e=ids.indexOf(parseInt(currentImageID));if(-1!==e){var t=(e+1)%ids.length;return ids[t]}return null}function getPrevImageId(){var e=ids.indexOf(parseInt(currentImageID));if(-1!==e){var t=(e-1+ids.length)%ids.length;return ids[t]}return null}function navigateImage(e){if(canClickButtons){var t="next"===e?getNextImageId():getPrevImageId();null!==t&&(currentImageID=t,showImage(t),disableButtonsTemporarily())}}function disableButtonsTemporarily(){canClickButtons=!1,$(".next-button, .prev-button").prop("disabled",!0),setTimeout(function(){canClickButtons=!0,$(".next-button, .prev-button").prop("disabled",!1)},1e3)}$(document).on("click",".btn-close-modal",abortAjaxRequest),$(document).on("click",".image-preview",function(){showImage(currentImageID=$(this).data("image-id"))}),$(document).on("click",".next-button",function(){navigateImage("next")}),$(document).on("click",".prev-button",function(){navigateImage("prev")}),$(document).keydown(function(e){39===e.keyCode&&navigateImage("next"),37===e.keyCode&&navigateImage("prev")}),document.addEventListener("DOMContentLoaded",function(){let e=document.querySelectorAll("img"),t=document.getElementById("skeleton-wrap"),n=0;e.forEach(o=>{let a=()=>{++n===e.length&&setTimeout(function(){t.classList.add("hidden"),e.forEach(e=>e.classList.remove("hidden"))},500)};o.complete?a():(o.addEventListener("load",a),o.addEventListener("error",a))})});