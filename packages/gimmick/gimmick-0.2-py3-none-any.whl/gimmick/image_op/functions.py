def convert_2dto3d(images):
    print("convering images to 3d: shape before convert_2dto3d", images.shape)
    if len(images.shape) == 3:
        images = images.reshape(images.shape[0], images.shape[1], images.shape[2], 1)
    print("shape after convert_2dto3d", images.shape)
    return images

if __name__ == "__main__":
    from sklearn import datasets
    digits = datasets.load_digits()
    images = digits.images  # It contains roughly 1800 images of shape 8 x 8
    print("shape before convert_2dto3d", images.shape)
    images = convert_2dto3d(images)
    print("shape after convert_2dto3d", images.shape)
