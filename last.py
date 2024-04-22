from moviepy.editor import *

path = 'D:/Drom'

clip1 = VideoFileClip(f'{path}/mix.mp4')
clip2 = VideoFileClip(f'{path}/last.jpg').set_duration(4)

combined = CompositeVideoClip([clip1, clip2.set_start(27).crossfadein(3)])
combined.write_videofile(f'{path}/final.mp4', threads=12, preset="ultrafast")
