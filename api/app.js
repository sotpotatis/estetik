/* app.js
The main app.
TODO: Fix status codes
*/

// Imports
const express = require("express") // Express - for serving the web app
const data = require("./data")
const cors = require("cors")
const multer = require("multer") // Multer - for handling posted multipart form
const body_parser = require("body-parser") // body-parser - for parsing JSON bodies
const api_responses = require("./api_responses")
const fs = require("fs") // fs - for reading file storage
const path = require("path")
const {generate_api_error, generate_api_response} = require("./api_responses");
const {update_structure_for} = require("./data");
const {json} = require("express");

// Constants
const SERVER_PORT = parseInt(process.env.ESTETIK_SERVER_PORT, 10)
const SERVER_BASE_URL = process.env.ESTETIK_SERVER_BASE_URL // Base URL that the server is accessible at
const ALLOWED_UPLOAD_FILE_EXTENSIONS = [".jpg", ".png"]

// Image upload things
const image_upload = multer({dest: path.join(data.CONTENT_BASE_PATH, "images") })

// App stuff
const app = express() // create an handler for the app
// Specify use of JSON
app.use(express.json())
app.use(express.urlencoded({ extended: true }))
app.use(body_parser.json())
// Specify use of CORS
app.use(cors())
app.get("/", (req, res) => {
    console.log("Got a request to the index!")
    return res.sendStatus(419)
})

app.get("/api/structure/:media_type", (req, res)=>{
    const media_type = req.params.media_type.toLowerCase()
    console.log(`Received a request to the structure with the media type ${media_type}`)
    if (!data.VALID_MEDIA_TYPES.includes(media_type)){
        console.log("Invalid media type - returning error...")
        return res.send(api_responses.generate_api_error(
            419,
            "Invalid media type."
        ))
    }
    else { // If valid media type - return structure definition
        let structure_content = data.get_structure_for(media_type)
        structure_content.parts.forEach(part => {
            part.segments.forEach(segment => {
                if (segment.media_url !== undefined){
                    segment.media_url = SERVER_BASE_URL + segment.media_url
                }
            })
        })
        return res.send(
            api_responses.generate_api_response(
                {
                    content: structure_content
                }
            )
        )

    }
})

app.get("/api/content/:media_type/:item_name", (req, res) => {
    console.log("Got a request to return content.")
    // Get media type and item name
    let media_type = req.params.media_type.toLowerCase()
    let item_name = req.params.item_name.toLowerCase()
    if (!data.VALID_MEDIA_TYPES.includes(media_type)){
        console.log("Invalid media type - returning error...")
        return res.send(api_responses.generate_api_error(
            419,
            "Invalid media type."
        ))
    }
    else {
        console.log("Valid media type, validating item name...")
        if (item_name.includes("/")){
            console.log(`Suspected hack attempt with path ${item_name}, forbidding...`)
            return res.send(api_responses.generate_api_error(
                400,
                "Request blocked by pattern."
            ))
        }
        else {
            let item_path = data.get_media_file_path(media_type, item_name)
            if (fs.existsSync(item_path)){
                return res.sendFile(item_path)
            }
            else {
                console.log(`Error! Requested path does not exist (requested ${item_name})`)
                return res.send(api_responses.generate_api_error(
                    404,
                    "The requested item was not found."
                ))
            }
        }
    }
})

app.get("/api/available_media_types", (req, res) => {
    console.log("Got a request to the available media types API! Returning response...")
    return res.send(api_responses.generate_api_response(
        {
            media_types: data.VALID_MEDIA_TYPES
        }
    ))
})

