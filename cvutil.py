import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv
from PIL import Image
import copy

# read and obtain the numpy array of the image
def read_img(img_path):
    img = cv.imread(img_path)
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    return img


# auxiliary function to reshape a 1-channel image to 3 identical channels
# while keeping the same image data type
def reshape_2D_img(img):
    if len(img.shape) == 2:
        height, width = img.shape  # get image dimension
        img_type = img.dtype  # get image type

        reshaped_img = np.zeros(shape=(height, width, 3),
                                dtype=img_type)  # initialize reshaped image
        for channel in range(3):
            reshaped_img[:, :, channel] = img

        return reshaped_img
    else:
        pass

# view image
def view_img(img, title=None):
    if len(img.shape)==2:
        img = reshape_2D_img(img)
        
    plt.imshow(img)
    if title is not None:
        plt.title(title, fontsize=15)
    plt.show()

# convert image to grayscale
# input image has to be in RGB format
# by default, output is reshaped to three identical channel
# set reshape to False if 1-channel output is desired
def convert_to_gray(img, reshape=True):
    if reshape==True:
        reshaped_img = reshape_2D_img(cv.cvtColor(img, cv.COLOR_RGB2GRAY))
        return reshaped_img
    else:
        return cv.cvtColor(img, cv.COLOR_RGB2GRAY)

# obtain the type of the image array
def get_type(img):
    return img.dtype

# obtain the shape of the image array
def get_shape(img):
    return img.shape

# convert image type from uint8 to float64
def convert_to_float(img):
    img = img.astype(np.float64)

    total_channel = len(img.shape)
    for channel in range(total_channel):
        img[:, :, channel] = img[:, :, channel] / np.max(img[:, :, channel])
    return img

# draw rectangle on color image based on two corner points
def draw_rectangle(img, pt1, pt2, color=None, thickness=None):
    if color is None:
        color = (255, 0, 0)

    if thickness is None:
        thickness = 5

    cv.rectangle(img, pt1=pt1, pt2=pt2, color=color, thickness=thickness)
    return img

# crop image based on two corner points
def crop(img, pt1, pt2):
    pt1_x, pt1_y = pt1
    pt2_x, pt2_y = pt2

    Xstart, Xend = min(pt1_x, pt2_x), max(pt1_x, pt2_x)
    Ystart, Yend = min(pt1_y, pt2_y), max(pt1_y, pt2_y)

    if len(img.shape) == 3:
        return img[Ystart:Yend + 1, Xstart:Xend + 1, :]
    elif len(img.shape) == 2:
        return img[Ystart:Yend + 1, Xstart:Xend + 1]

# invert grayscale image (work on reshaped or non-reshaped, uint8 image)
def invert(gray_img):
    return cv.bitwise_not(gray_img)

# thresholding grayscale image (work on reshaped or non-reshaped)
# pixel above threshold will be assigned the top_value
def thresholding(gray_img, threshold, top_value):
    return cv.threshold(gray_img, threshold, top_value, cv.THRESH_BINARY)[1]

# resize image by width and scale factor
def resize(img, width_scale_factor, height_scale_factor):
    height, width, _ = img.shape

    new_width = int(width * width_scale_factor)
    new_height = int(height * height_scale_factor)

    return cv.resize(img, (new_width, new_height))

# threshold with color range
def color_thresholding(img, lower_bound, upper_bound):
    lower_bound_arr = np.asarray(lower_bound)
    upper_bound_arr = np.asarray(upper_bound)

    # create mask
    mask = cv.inRange(img, lower_bound_arr, upper_bound_arr)

    return cv.bitwise_and(img, img, mask=mask)

# erode with kernel
def erode(img, kernel, **kwargs):
    return cv.erode(img, kernel, **kwargs)

# dilate with kernel
def dilate(img, kernel, **kwargs):
    return cv.dilate(img, kernel, **kwargs)

# open with kernel
def opening(img, kernel, **kwargs):
    return cv.morphologyEx(img, cv.MORPH_OPEN, kernel, **kwargs)

# closing with kernel
def closing(img, kernel, **kwargs):
    return cv.morphologyEx(img, cv.MORPH_CLOSE, kernel, **kwargs)

# canny edge detection
def getCanny(img, min_val, max_val):
    if len(img.shape)==2:
        img = reshape_2D_img(img)
    # print(f"Min value: {min_val}, Max value: {max_val}")
    return cv.Canny(img, min_val, max_val)

# find contours of grayscale image
def findContours(bin_img, **kwargs):
    bin_img_copy = copy.deepcopy(bin_img)
    if kwargs == {}:
        contours, hierarchy = cv.findContours(bin_img_copy, cv.RETR_TREE,
                                              cv.CHAIN_APPROX_SIMPLE)
    else:
        contours, hierarchy = cv.findContours(bin_img_copy, **kwargs)

    return contours

# draw contours on an image
def drawContours(img, contours, **kwargs):
    if len(img.shape) == 2:
        img = reshape_2D_img(img)

    img_copy = copy.deepcopy(img)

    if kwargs == {}:
        contour_img = cv.drawContours(img_copy, contours, -1, (255, 0, 0), 2)
    else:
        contour_img = cv.drawContours(img_copy, contours, **kwargs)

    return contour_img

# blur image
def blurring(img, mode=None, kernel_size=None, **kwargs):
    if kernel_size is None:
        kernel_size = 5

    if mode is None:
        mode = 'averaging'

    if mode == 'averaging':
        return cv.blur(img, (kernel_size, kernel_size))
    elif mode == 'gaussian':
        if kwargs == {}:
            kwargs['sigmaX'] = 0
            kwargs['sigmaY'] = 0
        return cv.GaussianBlur(img, (kernel_size, kernel_size), **kwargs)
    elif mode == 'median':
        return cv.medianBlur(img, kernel_size)
    elif mode == 'bilateral':
        if kwargs == {}:
            kwargs['d'] = 9
            kwargs['sigmaColor'] = 100
            kwargs['sigmaSpace'] = 100
        return cv.bilateralFilter(img, **kwargs)

# perform zero padding
def zero_padding(img, height_pad, width_pad):
    if len(img.shape)== 2:
        img_height, img_width = img.shape
        output = np.zeros((2*height_pad + img_height,
                           2*width_pad + img_width), dtype=np.uint8)
        output[height_pad:height_pad+img_height,
        width_pad:width_pad+img_width] = img
    elif len(img.shape)==3:
        img_height, img_width, _ = img.shape
        output = np.zeros((2*height_pad + img_height,
                          2*width_pad + img_width, 3), dtype=np.uint8)
        output[height_pad:height_pad+img_height,
        width_pad:width_pad+img_width, :] = img
    return output

# extract video frames
def extract_frame(video_path, output_dir=None):
    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(video_path))
    
    video = cv.VideoCapture(video_path)
    
    count = 0
    while (video.isOpened()):
        ret, frame = video.read()
        if ret:
            count += 1
            frame_path = os.path.join(output_dir, f"frame_{count:0>3d}.jpg")
            print(f"Saving frame {count:0>3d}")
            cv.imwrite(frame_path, frame)
        else:
            break
    
    video.release()