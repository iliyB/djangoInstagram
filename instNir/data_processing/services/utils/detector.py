from collections import Counter

from django.conf import settings
from moviepy.editor import VideoFileClip
from imageai.Detection import ObjectDetection, VideoObjectDetection

from data_processing.services.utils.file_utils import delete_file


class Detector:
    """
        Содержит и инициализирует два класса:
        - для получения метаданных с фото
        - для получения метаданных с видео
        При инициализация происходит загрузка модели
        нейронной сети
    """

    def __init__(self):
        self.detector_photo = DetectorPhoto()
        self.detector_video = DetectorVideo()


class DetectorPhoto:
    """Получает метаданные с фото"""

    def __init__(self):
        self.detector = ObjectDetection()
        self.detector.setModelTypeAsRetinaNet()
        self.detector.setModelPath(settings.ENV_CONFIG.get("PATH_TO_RETINA_NET_MODEL"))
        self.detector.loadModel()

    def detector_objects_from_photo(self, input_file: str, delete_file_: bool = False) -> Counter:
        """
            Получает метаданные из фото, находящегося по пути input_file
            и возвращает словарь с объектами с фото
        """

        _, list_objects = self.detector.detectObjectsFromImage(
            input_image=str(input_file),
            output_type="array",
            minimum_percentage_probability=45
        )

        objects = Counter()

        for object in list_objects:
            objects[object["name"]] += 1

        if delete_file_:
            delete_file(input_file)

        return objects


class DetectorVideo:
    """Получает метаданные с видео"""

    def __init__(self):
        self.detector = VideoObjectDetection()
        self.detector.setModelTypeAsRetinaNet()
        self.detector.setModelPath(settings.ENV_CONFIG.get("PATH_TO_RETINA_NET_MODEL"))
        self.detector.loadModel(detection_speed='fastest')
        self.result = None

    def detector_objects_from_video(self, input_file: str, delete_file_: bool = False) -> Counter:
        """
            Получает метаданные из видео, находящегося по пути input_file
            и возвращает словарь с объектами с видео.
            При обрабтки видео создает его копию с fps=3, по которому
            происходит определение метаданных
        """

        def _forFull(output_arrays, count_arrays, average_output_count):
            self.result = average_output_count

        new_file: str = str(str(input_file[:-4]) + 'fix' + str(input_file[-4:]))

        clip = VideoFileClip(input_file)
        clip.write_videofile(new_file, fps=3, logger=None, codec='libx264')
        clip.reader.close()

        self.detector.detectObjectsFromVideo(
            input_file_path=new_file,
            frames_per_second=3,
            video_complete_function=_forFull,
            minimum_percentage_probability=45,
            save_detected_video=False
        )

        if delete_file_:
            delete_file(input_file)
        delete_file(new_file)

        objects = Counter()

        for key, value in self.result.items():
            if value:
                objects[key] = value
            else:
                objects[key] = 1

        return objects

