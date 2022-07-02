<script>
    import { onMount } from "svelte";
    import LoadingSpinner  from "$lib/LoadingSpinner.svelte";
    let media_types;
    onMount(async () => {
        await fetch("http://127.0.0.1:5000/api/available_media_types")
            .then(response => response.json())
            .then(data => {
                console.log("API data: " + JSON.stringify(data))
                media_types = data.media_types;
            }).catch(error => {
                console.log("Caught API error: " + error)
                return {};
            })
    })
</script>

<svelte:head>
    <title>Albins hemsida</title>
</svelte:head>
<body class="bg-gray-200 text-gray-400 h-screen min-h-screen flex flex-col items-center text-center place-content-center">
<div class="flex flex-col gap-y-4 text-7xl font-bold">
    {#if media_types}
    {#each media_types as media_type}
        <p><a class="hover:cursor-pointer hover:underline" href="/media/{media_type}">{media_type}</a></p>
    {/each}
    {:else}
        <svelte:component this={LoadingSpinner}></svelte:component>
    {/if}
</div>
</body>