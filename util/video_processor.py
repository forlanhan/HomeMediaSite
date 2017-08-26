import cv2
import images2gif
import math
from PIL import Image


def get_video_cap(video_file_name):
    video_cap = cv2.VideoCapture()
    assert video_cap.open(video_file_name), "Fail to open video."
    return video_cap


def get_video_basic_info(video_cap):
    """
    :param video_cap: cv2.VideoCapture
    :return: 
    """
    frame_rate = video_cap.get(cv2.CAP_PROP_FPS)

    return {
        "frame_rate": frame_rate,
        "size": {
            "width": video_cap.get(cv2.CAP_PROP_FRAME_WIDTH),
            "height": video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        },
        "time": video_cap.get(cv2.CAP_PROP_FRAME_COUNT) * 1.0 / frame_rate
    }


def get_video_preview(video_cap, file_name="out.gif", img_count=15, duration=0.5):
    """
    :param file_name:
    :param video_cap: cv2.VideoCapture
    :param img_count: int
    :param duration:  float
    :return: 
    """
    image_list = list()
    frame_count = int(video_cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_delta = int(math.floor(frame_count / img_count))
    img_index = range(0, frame_count, frame_delta)
    img_index = img_index[:img_count]
    for frame in img_index:
        video_cap.set(cv2.CAP_PROP_POS_FRAMES, frame)
        success, frame = video_cap.read()
        image_list.append(Image.fromarray(frame[:, :, [2, 1, 0]]))

    images2gif.writeGif(
        filename=file_name,
        images=image_list,
        duration=duration,
        repeat=True,
        subRectangles=False
    )


if __name__ == "__main__":
    vcap = get_video_cap("buffer/video_temp_15DD798DE29.mp4")
    print get_video_basic_info(vcap)
    get_video_preview(vcap)
