# Clip Extractor

**Depends:** 

pip moviepy

sudo apt install ffmpeg ImageMagick

**Usage:** ./clip_videos.sh /path/to/dir

**Description**

Gathers a list of video files in a directory.

Creates a directory called 'clips' within that directory and selects random sections, then writes a new file.

Edit clip_length and clip_range to adjust output.

Edit the regex pattern. e.g files with names containing episode numbers: S01E20 = r"S\d{2}E\d{2}".

The regex pattern is overlayed on the output video.

In the absence of any match the full filename is used. (may be clipped)

Result from Family Guy Episode. Every run would result in different output:



https://github.com/Scofferoff/clip_extractor/assets/12169861/07946108-3406-41dc-b7b6-9ed621056241

