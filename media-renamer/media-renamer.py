from PIL import Image
from pymediainfo import MediaInfo
from datetime import datetime
import pytz
import os
import argparse
from termcolor import colored

DATE_TIME_ORIGINAL_TAG = 36867
valid_photo_extensions = [".jpg", ".jpeg"]
valid_video_extensions = [".mp4", ".mov"]


def read_photo_original_datetime(photo_path):
    date_time_original = Image.open(photo_path)._getexif()[DATE_TIME_ORIGINAL_TAG]
    return datetime.strptime(date_time_original, "%Y:%m:%d %H:%M:%S")


def read_video_encoded_datetime(video_path):
    media_info = MediaInfo.parse(video_path)
    for track in media_info.tracks:
        if track.track_type == 'General':
            encoded_date = datetime.strptime(track.encoded_date, "UTC %Y-%m-%d %H:%M:%S").replace(tzinfo=pytz.UTC)
            return encoded_date.astimezone()


def rename_file(original_path, new_path):
    print("{} -> {}".format(colored(original_path, "yellow"), colored(new_path, "green")))
    os.rename(original_path, new_path)


def create_unique_file_name(output_dir_path, formatted_date, file_ext, file_name_postfix):
    file_name_candidate = formatted_date
    if file_name_postfix > 0:
        file_name_candidate += "-{}".format(file_name_postfix)
    if os.path.exists(os.path.join(output_dir_path, file_name_candidate + file_ext)):
        file_name_postfix += 1
        return create_unique_file_name(output_dir_path, formatted_date, file_ext, file_name_postfix)
    return file_name_candidate


def get_new_file_name(output_dir_path, media_creation_date, file_ext):
    formatted_date = media_creation_date.strftime("%Y-%m-%d_%H:%M:%S")
    return create_unique_file_name(output_dir_path, formatted_date, file_ext, 0)


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
                creation_date = read_photo_original_datetime(os.path.join(root, file))
                new_file_name = get_new_file_name(root, creation_date, file_ext)
                rename_file(os.path.join(root, file), os.path.join(root, new_file_name + file_ext))
            elif file_ext.lower() in valid_video_extensions:
                creation_date = read_video_encoded_datetime(os.path.join(root, file))
                new_file_name = get_new_file_name(root, creation_date, file_ext)
                rename_file(os.path.join(root, file), os.path.join(root, new_file_name + file_ext))


if __name__ == '__main__':
    main()