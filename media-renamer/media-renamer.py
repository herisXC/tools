from PIL import Image
from pymediainfo import MediaInfo
from datetime import datetime
import pytz
import os
import argparse
from termcolor import colored


valid_photo_extensions = [".jpg", ".jpeg"]
valid_video_extensions = [".mp4", ".mov"]


def read_photo_original_datetime(photo_path):
    date_time_original = Image.open(photo_path)._getexif()[36867]
    print("DateTime Original: " + date_time_original)
    date_time_original_obj = datetime.strptime(date_time_original, "%Y:%m:%d %H:%M:%S")
    return date_time_original_obj.strftime("%Y-%m-%d_%H:%M:%S")


def read_video_encoded_datetime(video_path):
    media_info = MediaInfo.parse(video_path)
    for track in media_info.tracks:
        if track.track_type == 'General':
            print(track.encoded_date)
            encoded_date = datetime.strptime(track.encoded_date, "UTC %Y-%m-%d %H:%M:%S").replace(tzinfo=pytz.UTC)
            return encoded_date.astimezone().strftime("%Y-%m-%d_%H:%M:%S")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', required=True, help='Path to the folder where media files are located')
    parser.add_argument('-o', '--overwrite', type=bool, default='false', help='Determines whether files should be overwritten (default: %(default)s)')
    return parser.parse_args()


def main():
    args = parse_args()

    if not os.path.exists(args.path):
        print(colored("Path with media files does not exists", "red"))
        exit(-1)

    for root, directories, files in os.walk(args.path):
        for file in files:
            file_ext = os.path.splitext(file)[1]
            if file_ext.lower() in valid_photo_extensions:
                print("Image: {}".format(os.path.join(root, file)))
                print("New name: {}\n".format(read_photo_original_datetime(os.path.join(root, file))))
            elif file_ext.lower() in valid_video_extensions:
                print("Video: {}".format(os.path.join(root, file)))
                print("New name: {}\n".format(read_video_encoded_datetime(os.path.join(root, file))))


if __name__ == '__main__':
    main()