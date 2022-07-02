# Python API Client
I am an API client for the Estetik API. See below for how you can use me!

### Quickstart and examples

#### Client initialization

The code below initializes a client for interacting with the API.
Both `api_domain` and `use_https` are optional parameters, but you'll probably
have to set at least the API domain since the default is my instance.
```python
from api_client import Client #Import the client
#Client set-up
client = Client(
    "<LOAD_AUTH_TOKEN_HERE>", 
    api_domain="localhost:5000", #DO NOT start with a prefix like http:// or https://!
    use_https=False #Only use False if not in production :P
)
```

#### Upload a new image
The code below uploads a new image.
```python
import os
#[CLIENT INITIALIZATION CODE HERE]
#Set the path of the file to upload
file_to_upload = os.path.join(os.getcwd(), "testfile.jpg")
client.create_new_image_item(
    file_to_upload, #Path
    "Cute puppy dog", #Title
    "Woof woof! This is me testing out the API.", #Description
    "test_image_of_cute_puppy_dog", #An ID to give the image
    "tests" #Part ID that the image should be added to
```

#### Create a new part
A part is a collection of media, such as images etc. You can find out more about parts and media structure in the main README.
```python
#[CLIENT INITIALIZATION CODE HERE]
client.create_new_part(
    "images", #Media type to create part in
    "Collection of test images", #A title to give the part
    "This is a collection of images testing out the API.", #A description for the new part
    "test_images" #An id for the new part
)
```
   