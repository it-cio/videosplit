from math import ceil
from os import remove
from random import randint
from sys import stdout

import cv2
from moviepy.video.io.VideoFileClip import VideoFileClip


class Divider:
    def __init__(self, video_path, save_path, video_length, cut_length):  # todo Add music and logo path
        self.video_path = video_path
        self.save_path = save_path

        self.capture = cv2.VideoCapture(self.video_path)
        self.capture.set(cv2.CAP_PROP_POS_AVI_RATIO, 1)

        self.length = int(self.capture.get(cv2.CAP_PROP_POS_FRAMES))
        self.width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = int(self.capture.get(cv2.CAP_PROP_FPS))

        self.video_length = ceil(video_length * self.fps)
        self.cut_length = ceil(cut_length * self.fps)

        self.repeatable = False  # Repeat frames.
        if self.video_length > self.length:
            self.repeatable = True

        self.frame = ""
        self.capture.set(cv2.CAP_PROP_POS_AVI_RATIO, 0)

        self.writer = cv2.VideoWriter("".join(self.save_path.split(".")[:-1]) + "_tmp.avi",
                                      cv2.VideoWriter_fourcc(*'XVID'), self.fps, (self.width, self.height))

        self.progress = 0
        self.last_progress = 0

        self.run_operations()

    def run_operations(self):
        self.read_frames()
        # todo Add music and logo functions
        self.complete_operation()
        remove("".join(self.save_path.split(".")[:-1]) + "_tmp.avi")

    def read_frames(self):  # Reads the frames in the source video.

        used_frames = list()

        for i in range(ceil(self.video_length / self.cut_length)):
            cut_location = randint(0, self.length - self.cut_length)

            if self.repeatable:
                cut_location = randint(0, self.length - self.cut_length)

            else:
                y = 0
                while (any(x in used_frames
                           for x in list(range(cut_location - self.fps, cut_location + self.cut_length + self.fps + 1)))
                       and y < 5):
                    cut_location = randint(0, self.length - self.cut_length)
                    y += 1

            used_frames.extend(list(range(cut_location, cut_location + self.cut_length + 1)))
            self.capture.set(cv2.CAP_PROP_POS_FRAMES, cut_location)

            for x in range(self.cut_length):
                self.write_frame(i, x)
                self.update_progress(i, x)
                self.display_progress()

        self.capture.release()
        self.writer.release()

    def write_frame(self, i, x):  # Writes frames to the temporary output file.
        ret, self.frame = self.capture.read()
        self.writer.write(self.frame)

    def update_progress(self, i, x):  # Updates the progress.
        self.progress = ceil((i * self.cut_length + x) / self.video_length * 100)

    def display_progress(self):  # Displays the progress.
        if self.progress > self.last_progress:
            self.last_progress = self.progress
            stdout.write("\r%d%%" % self.progress)
            stdout.flush()

    # todo Add music and logo functions

    def complete_operation(self):
        clip = VideoFileClip("".join(self.save_path.split(".")[:-1]) + "_tmp.avi")
        clip.write_videofile(self.save_path, fps=self.fps, verbose=False, logger=None)
        stdout.write("\r%s" % "Operation completed!")
        stdout.flush()
