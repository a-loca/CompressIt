import numpy as np

def jpg_compression(image, f, d):
    data = image.getdata()
    
    # Get pixels values as a numpy matrix
    pixels = np.asarray(data)
    
    # Subdivide image in FxF matrices
    
    