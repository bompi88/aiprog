def normalize(image):
    return [(float(pixel) / float(255)) for pixel in image]


def normalize_images(images):
    for idx, image in enumerate(images):
        images[idx] = normalize(image)
    return images


def as_binary_vector(num):
    return [1 if num == i else 0 for i in range(10)]