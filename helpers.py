import cv2

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