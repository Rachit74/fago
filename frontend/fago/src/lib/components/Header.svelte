<script>
    let isNavVisible = false;

    function toggleNav() {
        isNavVisible = !isNavVisible;
    }
</script>

<style>
    .navbar {
        display: none;
    }
    .navbar.visible {
        display: block;
    }
</style>

<a href="#" on:click|preventDefault={toggleNav} class="toggleNavbar">Navigation</a>
<nav class="navbar {isNavVisible ? 'visible' : ''}">
    <ul>
        <li><a href="">Home</a></li>
        <li><a href="">Post</a></li>
        <li><a href="">Communities</a></li>
    </ul>
</nav>
