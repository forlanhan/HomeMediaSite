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
    vbi = dict()
    vbi["frame_rate"] = video_cap.get(cv2.CAP_PROP_FPS)
    vbi["frame_width"] = video_cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    vbi["frame_height"] = video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    vbi["frame_count"] = video_cap.get(cv2.CAP_PROP_FRAME_COUNT)
    vbi["constant_time"] = vbi["frame_count"] * 1.0 / vbi["frame_rate"]
    return vbi

def get_video_preview(video_cap, file_name="out.gif", img_count=15, duration=0.5):
    """
    
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
        repeat=True
    )


if __name__ == "__main__":
    vcap = get_video_cap("test.mp4")
    print get_video_basic_info(vcap)
    get_video_preview(vcap)
