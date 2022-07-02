/* api_data_handler.js
Converts so that .svelte files can access API data in a sweet and sexy way.
*/
import {writable, derived} from "svelte/store";

export const api_data = writable({})

// Some data transformation for different scenarios
export const get_api_data = derived(api_data, ($api_data) => {
    if ($api_data){
        return $api_data
    }
    return {}
})

