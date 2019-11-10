from PIL import Image
import pytesseract
import cv2
import numpy as np
import tkinter as tk

def ImageToGrid(image):

    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    # Pildi tõlkimine piksliteks ja seejätel RGB-->ühevärviline
    img = cv2.imread(image)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # Pildilt äärte üles otsimine kasutades Canny meetodit
    edges = cv2.Canny(gray, 100, 200)

    # Pikslite tegemine kas mustaks kui väärtus on alla 110 või valge kui üle 255. Et lihtsam oleks töödelda
    ret, whiteblackimg = cv2.threshold(gray, 110, 255, cv2.THRESH_BINARY)

    # Otsin üles pildilt kõik sirged jooned, HoughLines meetodiga
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 175)

    vertical_lines = []
    horizontal_lines = []

    # Eemaldan liiga kõrvuti olevad jooned. Eesmärgiks on saada vaid 10 joont mõlemat pidi, mitte mingi 25
    for index, line in enumerate(lines):
        tooSimilar = False
        if 1 < line.item(1) < 2:
            if vertical_lines == []:
                vertical_lines.append(line)
                continue
            for el in vertical_lines:
                if abs(el.item(0) - line.item(0)) < 20:
                    tooSimilar = True
                    break
            if tooSimilar == False:
                vertical_lines.append(line)

        else:
            if horizontal_lines == []:
                horizontal_lines.append(line)
                continue
            for el in horizontal_lines:
                if abs(abs(el.item(0)) - abs(line.item(0))) < 30:
                    tooSimilar = True
                    break
            if tooSimilar == False:
                horizontal_lines.append(line)
    lines = horizontal_lines + vertical_lines

    # Meetod Houghlines leiab read polaarkoordinaatidena. Kuna ma ei oska nendega ringi käia, siis teen need Descartesi koordinaatideks.
    cart_horizontal_lines = []
    for line in horizontal_lines:
        rho, theta = line[0]
        y = rho * np.cos(theta)
        x = rho * np.sin(theta)
        cart_horizontal_lines.append([int(y), int(x)])

    cart_vertical_lines = []
    for line in vertical_lines:
        rho, theta = line[0]
        y = rho * np.cos(theta)
        x = rho * np.sin(theta)
        cart_vertical_lines.append([int(x), int(y)])

    cart_horizontal_lines.sort()
    cart_vertical_lines.sort()


    # Tükeldan pildi ühikruutudeks ja pytesseract katsub tuvastada numbi
    result = []
    for i in range(9):
        temp = []
        for j in range(9):
            area = whiteblackimg[cart_horizontal_lines[i][0]:cart_horizontal_lines[i + 1][0],
                   cart_vertical_lines[j][0]: cart_vertical_lines[j + 1][0]]
            new_image = Image.fromarray(area)
            k = (pytesseract.image_to_string(new_image, lang='eng',
                                             config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789'))
            temp.append(k)
        result.append(temp)

    return result
