/*
api_responses.json
Library for generating API responses.
*/

API_STATUS_SUCCESS = "success"
API_STATUS_ERROR = "error"

function generate_api_response(data, status=API_STATUS_SUCCESS, status_code=200){
    // Function for generating an API response.
    data.status =  {
            type: status,
            code: status_code
    }
    return data
}

function generate_api_error(status_code, message){
    // Shortcut function to generate an API error.
    return generate_api_response({"message": message}, API_STATUS_ERROR, status_code)
}

function validate_json_present_keys(json_obj, required_keys){
    // Validates that certain keys exist in a JSON object
    console.log("Validating JSON keys in an object...")
    let found_keys = 0
    Object.keys(json_obj).forEach(key => {
        if (required_keys.includes(key)){
            found_keys += 1
        }})
    if (found_keys >= required_keys.length){
        console.log("Found required keys.")
        return true
    }
    else {
        console.log("Did not find required keys.")
        return false
    }
}

module.exports = { generate_api_response, generate_api_error, validate_json_present_keys }