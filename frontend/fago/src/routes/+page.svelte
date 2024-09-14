<script>
    let posts = []

    const getRecentPosts = async () => {
        try {
            let response = await fetch('http://localhost:8000/api/posts/');
            if (!response.ok) {
                console.log("Unable to fetch!");
            };
            let data = await response.json();
            posts = data;
        } catch (error) {
            console.log(error);
            
        }
    }
    getRecentPosts();
</script>
<h2>Recent Posts</h2>