import cv2
import numpy as np
from base64 import b64decode
import io
from PIL import Image

def js_to_image(js_reply):
    """
    Params:
            js_reply: JavaScript object containing image from webcam
    Returns:
            img: OpenCV BGR image
    """
    # Decode base64 image
    image_bytes = b64decode(js_reply.split(',')[1])
    # Convert bytes to numpy array
    jpg_as_np = np.frombuffer(image_bytes, dtype=np.uint8)
    # Decode numpy array into OpenCV BGR image
    img = cv2.imdecode(jpg_as_np, flags=1)

    return img

def bbox_to_bytes(bbox_array):
    """
    Params:
            bbox_array: Numpy array (pixels) containing rectangle to overlay on video stream.
    Returns:
        bytes: Base64 image byte string
    """
    # Convert array into PIL image
    bbox_PIL = Image.fromarray(bbox_array, 'RGBA')
    iobuf = io.BytesIO()
    # Format bbox into PNG for return
    bbox_PIL.save(iobuf, format='png')
    # Format return string
    bbox_bytes = 'data:image/png;base64,{}'.format(str(b64encode(iobuf.getvalue()), 'utf-8'))

    return bbox_bytes