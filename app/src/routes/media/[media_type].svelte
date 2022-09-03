<script>
    import {page} from "$app/stores"
    import {onMount} from "svelte";
    import LoadingSpinner from "$lib/LoadingSpinner.svelte";
    import Icon from '@iconify/svelte'
    import Text from '$lib/Text.svelte';
    import Button from '$lib/Button.svelte'
    import { API_STRUCTURE_BASE_URL } from '../../lib/APIRoutes.js'
    let media_type = $page.params.media_type
    console.log(`Requested media type: ${media_type}`)
    let api_url = API_STRUCTURE_BASE_URL + encodeURIComponent(media_type)
    let structure;
    let covering_image; // The image that is used to examine other images
    let covering_image_container;
    console.log(`Fetching ${api_url}...`)
    onMount(async () => {
        await fetch(api_url)
            .then(response => response.json())
            .then(data => {
                console.log("Got data from API: " + JSON.stringify(data))
                structure = data.content;

            }).catch(error => {
                console.log("Error from API: "  + error)
                structure = {};
            })
    })
    // Other UI functions
    const enlarge_minify_image = (event) => {
        let element = event.target
        console.log(`Enlarging or minifying image for ${element}...`)
        // Check if image is enlarged or minified
        let enlarged = !covering_image_container.classList.contains("hidden")
        // Get covering image
        if (enlarged){
            console.log("Minimizing image...")
            covering_image_container.classList.add("hidden")
        }
        else {
            console.log("Enlarging image...")
            let source = element.src
            console.log(`New image URL: ${source}`)
            covering_image.src = source // Set image source to match
            covering_image_container.classList.remove("hidden")
        }
    }
</script>
<svelte:head>
    <title>{media_type} - estetik.albins.website</title>
</svelte:head>
<body class="bg-gray-200 z-10 font-serif text-gray-400 scroll-smooth text-center min-h-screen flex flex-row place-content-center text-center">
{#if structure}
    <div>
        <!-- Part navigation -->
        <div class="text-sm flex flex-row text-center gap-x-5">
        <p>quickly navigate: {#each structure.parts as part}<a href="#{part.id}-segments" class="hover:cursor-pointer hover:underline mr-5">{part.title}</a>{/each}</p>
    </div>
            <!-- Test - Covering image -->
        <div id="covering-image" class="w-screen h-screen sticky top-0 z-0 flex flex-row place-content-center hidden" bind:this={covering_image_container} style="background-image: url('/static/artdisplay.png')">
            <img class="border-gray-100 border-4 h-auto" src="" bind:this={covering_image}>
            <span id="covering-image-icon-container" data-enlarged="true" on:click={enlarge_minify_image}><Icon class="text-3xl text-gray-400" icon="maki:cross"/></span>
        </div>

    {#each structure.parts as part}
        <h1 class="text-5xl font-bold italic">{part.title}</h1>
        <p class="text-lg">{part.description}</p>
        <hr class="w-75 text-gray-300">
        <!-- Segments -->
        <div id="{part.id}-segments" class="grid grid-cols-1 sm:grid-cols-3">
        {#each part.segments as segment}
            <div class="p-12 h-full min-h-full">
            {#if segment.segment_type === "media"}
            <!-- Media segment type - Image -->
                <img class="border-gray-100 border-4 object-cover h-full" id="{segment.id}" src={segment.media_url} data-enlarged="false" data-parent="{part.id}-segments" on:click={enlarge_minify_image}>
                {#if segment.text}
                    {#each segment.text as text}
                        <Text data={text}/>
                    {/each}
                {/if}
                {:else if segment.segment_type === "text"}
                    <!-- Media segment type - Text -->
                    {#each segment.text as text}
                    <Text data={text}/>
                    {/each}
                {:else if segment.segment_type === "divider"}
                    <!-- Media segment type - Divider -->
                    <hr class="text-gray-500 {segment.classes}">
                {:else if segment.segment_type === "empty"}
                <!-- Media segment type - Empty -->
                {:else if segment.segment_type === "button"}
                        <!-- Media segment type - button -->
                        <Button data={segment}/>
                {/if}

            </div>
        {/each}
        </div>
    {/each}
    </div>
{:else}
<svelte:component this={LoadingSpinner}></svelte:component>
{/if}
</body>