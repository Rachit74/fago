function submitDeleteForm(event) {
    event.preventDefault(); // Prevent the default form submission
    
    // Get the blog ID from the hidden input
    const blogId = document.getElementById('blogId').value;

    // Send the DELETE request
    fetch(`http://localhost:8080/blogs/${blogId}`, {
        method: 'DELETE',
    })
    .then(response => {
        if (response.ok) {
            window.location.href = "/"; // Redirect after successful deletion
        } else {
            console.error('Failed to delete blog:', response.statusText);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
