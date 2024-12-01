from PyQt6.QtCore import QByteArray, QBuffer, QIODevice
from PyQt6.QtGui import QImage


def image_to_bytearray(image: QImage) -> QByteArray:
    byte_array = QByteArray()
    buffer = QBuffer(byte_array)
    if buffer.open(QIODevice.OpenModeFlag.WriteOnly):
        image.save(buffer, "PNG")
        buffer.close()
    return byte_array


def bytearray_to_image(byte_array: QByteArray) -> QImage:
    image = QImage()
    image.loadFromData(byte_array)
    return image


def binary_to_qimage(binary_data):
    # Преобразуем строку двоичного представления в байты
    bytes_data = bytes(binary_data, encoding='utf-8')

    # Создаем объект QImage из байтов
    image = QImage()
    image.loadFromData(bytes_data)

    return image