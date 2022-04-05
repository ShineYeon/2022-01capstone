""" Image process module

Reference:
  Extracting text from images with Tesseract OCR, OpenCV, and Python
  https://www.opcito.com/blogs/extracting-text-from-images-with-tesseract-ocr-opencv-and-python

Command:
  $ python -m venv venv
  $ venv\Script\activate
  $ pip install -r requirements.txt
  $ python image_process_v1.py

"""

import cv2
import pytesseract
import regex


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


def highlight_with_rectangle(details, threshold_img):
    total_boxes = len(details['text'])

    for sequence_number in range(total_boxes):
        trans_conf = int(float(details['conf'][sequence_number]))
        if trans_conf > 30:
            (x, y, w, h) = (
            details['left'][sequence_number], details['top'][sequence_number], details['width'][sequence_number],
            details['height'][sequence_number])
            threshold_img = cv2.rectangle(threshold_img, (x, y), (x + w, y + h), (0, 255, 0), 1)

    display_image(threshold_img)


def display_image(threshold_img):
    cv2.imshow('captured text', threshold_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


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