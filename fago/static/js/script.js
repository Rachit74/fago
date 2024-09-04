function imageToggle(imageID) {
    var image = document.getElementById('post-image-' + imageID)
    var toggle_link = document.getElementById('post-toggle-link-' + imageID)


    if (image.style.display == 'none' || image.style.display == '') {
        image.style.display = 'block';
        toggle_link.innerHTML = "Hide Image";
    } else {
        image.style.display = 'none';
        toggle_link.innerHTML = "Show Image";
    };
};