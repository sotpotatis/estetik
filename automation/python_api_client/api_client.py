'''python_api_client.py
A client to interact with the API.
'''

import os, logging, requests, io

FILE_CLASSES = [io.TextIOBase, io.BufferedIOBase, io.RawIOBase, io.IOBase]
def detect_if_object_is_file(object):
    '''Quick function to detect if an object is a file.

    :param object: The object to check.'''
    return any([isinstance(object, file_class)] for file_class in FILE_CLASSES)

#Exceptions
class UnexpectedStatusCodeError(Exception):
    pass

class JSONDecodingFailed(Exception):
    pass

class ErrorReturnedFromAPI(Exception):
    pass

#Client definition
class Client:
    def __init__(self, access_token, api_domain="estetik-api.albins.website", use_https=True):
        self.access_token = access_token
        self.api_domain = api_domain
        self.use_https = use_https
        self.logger = logging.getLogger(__name__)
        self.api_base_params = {"access_token": self.access_token}
        self.logger.info(f"Initialized API client with params: domain: {self.api_domain}, HTTPS: {self.use_https}.")

    def create_api_url(self, api_endpoint):
        '''Creates an API url by concatenating the API URL with the other set parameters.

        :param api_endpoint: Endpoint to access without slashes and /api/ part. For example add_image.'''
        return ("https://" if self.use_https else "http://") + self.api_domain + "/api/" + api_endpoint

    def handle_request_success_and_error(self, request_obj, return_json=True):
        '''Handles requests that have been returned as request objects and checks if they have been successful.
        The return value may be used as the return value from any function calling the API.

        :param request_obj: The requests.Request object that was returned by the request.

        :param return_json: Whether to return the JSON that the API returned or not.'''
        self.logger.debug("Handling and checking status of a request...")
        if request_obj.status_code != 200:
            error_message = f"Received an unexpected status code from the API ({request_obj.status_code})."
            self.logger.critical(error_message)
            raise UnexpectedStatusCodeError(error_message)
        else:
            try:
                request_json = request_obj.json()
            except Exception as e:
                error_message = "Did not get valid JSON back from the API (JSON decoding failed)"
                self.logger.critical(error_message)
                raise JSONDecodingFailed(error_message)
            #Check success or not
            api_status = request_json["status"]["type"].lower()
            if api_status != "success":
                error_message = f"The API responded with a status that was not success (status was: {api_status})."
                #The error status should have provided us with a "message" attribute.
                if "message" in request_json:
                    error_message += f"An error message was provided: {request_json['message']}"
                self.logger.critical(error_message)
                raise ErrorReturnedFromAPI(error_message)
            else:
                self.logger.info("The request succeeded!")
                if return_json:
                    self.logger.debug(f"Returning request JSON as requested: {request_json}...")
                    return request_json #Return the request JSON
                else:
                    self.logger.debug(f"Returning None as requested... (return_json is False)")
                    return #Return nothing

    def create_new_image_item(self, image_path, image_title, image_description, image_id, belongs_to_part_id):
        '''Uploads an image using the API and thus creates a new item.

        :param image_path: A path to the image file.

        :param image_title: Title of the image

        :param image_description: Description of the image

        :param belongs_to_part_id: The part ID that the image item belongs to

        :param image_id: An ID to give the image. This will decide its final filename on the server.'''
        self.logger.debug("Opening passed file parameter and reading...")
        file_to_send = open(image_path, "rb")
        self.logger.debug("Provided file read.")
        #Create request parameters
        request_params = self.api_base_params
        request_params["title"] = image_title
        request_params["description"] = image_description
        request_params["target_part_id"] = belongs_to_part_id
        request_params["image_id"] = image_id
        filename = os.path.basename(image_path)
        request_url = self.create_api_url("add_image")
        files = {"image": (filename, file_to_send)}
        self.logger.debug(f"Sending item creation request with URL: {request_url} and params {request_params}...")
        request = requests.post(request_url, params=request_params,
                                files=files)
        return self.handle_request_success_and_error(request)

    def create_new_part(self, media_type_to_create_part_in, part_title, part_description, part_id, part_segments=[]):
        '''Creates a new part in a media types's structure.

        :param media_type_to_create_part_in: The media type to create the part in.

        :param part_title: A descriptive title for the new part.

        :param part_description: A description of the new part.

        :param part_id: An ID to give the new part.

        :param part_segments: If specified, any segments to include in the part.'''
        request_json = {
            "title": part_title,
            "description": part_description,
            "id": part_id,
            "segments": part_segments
        }
        api_url = self.create_api_url(f"{media_type_to_create_part_in.lower()}/parts/add")
        self.logger.info(f"Creating a new part by sending a request to {api_url}...")
        self.logger.debug(f"Request JSON: {request_json}. Params: {self.api_base_params}")
        request = requests.post(api_url, json=request_json, params=self.api_base_params)
        return self.handle_request_success_and_error(request)

    def get_segment_structure_for(self, media_type):
        '''Gets the segment structure for a certain media type. This endpoint requires no authorization.

        :param media_type: The media type.'''
        self.logger.info(f"Getting and returning structure for {media_type}...")
        api_url = self.create_api_url(f"structure/{media_type.lower()}")
        self.logger.info(f"Sending a request to {api_url}...")
        request = requests.get(api_url)
        return self.handle_request_success_and_error(request)