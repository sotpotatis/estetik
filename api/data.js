/*
data.js
Contains some functions related to reading data such as segment defintiions, images, etc.
*/
const fs = require("fs") // Used for reading from files
const path = require("path") // Used for paths

const VALID_MEDIA_TYPES = ["images", "sounds", "text"]
const CONTENT_BASE_PATH = path.join(__dirname, "content") // Base folder for content
const ALLOWED_AUTH_TOKENS_PATH = path.join(__dirname, "authorized_tokens.json") // Authorized auth tokens
media_type_paths = {}

function load_json_from_filepath(filepath){
    // Loads JSON from a filepath
    console.log(`Reading JSON from ${filepath}`)
    let file_content = fs.readFileSync(filepath);
    return JSON.parse(file_content)
}

function write_json_to_filepath(filepath, new_json){
    // Writes JSON to a filepath
    console.log(`Writing JSON to ${filepath}...`)
    fs.writeFileSync(filepath, JSON.stringify(new_json, null, 2)) // Adding null, 2 creates an indented JSON - nice!
}

function get_structure_filepath(media_type){
    // Gets the filepath to a structure.json file for a certain content type
    media_type = media_type.toLowerCase()
    // Validate media type
    if (!VALID_MEDIA_TYPES.includes(media_type)){
        throw new DOMException("Invalid media type.")
    }
    return path.join(CONTENT_BASE_PATH, media_type, "/structure.json")
}
function get_structure_for(media_type){
    // Returns the structure definition for a media_type.
    media_type = media_type.toLowerCase();
    structure_file_path = get_structure_filepath(media_type)
    console.log(`Returning structure for ${media_type} (${structure_file_path})...`)
    return load_json_from_filepath(structure_file_path)
}

function update_structure_for(media_type, new_structure_content){
    // Updates the structure.json definition file for a certain media type
    media_type = media_type.toLowerCase();
    console.log(`Updating structure for media type ${media_type}...`)
    write_json_to_filepath(get_structure_filepath(media_type), new_structure_content)
    console.log(`Structure for ${new_structure_content} updated.`)
}

function get_media_file_path(media_type, media_name){
    // Function for getting a media file that is in a certain type directory.
    // For now, the media files are (most likely) only going to be images
    console.log(`Getting media ${media_name} from ${media_type}...`)
    let media_path = path.join(CONTENT_BASE_PATH, media_type, `/${media_name}`)
    console.log(`Path is ${media_path}.`)
    return media_path
}

function get_allowed_access_tokens(){
    // Function for getting access tokens that are allowed to access the server.
    return load_json_from_filepath(ALLOWED_AUTH_TOKENS_PATH).tokens
}

// To make sure functions are available when importing this, we have to export all defined functions
module.exports = { write_json_to_filepath, get_structure_for, VALID_MEDIA_TYPES, CONTENT_BASE_PATH, get_media_file_path, get_allowed_access_tokens, update_structure_for, get_structure_filepath }