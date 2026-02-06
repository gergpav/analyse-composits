import cv2
import numpy as np
from tkinter import messagebox

def composite_in_section(image_path):
    def detect_people(image):

        hog = cv2.HOGDescriptor()
        hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        boxes, weights = hog.detectMultiScale(gray, winStride=(8, 8), padding=(8, 8), scale=1.05)

        return len(boxes) > 0  #

    image = cv2.imread(image_path)


    if detect_people(image):
        messagebox.showerror("Ошибка",
                             "На изображении обнаружены люди. Не композит.")
        exit()

    # Преобразование изображения в серые оттенки
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Сглаживание изображения для удаления шума
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Пороговая обработка: можно подбирать значение порога в зависимости от изображения
    _, thresh = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY_INV)

    # Поиск контуров на изображении
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Копируем изображение для отрисовки контуров
    image_with_contours = image.copy()

    # Цвет для рисования контуров
    contour_color = (0, 255, 0)  # Зеленый
    cv2.drawContours(image_with_contours, contours, -1, contour_color, 1)

    # Вычисляем площадь торфа
    torf_area = sum(cv2.contourArea(c) for c in contours)

    # Общая площадь изображения
    total_area = image.shape[0] * image.shape[1]

    # Вычисляем процент торфа в разрезе
    percentage_torf = (torf_area / total_area) * 100

    b = round(100 - percentage_torf, 1)

    if 10 <= percentage_torf < 40:
        text_for_word = f"Процент тофра – {b}%. Данный композит идеален для теплоизоляции. Низкая теплопроводность (0,15–0,30 Вт/(м·К)) позволяет эффективно сохранять тепло, что подходит для утепления стен, кровли, полов или изоляции холодильных камер. Звукопоглощение (a = 0,2–0,5) и прочность (0,8–1,5 МПа) здесь умеренные, поэтому материал не рекомендуется для несущих конструкций или помещений с высокими требованиями к шумоизоляции."
    elif 40 <= percentage_torf < 60:
        text_for_word = f"Процент тофра – {b}%. Этот вариант обеспечивает баланс между теплоизоляцией, звукопоглощением и прочностью. Теплопроводность (0,45–0,55 Вт/(м·К)) достаточно для умеренной изоляции, звукопоглощение (a = 0,6–0,7) эффективно снижает бытовой шум, а прочность (2,2–4,5 МПа) подходит для большинства строительных задач: фасадные панели, перегородки, универсальные плиты. Оптимален, если нужен композит «два в одном» — и для тепла, и для тишины."
    else:
        text_for_word = f"Процент тофра – {b}%. Композит с таким процентом торфа — выбор для звукоизоляции и прочности. Максимальное звукопоглощение (α = 0,8) делает его идеальным для студий, кинотеатров, промышленных объектов, а высокая прочность (5,0 МПа) позволяет использовать в несущих конструкциях или мебели. Однако теплоизоляция здесь слабая (λ = 0,65 Вт/(м·K)), поэтому для утепления он не подойдет."

    return image_with_contours, text_for_word
