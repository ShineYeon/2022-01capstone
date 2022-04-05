import cv2
import numpy as np
import pytesseract
import regex
from elasticsearch import Elasticsearch

# get image
img = cv2.imread('/Users/heeyeon/Desktop/graduate_/graduate/imgs/allergytest.png')

# all funtions

def extract_words(details):
    parse_text = []
    word_list = []
    last_word = ''

    for word in details['text']:
        if word != '':
            word_list.append(word)
            last_word = word

        if (last_word != '' and word == '') or (word == details['text'][-1]):
            parsed = ''.join(word_list)
            match = regex.match(r"([가-힣ㄱ-ㅎㅏ-ㅣ]+)([0-9]+)", parsed, regex.I)

            if match:
                items = match.groups()
            else:
                items = parsed

            parse_text.append(items)
            word_list = []
    return parse_text


def convert_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, threshold_img = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY)
    return threshold_img


def feed_image_to_tess(threshold_img):
    custom_config = r'--oem 3 --psm 6'

    details = pytesseract.image_to_data(
        threshold_img,
        output_type=pytesseract.Output.DICT,
        config=custom_config,
        lang='kor+eng'
    )
    return details


# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# noise removal
def remove_noise(image):
    return cv2.medianBlur(image, 5)


# thresholding
def thresholding(image):
    # threshold the image, setting all foreground pixels to
    # 255 and all background pixels to 0
    return cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]


# dilation
def dilate(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.dilate(image, kernel, iterations=1)


# erosion
def erode(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.erode(image, kernel, iterations=1)


# opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)


# canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)


# skew correction
def deskew(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    thresh = cv2.threshold(gray, 0, 255,
                           cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h),
                             flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated


# template matching
def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)

gray = get_grayscale(img)
thresh = thresholding(gray)
rnoise = remove_noise(gray)
dilate = dilate(gray)
erode = erode(gray)
opening = opening(gray)
canny = canny(gray)

#cv2.imwrite("/Users/heeyeon/Desktop/graduate_/graduate/imgs/grayscale.jpg")

#image pretreatment
#deskew = deskew(img)
#gray = get_grayscale(img)
#cv2.imwrite("/Users/heeyeon/Desktop/graduate_/graduate/imgs/grayscale.jpg", gray)

#rnoise는 노이즈 감소라서 작은 글씨 선별에는 별로인듯하다
#rnoise = remove_noise(gray)
#cv2.imshow('rnoise', rnoise)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

#threshold는 특정 수치값을 정해놓으면 그 기준값을 통해 값을 도출 -> 흑백으로 작업해야함
#글씨 선별에 좋은 듯함.
#thresh = thresholding(gray)
#cv2.imwrite("/Users/heeyeon/Desktop/graduate_/graduate/imgs/threshold.jpg", thresh)
#cv2.imshow('thresh', thresh)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

#dilate = dilate(thresh)
#cv2.imshow('dilate', dilate)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

#ero = erode(dilate)
#cv2.imshow('ero', ero)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

#dil = dilate(gray)
#cv2.imshow('dil', dil)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

#opening = opening(ero)
#cv2.imshow('opening', opening)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

#canny = canny(thresh)
#cv2.imshow('canny', canny)
#cv2.imwrite("/Users/heeyeon/Desktop/graduate_/graduate/imgs/canny.jpg", canny)

#OCR
def main():

    image_path = '/Users/heeyeon/Desktop/graduate_/graduate/imgs/allergytest.png'
    threshold_img = convert_image(image_path)

    # display_image(threshold_img)

    details = feed_image_to_tess(threshold_img)
    parse_text = extract_words(details)

    print(f"Parsed text: {parse_text}")

    # highlight_with_rectangle(details, threshold_img)


if __name__ == '__main__':
    main()
