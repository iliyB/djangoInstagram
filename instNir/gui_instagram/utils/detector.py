from imageai.Detection import ObjectDetection, VideoObjectDetection
import os
from moviepy.editor import VideoFileClip
from .checkPath import delete_file

class detector:

    def __init__(self):

        self.detector_photo = detector_photo()
        self.detector_video = detector_video()

class detector_photo:

    def __init__(self):
        self.detector = ObjectDetection()
        self.detector.setModelTypeAsRetinaNet()
        self.detector.setModelPath("resnet50_coco_best_v2.1.0.h5")
        self.detector.loadModel()

    def detectorRetinaNet_from_photo(self, input_file: str, delete_file_: bool=False) -> {}:

        _, list = self.detector.detectObjectsFromImage(
            input_image=str(input_file),
            output_type="array",
            minimum_percentage_probability=45
        )
        objects = {}
        for object in list:
            if object['name'] in objects:
                objects[object['name']] += 1
            else:
                objects.update({object['name']: 1})

        if delete_file_:
            delete_file(str(input_file))

        return objects

class detector_video:

    def __init__(self):
        self.detector = VideoObjectDetection()
        self.detector.setModelTypeAsRetinaNet()
        self.detector.setModelPath("resnet50_coco_best_v2.1.0.h5")
        self.detector.loadModel(detection_speed='fastest')
        self.result = None

    def detectorRetinaNet_from_video(self, input_file: str, delete_file_: bool=False) -> {}:

        def forFull(output_arrays, count_arrays, average_output_count):
            # print("Array for the outputs of each frame ", output_arrays)
            # print("Array for output count for unique objects in each frame : ", count_arrays)
            # print("Output average count for unique objects in the entire video: ", average_output_count)
            # print("------------END OF THE VIDEO --------------")
            self.result = average_output_count

        new_file = str(str(input_file[:-4]) + 'fix' + str(input_file[-4:]))

        clip = VideoFileClip(str(input_file))
        clip.write_videofile(str(new_file), fps=3, logger=None, codec='libx264')
        clip.reader.close()

        self.detector.detectObjectsFromVideo(input_file_path=str(new_file)
                                                     , frames_per_second=3, video_complete_function=forFull,
                                                     minimum_percentage_probability=45,
                                                     save_detected_video=False)
        if delete_file_:
            delete_file(str(input_file))
        delete_file(str(new_file))

        objects = {}
        for key in self.result.keys():
            if self.result.get(key):
                objects.update({key: self.result.get(key)})
            else:
                objects.update({key: 1})

        return objects
