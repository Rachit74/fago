
// script to toggle the comment box on read-post page
function commentBoxToggle() {
    var commentBox = document.getElementById("comment-box");
    if (commentBox.style.display === "none" || commentBox.style.display === "") {
        commentBox.style.display = "block"; // Show the comment box
    } else {
        commentBox.style.display = "none"; // Hide the comment box
    }
}

// Toggle reply box
function replyBoxToggle(commentID) {
    var replyBox = document.getElementById("reply-box-" + commentID);

    if (replyBox.style.display === "none" || replyBox.style.display === "") {
        replyBox.style.display = "block";
    } else {
        replyBox.style.display = "none";
    }
}

// post image toggle
function imageToggle(postId) {
    var image = document.getElementById("post-image-" + postId);
    var link = document.getElementById("image-toggle-link-" + postId);

    if (image.style.display === "block") {
        image.style.display = "none";
        link.innerHTML = "Show Image";
    } else {
        image.style.display = "block";
        link.innerHTML = "Collapse Image";
    }
}