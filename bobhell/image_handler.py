from PIL import Image







def combine():

    # Открываем изображение, которое будет фоном (разрешение 1080x1920)
    background = Image.open("C:\\Users\\Dmitry\\Documents\\projects\\bobhell\\background.jpg")
    
    # Получаем размеры изображения
    width, height = background.size

    # Вычисляем новые размеры и координаты для вырезки
    new_width = min(width, height * 9 // 16)  # Ширина будет 9/16 от высоты
    new_height = min(height, width * 16 // 9)  # Высота будет 16/9 от ширины
    left = 0  # Начало вырезки по горизонтали
    top = height - new_height  # Начало вырезки по вертикали (снизу)

    # Вырезаем часть изображения
    background = background.crop((left, top, left + new_width, top + new_height))

    # Меняем размер до 1080x1920
    background = background.resize((1080, 1920), Image.LANCZOS)

    # Открываем изображение, которое будет накладываться (любого формата)
    overlay = Image.open("C:\\Users\\Dmitry\\Documents\\projects\\bobhell\\overlay.jpg")

    # Получаем размеры фона и наложения
    background_width, background_height = background.size
    overlay_width, overlay_height = overlay.size

    # Рассчитываем новые размеры наложения, чтобы оно соответствовало разрешению 1080x1920
    new_overlay_width = 900
    new_overlay_height = int(overlay_height * (new_overlay_width / overlay_width))

    # Масштабируем наложение к новым размерам
    overlay = overlay.resize((new_overlay_width, new_overlay_height), Image.LANCZOS)

    # Рассчитываем координаты, чтобы разместить наложение в центре фона с рамками
    x = (background_width - new_overlay_width) // 2
    y = (background_height - new_overlay_height) // 2

    # Создаем новое изображение, накладывая фон и наложение
    result = background.copy()
    result.paste(overlay, (x, y))

    # Сохраняем итоговое изображение
    result.save("result.jpg")

    # Закрываем изображения
    background.close()
    overlay.close()



def main():
    print()



if __name__ == "__main__":
    main()