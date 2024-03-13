from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.editor import CompositeVideoClip

import os
import random
import subprocess
import re

clip_length = 3 # Seconds for each clip
clip_range = 6 # Number of clips

pattern = r"S\d{2}E\d{2}" # Filenames need to contain Season and Episode e.g. S05E01 

def generate_random_times(duration):
    times = []
    for _ in range(clip_range):
        random_time = random.randint(60, int(duration) - 60)  # Ignore first and last minute
        times.append(random_time)
    times.sort()
    return times

def extract_episode(filename):
    match = re.search(pattern, filename)
    if match:
        return match.group()
    else:
        return filename
'''        
def get_bitrate(input_file):
    try:
        # Run ffprobe to get bitrate information
        ffprobe_cmd = f"ffprobe -v error -show_entries format=bit_rate -of default=noprint_wrappers=1:nokey=1 {input_file}"
        result = subprocess.run(ffprobe_cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            bitrate_str = result.stdout.strip()
            return int(bitrate_str)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred retrieving bitrate {input_file}: {e}")
    except Exception as e:
        print(f"An Error occurred: {e}")

        return None
'''        
def main(input_file):
    if not os.path.exists(input_file):
        print("Input file does not exist.")
        return
    
    # Sanitize paths    
    directory, filename = os.path.split(input_file)
    new_directory = os.path.join(directory, "clips")
    os.makedirs(new_directory, exist_ok=True)
    
    output_file = os.path.join(new_directory, os.path.splitext(filename)[0] + "_clips.mp4")
    episode = extract_episode(input_file) # for overlay of filename or episode
    
    video = VideoFileClip(input_file)
    duration = video.duration
    print(f"Duration: {duration}")
    video.close()
    
    if duration <= 120:
        print("Video is too short to extract clips.")
        return
    
    random_times = generate_random_times(duration)
    clips = []
    for time in random_times:
        if time + clip_length <= duration:
            #print(f"Time: {time}")
            clip = VideoFileClip(input_file).subclip(time, (time + clip_length))
            clips.append(clip)
        else:
            clip = VideoFileClip(input_file).subclip(duration - clip_length, duration)
            clip.append(clip)
    
    final_clip = concatenate_videoclips(clips)
    total_duration = sum([clip.duration for clip in clips])
    final_clip = final_clip.set_position(("center", "center")).set_duration(total_duration)
    
    # Overlay episode text at the bottom center of the output video
    episode_text = f"{episode}"
    episode_clip = TextClip(episode_text, font='DejaVuSans', fontsize=50, color='white')
    episode_clip = episode_clip.set_position(("center", "bottom"))
    episode_clip = episode_clip.set_duration(total_duration)
    
    # Composite the video clip and the episode text together
    final_clip = CompositeVideoClip([final_clip, episode_clip])
    '''
    # Retrieve bitrate from input file
    input_bitrate = get_bitrate(input_file)
    if input_bitrate:
        # Set bitrate for nvenc encoding
        nvenc_options = f"-b:v {input_bitrate} -c:v h264_nvenc"
    else:
        nvenc_options = "-c:v h264_nvenc"  # Default nvenc options
        
    final_clip.write_videofile(output_file, codec="libx264", fps=24, ffmpeg_params=nvenc_options)
    '''

    # Avoid process ending due to ffmpeg errors
    try:
        final_clip.write_videofile(output_file, codec="libx264", fps=24)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred processing {input_file}: {e}")
        return False
    except Exception as e:
        print(f"ffmpeg error occurred: {e}")
        return False
    
    print(f"Clips extracted and saved as {output_file}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python script.py input_file")
        sys.exit(1)
    
    main(sys.argv[1])
