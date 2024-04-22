from moviepy.editor import *

clip1 = VideoFileClip("trek_01.MP4").subclip(260, 420)
# clip2 = VideoFileClip("trek_02.MP4").fx(vfx.speedx, 1.5).fx(vfx.colorx, 1)
clip3 = VideoFileClip("trek_03.mp4")
clip4 = VideoFileClip("trek_04.mp4")
clip5 = VideoFileClip("trek_05.mp4")
clip6 = VideoFileClip("trek_06.mp4")
clip7 = VideoFileClip("trek_07.mp4")
clip8 = VideoFileClip("trek_08.mp4").subclip(165, 420).fx(vfx.speedx, 1.5).fx(vfx.colorx, 1)
clip9 = VideoFileClip("trek_09.mp4").subclip(5, 300)
clip10 = VideoFileClip("trek_10.mp4").subclip(30, 300)
clip11 = VideoFileClip("trek_11.mp4").subclip(8, 260).fx(vfx.speedx, 2).fx(vfx.colorx, 1.5)
clip12 = VideoFileClip("trek_12.mp4")
# clip13 = VideoFileClip("trek_13.mp4") Promo clip

combined = concatenate_videoclips(
    [clip1, clip3, clip4, clip5, clip6, clip7, clip8, clip9, clip10, clip11, clip12]
)
combined.write_videofile("trek_mix.mp4", threads=6, audio=False, verbose=False)
