from google.cloud import vision

# Define the client options with the specific API endpoint
client_options = {"api_endpoint": "eu-vision.googleapis.com"}


def detect_text_uri(uri):
    """
    Detects text in the file located in Google Cloud Storage or on the Web.

    This function uses the Google Vision API to perform text detection on an image.
    The image is specified by the URI parameter, which can be a URL or a Google Cloud Storage URI.
    The function returns the detected text as a string.

    :param uri: The URI of the image to analyze.
    :return: The detected text as a string.
    :raises Exception: If an error occurs during the API request.
    """

    # Create a client for the Vision API
    client = vision.ImageAnnotatorClient(client_options=client_options)

    # Create an Image object and set its source to the specified URI
    image = vision.Image()
    image.source.image_uri = uri

    # Perform text detection on the image
    response = client.text_detection(image=image)

    # If an error occurred during the API request, raise an exception
    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )

    # Return the detected text
    return response.full_text_annotation.text
