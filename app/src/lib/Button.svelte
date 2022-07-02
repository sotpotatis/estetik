<script>
    export let data;
</script>

<button class="bg-{data.color} font-{data.text_font} text-{data.text_color} border-2 rounded border-{data.border_color} pl-3 pr-3 pl-1 pt-1 font-bold" onclick="location.href='{data.url}'">{data.text}</button>
