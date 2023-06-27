# import requests
import sys

import ffmpeg

# in_filename = "D:\\Learning\\Study_Videos_BE\\Study_Videos\\pexels-ἐμμανυελ--16764519-1920x1080-24fps.mp4"
# out_filename1 = "THUMBNAIL1.jpg"
# out_filename2 = "THUMBNAIL2.jpg"
# out_filename3 = "THUMBNAIL3.jpg"


def generate_thumbnail(in_filename, out_filename1, out_filename2, out_filename3):
    try:
        probe = ffmpeg.probe(in_filename)
        total_duration = float(probe["streams"][0]["duration"])
        time = float(probe["streams"][0]["duration"]) // 1.25
        time1 = float(probe["streams"][0]["duration"]) // 2
        time2 = float(probe["streams"][0]["duration"]) // 3
        # print(time, time1, time2, total_duration)
        width = probe["streams"][0]["width"]
        try:
            (
                ffmpeg.input(in_filename, ss=time)
                .filter("scale", width, -1)
                .output(out_filename1, vframes=1)
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=True)
            )
            (
                ffmpeg.input(in_filename, ss=time1)
                .filter("scale", width, -1)
                .output(out_filename2, vframes=1)
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=True)
            )
            (
                ffmpeg.input(in_filename, ss=time2)
                .filter("scale", width, -1)
                .output(out_filename3, vframes=1)
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=True)
            )
            return True
        except ffmpeg.Error as e:
            print(e.stderr.decode(), file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(str(e))


# generate_thumbnail(in_filename, out_filename1, out_filename2, out_filename3)
