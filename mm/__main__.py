#!/usr/bin/env python3
import argparse
from tabulate import tabulate
from mm.video import print_video_info
from mm.video import get_video_info
from mm.video import convert
from mm.file import is_directory_writable
from mm.file import get_file_path
from mm.file import get_basename
import pprint

def main():
	parser = argparse.ArgumentParser(description='Mobile Media - A tool to convert video files into a format playable on Chrysler uconnect devices.')
	parser.add_argument('video', type=str, help='The video file')
	parser.add_argument('-i', '--info', action='store_true', help='Return video information')
	parser.add_argument('-c', '--convert', action='store_true', help='Convert video to uconnect compatible format')
	parser.add_argument('-o', '--output', type=str, help='Path for output file.  If none specified the out file will be saved in the same directory as the input file')
	parser.add_argument('-n', '--name', type=str, help="Specify an output name.  If none specified the input name will be used with the mm_ prefix")

	args = parser.parse_args()
	video = args.video
	get_info = args.info
	out_dir = args.output
	out_file = args.name
	convert_file = args.convert
	
	info = get_video_info(video)

	if get_info:
		table_as_list = [[key, value] for key, value in info.items()]
		print(tabulate(table_as_list, headers=["Attribute", "Value"], tablefmt="simple"))
	
	if convert_file:
		if out_dir:
			try:
				is_directory_writable(out_dir)
			except Exception as e:
				return f"Output directory is not writeable: {e}"
		else:
			out_dir = get_file_path(video)
	
		if not out_file:
			out_file = "mm_" + get_basename(video)

		out_full_path = out_dir + "/" + out_file
		
		convert(video, out_full_path, info)

if __name__ == "__main__":
	main()
