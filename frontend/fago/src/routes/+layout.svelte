<script>
    import Header from "../lib/components/Header.svelte";
    import '$lib/styles/styles.css';
</script>

<Header></Header>

<main>
    <slot></slot>
</main>