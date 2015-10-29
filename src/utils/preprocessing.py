def preprocess(image):
    return normalize(image)


def normalize(image):
    return [(float(pixel) / float(255)) for pixel in image]