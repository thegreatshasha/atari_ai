import cv2
import numpy as np

def resize_image(image, width, height, resized_width, resized_height, crop_offset, resize_method = 'crop'):
        """ Appropriately resize a single image """

        if resize_method == 'crop':
            # resize keeping aspect ratio
            resize_height = int(round(float(height) * resized_width / width))

            resized = cv2.resize(image, (resized_width, resize_height), interpolation=cv2.INTER_LINEAR)

            # Crop the part we want
            crop_y_cutoff = resize_height - crop_offset - resized_height
            cropped = resized[crop_y_cutoff : crop_y_cutoff + resized_height, :]

            return cropped
        
        elif resize_method == 'scale':
            return cv2.resize(image, (resized_width, resized_height), interpolation=cv2.INTER_LINEAR)
        
        else:
            raise ValueError('Unrecognized image resize method.')

def get_processed_screen(ale):
    RESIZE_METHOD = 'crop'
    RESIZED_WIDTH = 84
    RESIZED_HEIGHT = 84
    CROP_OFFSET = 8
    width, height = ale.getScreenDims()
    screen_buffer = np.empty((height, width), dtype=np.uint8)
    
    ale.getScreenGrayscale(screen_buffer)

    resized_image = resize_image(screen_buffer, width, height, RESIZED_WIDTH, RESIZED_HEIGHT, CROP_OFFSET, resize_method = 'crop')
    return resized_image