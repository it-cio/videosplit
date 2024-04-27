import random
from math import ceil
from os import remove
from random import randint
from sys import stdout

import cv2
from moviepy.editor import *
from moviepy.audio.fx.audio_loop import audio_loop
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.io.VideoFileClip import VideoFileClip


class Divider:
    def __init__(self,
                 video_race, video_pilot,
                 music_path, logo_path, end_logo_path,
                 save_path, temp_path,
                 video_length, cut_length):
        self.video_race = video_race
        self.video_pilot = video_pilot
        self.music_path = music_path
        self.logo_path = logo_path
        self.save_path = save_path
        self.temp_path = temp_path
        self.end_logo_path = end_logo_path

        # video_list, file_list = [], []
        # ext = [".mp4", ".avi", ".wmv", ".mov", ".mkv"]
        # for file in os.listdir(self.video_path):
        #     if file.lower().endswith(tuple(ext)) and '~$' not in file:
        #         clip_duration = VideoFileClip(f"{self.video_path}/{file}").duration
        #         clip_start = clip_duration / 4
        #         clip_end = clip_duration - clip_duration / 4
        #         file_list.append(file)
        #         video_list.append(VideoFileClip(f'{self.video_path}/{file}')
        #                           .subclip(clip_start, clip_end)
        #                           .fx(vfx.speedx, 1))
        # if len(video_list) > 1:
        #     combined = concatenate_videoclips(video_list)
        #     combined.write_videofile(f"{self.temp_path}_video.mp4",
        #                              fps=60, threads=12, audio=False, verbose=False)
        # else:
        #     with (open(f"{self.video_path}/{file_list[0]}", 'rb') as src,
        #           open(f"{self.temp_path}_video.mp4", 'wb') as dst):
        #         dst.write(src.read())
            # os.rename(f"{self.video_path}/{file_list[0]}", f"{self.temp_path}_video.mp4")

        # clip1_duration = VideoFileClip(video_race).duration
        # clip1_start = clip1_duration / 2 - video_length
        # clip1_end = clip1_duration / 2 + video_length
        #
        # clip2_duration = VideoFileClip(video_pilot).duration
        # clip2_start = clip2_duration / 2 - video_length
        # clip2_end = clip2_duration / 2 + video_length

        def set_duration(path, length):
            clip_duration = VideoFileClip(path).duration
            clip_start = round(clip_duration / 2 - length)
            clip_end = round(clip_duration / 2 + length)
            return clip_start, clip_end

        race = (VideoFileClip(video_race)
                .subclip(','.join(str(time) for time in set_duration(video_race, video_length)))
                .fx(vfx.speedx, 1.2))

        pilot = (VideoFileClip(video_pilot)
                 .subclip(','.join(str(time) for time in set_duration(video_pilot, video_length)))
                 .fx(vfx.speedx, 1.2)
                 .resize(0.40))

        combined = CompositeVideoClip([race, pilot.set_start(0).set_position((0.58, 0.04), relative=True)])
        combined.write_videofile(f"{self.temp_path}_video.mp4", fps=60, threads=12, audio=False, verbose=False)

        self.capture = cv2.VideoCapture(f"{self.temp_path}_video.mp4")
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

        self.writer = cv2.VideoWriter(f"{self.temp_path}_tmp.mp4",
                                      cv2.VideoWriter_fourcc(*'mp4v'), self.fps, (self.width, self.height))
        self.progress = 0
        self.last_progress = 0

        self.run_operations()

    def run_operations(self):
        self.read_frames()
        self.video_processing()
        self.complete_operation()

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

    def video_processing(self):
        music_list = []
        for file in os.listdir(self.music_path):
            music_list.append(file)
        clip = VideoFileClip(f"{self.temp_path}_tmp.mp4")
        music = AudioFileClip(f"{self.music_path}{random.choice(music_list)}")
        clip = clip.set_audio(audio_loop(music, duration=clip.duration))

        logo = (ImageClip(self.logo_path)
                .set_duration(clip.duration)
                .set_opacity(0.7)
                .set_position(("center", "bottom"))).resize(0.10)
        end_logo = (VideoFileClip(self.end_logo_path)
                     .set_duration(6))
        clip = CompositeVideoClip([clip, logo, end_logo.set_start(54).crossfadein(3)])

        stdout.write("\r%s" % "Mixing...")
        stdout.flush()
        clip.write_videofile(self.save_path, fps=self.fps, threads=12)
        clip.close()
        stdout.write("\r%s" % "Complete")
        stdout.flush()

    def complete_operation(self):
        stdout.write("\r%s" % "Operation completed!")
        stdout.flush()
        remove(f"{self.temp_path}_tmp.mp4")
        remove(f"{self.temp_path}_video.mp4")
