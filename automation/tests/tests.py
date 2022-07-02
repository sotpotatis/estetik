'''tests.py
Some tests.'''
import json, os, random, logging
from api_client import Client
AUTH_TOKENS = json.loads(open(os.path.join(os.path.dirname(os.getcwd()), "api/authorized_tokens.json"), "r").read())
AUTH_TOKEN = random.choice(AUTH_TOKENS["tokens"])
client = Client(AUTH_TOKEN, api_domain="localhost:5000", use_https=False)
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
logger.info("Client created.")
#Test uploads:
"""#File to upload
file_to_upload = os.path.join(os.getcwd(), "testfile.jpg")
client.create_new_image_item(
    file_to_upload,
    "API test image",
    "Testing out the API.",
    "test_image",
    "tests"
)"""
#Test part creation
"""client.create_new_part("images",
                       "Test",
                       "test",
                       "This is a test")"""
#Test listing of structure
logger.info(client.get_segment_structure_for("images"))