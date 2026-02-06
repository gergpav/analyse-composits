import cv2
import numpy as np
from tkinter import messagebox

def one_piece_composite(image_path):
    def is_peat_composite(image):
        # Преобразуем в HSV для анализа цвета
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Диапазоны коричневых оттенков (типичных для торфа и древесины)
        lower_brown = np.array([5, 50, 20])
        upper_brown = np.array([25, 255, 200])

        # Маска коричневых пикселей
        brown_mask = cv2.inRange(hsv, lower_brown, upper_brown)

        # Считаем процент коричневых пикселей
        brown_ratio = np.sum(brown_mask > 0) / (image.shape[0] * image.shape[1])

        return brown_ratio > 0.2

    def detect_people(image):

        hog = cv2.HOGDescriptor()
        hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

        # Детекция людей на изображении
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        boxes, weights = hog.detectMultiScale(gray, winStride=(8, 8), padding=(8, 8), scale=1.05)

        return len(boxes) > 0  # Если есть хотя бы один человек, возвращаем True


    image = cv2.imread(image_path)

    # Проверка на древесно-торфяной композит
    if not is_peat_composite(image):
        messagebox.showerror("Ошибка",
                             "Предупреждение: загруженное изображение не похоже на древесно-торфяной композит.")
        exit()

    # Детекция людей
    if detect_people(image):
        messagebox.showerror("Ошибка",
                             "Предупреждение: на изображении обнаружены люди.")
        exit()

    # Преобразование в серый
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Сглаживание
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Пороговая обработка
    _, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY)

    # Поиск контуров
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Копирование изображения для отрисовки контуров
    image_with_contours = image.copy()

    # Контуры
    contour_color = (154, 250, 0)
    cv2.drawContours(image_with_contours, contours, -1, contour_color, 1)


    # Площадь
    area = sum(cv2.contourArea(c) for c in contours)
    total_area = image.shape[0] * image.shape[1]
    percentage = (area / total_area) * 100

    a = round(100 - percentage, 1)



    if 10 <= a < 40:
        text_for_word = f"Процент тофра – {a}%. Данный композит идеален для теплоизоляции. Низкая теплопроводность (0,15–0,30 Вт/(м·К)) позволяет эффективно сохранять тепло, что подходит для утепления стен, кровли, полов или изоляции холодильных камер. Звукопоглощение (a = 0,2–0,5) и прочность (0,8–1,5 МПа) здесь умеренные, поэтому материал не рекомендуется для несущих конструкций или помещений с высокими требованиями к шумоизоляции."
    elif 40 <= a < 60:
        text_for_word = f"Процент тофра – {a}%. Этот вариант обеспечивает баланс между теплоизоляцией, звукопоглощением и прочностью. Теплопроводность (0,45–0,55 Вт/(м·К)) достаточно для умеренной изоляции, звукопоглощение (a = 0,6–0,7) эффективно снижает бытовой шум, а прочность (2,2–4,5 МПа) подходит для большинства строительных задач: фасадные панели, перегородки, универсальные плиты. Оптимален, если нужен композит «два в одном» — и для тепла, и для тишины."
    else:
        text_for_word = f"Процент тофра – {a}%. Композит с таким процентом торфа — выбор для звукоизоляции и прочности. Максимальное звукопоглощение (α = 0,8) делает его идеальным для студий, кинотеатров, промышленных объектов, а высокая прочность (5,0 МПа) позволяет использовать в несущих конструкциях или мебели. Однако теплоизоляция здесь слабая (λ = 0,65 Вт/(м·K)), поэтому для утепления он не подойдет."

    return image_with_contours, text_for_word
