import cv2
import numpy as np
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim


def compareImages(
        compared_images, reference_image, image_names=None, crop_size=None,
        font_size=1, font_stoke=3, first_line_y=40, text_spacing=40,
        text_x_coordinate=10, white_box_height=140):
    """Compare list of images to one image

    Concatenate images into single image with added similarity metrics printed
    below each comparison image.

    Arguments
    ---------
    compared_images : list of numpy arrays
        List including images which are compared to the reference image
    reference_image : numpy array
        Image which is compared to all comparison images
    image_names : list of strings
        List of names for each comparison image and reference image
    crop_size : int
        If defined, all images will be center cropped with this size
    font_size : int
        Text font size
    font_stoke : int
        Text width
    first_line_y : int
        Text y-coordinate in the first line
    text_spacing : int
        Text row height
    text_x_coordinate : int
        Text x-coordinate in each row
    white_box_height : int
        Height in pixels of each white box added below the images

    Return
    ------
    Numpy array of concatenated comparison image with similarity metrics
    """
    def centerCrop(image):
        center = np.divide(list(image.shape), 2)
        x = center[1] - crop_size / 2
        y = center[0] - crop_size / 2
        return image[int(y):int(y + crop_size), int(x):int(x + crop_size)]
    def addText(image, text, position):
        return cv2.putText(
            image, text, position, cv2.FONT_HERSHEY_SIMPLEX, font_size,
            (0, 0, 0, 255), font_stoke)
    def getWhiteBox(image):
        shape = tuple([white_box_height] + list(image.shape[1:]))
        return np.ones(shape) * 255

    # Crop images
    if type(compared_images) == np.array:
        compared_images = [compared_images]
    if crop_size:
        compared_images = [centerCrop(image) for image in compared_images]
        reference_image = centerCrop(reference_image)

    # Define texts
    texts = []
    if image_names:
        texts.append(image_names)
    texts += [
        [
            "PSNR: {0:.2f}dB".format(psnr(image, reference_image))
            for image in compared_images
        ],
        [
            "SSIM: {0:.2f}".format(
                ssim(image, reference_image, multichannel=True))
            for image in compared_images
        ],
    ]

    # Add text to images
    for i, image in enumerate(compared_images):
        white_area = getWhiteBox(image)
        for j, text_list in enumerate(texts):
            position = (text_x_coordinate, first_line_y + j*text_spacing)
            white_area = addText(white_area, text_list[i], position)
        compared_images[i] = np.concatenate([image, white_area], axis=0)
    if len(image_names) > len(compared_images):
        white_area = getWhiteBox(reference_image)
        position = (text_x_coordinate, first_line_y)
        white_area = addText(white_area, image_names[-1], position)
        reference_image = np.concatenate([reference_image, white_area], axis=0)
    return np.concatenate(compared_images + [reference_image], axis=1)


if __name__ == "__main__":
    # Paths
    image_paths = [
        "../REDS/train_blur/001/00000000.png",
        "../REDS/train_sharp/001/00000000.png",
        "../REDS/train_sharp/001/00000000.png",
    ]
    reference_image_path = "../REDS/train_sharp/001/00000000.png"

    # Images and names
    images = [cv2.imread(image_path) for image_path in image_paths]
    images[2] = (images[2]**0.5 * 4).astype(np.uint8)
    reference_image = cv2.imread(reference_image_path)
    names = ["Input", "Prediction 1", "Prediction 2", "Ground Truth"]

    # Create comparison image
    comparison_image = compareImages(
        images, reference_image, names, crop_size=256)
    cv2.imwrite("comparison_image.png", comparison_image)
