from moviepy.editor import *

path = 'D:/Drom/source'

clip1 = VideoFileClip(f'{path}/gtmk_1.MP4').subclip(120, 180).fx(vfx.speedx, 2.5)#.fx(vfx.colorx, 1.5)
clip2 = VideoFileClip(f'{path}/gtmk_2.MP4').subclip(120, 180).fx(vfx.speedx, 3)#.fx(vfx.colorx, 1.5)
clip3 = VideoFileClip(f'{path}/gtmk_3.MP4').subclip(120, 180).fx(vfx.speedx, 1.5)#.fx(vfx.colorx, 1.5)
clip4 = VideoFileClip(f'{path}/gtmk_4.MP4').subclip(120, 180).fx(vfx.speedx, 2)#.fx(vfx.colorx, 1.5)

combined = concatenate_videoclips([clip1, clip2, clip3, clip4])
combined.write_videofile(f'{path}/mix.mp4', threads=12, audio=False, verbose=False, preset="ultrafast")