app.post("/api/add_image",  image_upload.single("image"), (req, res) => {
    console.log("Got a request to add an image. Validating token...")
    let access_token = req.query.access_token;
    if (access_token === undefined){
        console.log("Error! Token was not set.")
        return res.send(
            api_responses.generate_api_error(
                401,
                "No auth token was provided in the request."
            )
        )
    }
    else if (!data.get_allowed_access_tokens().includes(access_token)){
        console.log(`Error! Received a non-authorized access token: ${access_token}.`)
        return res.send(
            api_responses.generate_api_error(
                403,
                "You are not permitted to access this resource."
            )
        )
    }
    else {
        console.log("Auth token was ok, validating other parameters...")
        // Get title and description
        let title = req.query.title
        let description = req.query.description
        let image_id = req.query.image_id
        let target_part_id = req.query.target_part_id // The part that the image should be added to
        if (title === undefined || description === undefined || image_id === undefined){
            console.log("Title or description is undefined. Returning error...")
            return res.send(
                api_responses.generate_api_error(
                    400,
                    "Title or description is undefined."
                )
            )
        }
        console.log("Title, description and ID exists.")
        if (image_id.includes(" ")){
            console.log("Image ID contains space. Returning error...")
            return res.send(generate_api_error(
                400,
                "Image ID contains a space. Please use a separator (for example _) instead."
            ))
        }
        // Update structure
        let previous_structure = data.get_structure_for("images")
        let new_item_structure = {
        "segment_type": "media",
          "media_url": undefined,
          "text": [{
            "font": "serif-modified",
            "value": title,
            "size": "4xl"
          },
          {
            "font": "serif-modified",
            "value": description,
            "size": "2xl"
          }]
        }
        console.log("Getting uploaded image...")
        const temporary_image_path = req.file.path;
        let file_extension = path.extname(req.file.originalname) // Get file extension of uploaded file
        console.log(`Original name: ${req.file.originalname}`)
        if (!ALLOWED_UPLOAD_FILE_EXTENSIONS.includes(file_extension)){
            console.log(`Error: Non-allowed file extension ${file_extension}!`)
            return res.send(generate_api_error(
                400,
                "Invalid file extension. Not accepted by the server."
            ))
        }
        let target_file_name = image_id + file_extension
        let target_file_path = path.join(data.get_media_file_path("images", target_file_name))
        console.log(`Saving image from temporary file path ${temporary_image_path} to ${target_file_path}...`)
        fs.renameSync(temporary_image_path, target_file_path)
        console.log("Image saved.")
        new_item_structure.media_url = `/api/content/images/${target_file_name}`
        // Find part index
        let parts_index = null
        let i = 0
        previous_structure.parts.forEach(part => {
            if (part.id === target_part_id){
                parts_index = i;
            }
            i += 1
        })
        if (parts_index === null){
            return res.send(generate_api_error(
                400,
                "A part with the requested index could not be found."
            ))
        }
        previous_structure.parts[parts_index].segments.push(new_item_structure)
        console.log("Updating structure definition file...")
        update_structure_for("images", previous_structure)
        console.log("Structure definition file updated.")
        // Return that the update was successful
        return res.send(
            generate_api_response({
                message: "Update was successful. Item has been added."
            })
        )
    }
})

app.post("/api/:media_type/parts/add", (req, res) => {
    console.log("Got a request to add a new part for a media type!")
    let media_type = req.params.media_type.toLowerCase();
    // Validate access token
    let access_token = req.query.access_token;
    if (access_token === undefined){
      console.log("Error! Token was not set.")
        return res.send(
            api_responses.generate_api_error(
                401,
                "No auth token was provided in the request."
            )
        )
    }
    else if (!data.get_allowed_access_tokens().includes(access_token)){
        console.log(`Error! Received a non-authorized access token: ${access_token}.`)
        return res.send(
            api_responses.generate_api_error(
                403,
                "You are not permitted to access this resource."
            )
        )
    }
    else {
        console.log("Access token is valid! Validating other parameters...")
        // Get data of the new part that is being created
        let json_body = req.body;
        // Validate JSON body
        if (!api_responses.validate_json_present_keys(json_body, ["title", "description", "id", "segments"])){
            console.log("JSON keys not found, returning error...")
            return res.send(api_responses.generate_api_error(
                400,
                "Required JSON keys missing in your request."
            ))
        }
        console.log("JSON keys were found. Adding to media...")
        let previous_media_structure = data.get_structure_for(media_type)
        // Check that ID is unique
        let previous_ids = []
        json_body.id = json_body.id.toLowerCase() // Convert current ID to lowercase
        previous_media_structure.parts.forEach(media_part => {
            if (media_part.id){ // An ID should exist but some test structures doesn't so therefore I'm including this check here.
                previous_ids.push(media_part.id.toLowerCase())
            }
        })
        if (previous_ids.includes(json_body.id)){
            console.log("Error! ID is not unique. Returing error...")
            return res.send(
                api_responses.generate_api_error(409, "ID is not unique.")
            )
        }
        previous_media_structure.parts.push(json_body)
        update_structure_for(media_type, previous_media_structure)
        console.log("Part was added. Returning response...")
        return res.send(api_responses.generate_api_response(
            {"message": "Part was added successfully.", "new_part": json_body, "complete_new_part_json": previous_media_structure}
        ))
    }


})
app.listen(SERVER_PORT, () => {
    console.log(`The app has started and is listening on port ${SERVER_PORT}.`)
})