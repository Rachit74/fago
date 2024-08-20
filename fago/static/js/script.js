document.addEventListener('DOMContentLoaded', function () {
    // Get all reply buttons
    const replyButtons = document.querySelectorAll('.reply-button');
    
    replyButtons.forEach(button => {
        button.addEventListener('click', function () {
            // Get the corresponding reply form
            const postId = this.getAttribute('data-post-id');
            const replyForm = document.getElementById(`reply-form-${postId}`);
            
            // Toggle the display of the reply form
            if (replyForm.style.display === 'none') {
                replyForm.style.display = 'block';
            } else {
                replyForm.style.display = 'none';
            }
        });
    });
});
