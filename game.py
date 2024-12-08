from screen import Screen
import numpy as np 
from PIL import Image
import random 


#Example usage:
slices = sliceimage(" ", 3, 3)

#Convert slices back to Pillow Images and save
for i, slice_img in enumerate(slices):
    slice_pil_img = Image.fromarray(slice_img)
    # Convert RGBA to RGB before saving as JPEG
    if slice_pil_img.mode == 'RGBA':
        slice_pil_img = slice_pil_img.convert('RGB')

        # Now you can save the image as a JPEG
        slice_pil_img.save(f"slice{i+1}.jpg")

    slice_pil_img.save(f"slice{i+1}.jpg")



#Creating the Shuffler

image_paths = sliceimage

# Load the images into a list
images = [Image.open(img_path) for img_path in image_paths]

# Convert the list into a 2D list (3x3 matrix)
matrix = np.array(images).reshape(3, 3)

# Flatten the matrix to a 1D list for shuffling
flattened_images = matrix.flatten()

# Shuffle the 1D list
random.shuffle(flattened_images)

# Reshape the shuffled images back to a 3x3 matrix
shuffled_matrix = np.array(flattened_images).reshape(3, 3)
print(shuffled_matrix)