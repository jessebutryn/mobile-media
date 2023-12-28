import cv2
from mm.file import get_file_size
import subprocess
import json
import math

def get_video_info(file_path):
	result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'stream', '-of', 'json', file_path], capture_output=True, text=True)
	data = json.loads(result.stdout)
	file_size = get_file_size(file_path)

	video_stream = next((stream for stream in data['streams'] if stream['codec_type'] == 'video'), None)
	audio_stream = next((stream for stream in data['streams'] if stream['codec_type'] == 'audio'), None)

	resolution = str(video_stream['height']) + 'x' + str(video_stream['width'])
	aspect_ratio = video_stream.get('display_aspect_ratio', 'N/A')
	video_bitrate = video_stream.get('bit_rate', 'N/A')
	audio_bitrate = audio_stream.get('bit_rate', 'N/A')

	table = {
		"Video Codec": video_stream['codec_long_name'],
		"Aspect Ratio": aspect_ratio,
		"Video bitrate": video_bitrate,
		"height": video_stream['height'],
		"width": video_stream['width'],
		"Resolution": resolution,
		"Audio Codec": audio_stream['codec_long_name'],
		"Audio Channels": audio_stream['channels'],
		"Audio Channel Layout": audio_stream['channel_layout'],
		"Audio bitrate": audio_bitrate,
		"File Size": file_size,
	}
	return table

def print_video_info(data):
	video_stream = next((stream for stream in data['streams'] if stream['codec_type'] == 'video'), None)
	audio_stream = next((stream for stream in data['streams'] if stream['codec_type'] == 'audio'), None)

	resolution = str(video_stream['height']) + 'x' + str(video_stream['width'])
	video_bitrate = video_stream.get('bit_rate', 'N/A')
	audio_bitrate = audio_stream.get('bit_rate', 'N/A')

	table = {
		"Video Codec": video_stream['codec_long_name'],
		"Aspect Ratio": video_stream['display_aspect_ratio'],
		"Video bitrate": video_bitrate,
		"height": video_stream['height'],
		"width": video_stream['width'],
		"Resolution": resolution,
		"Audio Codec": audio_stream['codec_long_name'],
		"Audio Channels": audio_stream['channels'],
		"Audio Channel Layout": audio_stream['channel_layout'],
		"Audio bitrate": audio_bitrate,
		"File Size": data['file_size'],
	}
	table_as_list = [[key, value] for key, value in table.items()]
	print(tabulate(table_as_list, headers=["Attribute", "Value"], tablefmt="simple"))

def convert(input_file, output_file, info):
	max_width = 1280
	max_height = 720
	codec = 'libx264'
	audio_codec = 'aac'
	video_bitrate = '706k'
	audio_bitrate = '192k'

	width = info['width']
	height = info['height']

	width_scale = max_width / width
	height_scale = max_height / height

	min_scale = min(width_scale, height_scale)
	new_width = int(math.trunc(width * min_scale / 2) * 2)
	new_height = int(math.trunc(height * min_scale / 2) * 2)

	command = [
		'ffmpeg',
		'-i', input_file,
		'-vf', f'scale={new_width}:{new_height}',
		'-c:v', codec,
		'-b:v', video_bitrate,
		'-c:a', audio_codec,
		'-b:a', audio_bitrate,
		output_file
	]

	subprocess.run(command, check=True)
