# Import everything needed to edit video clips
from moviepy.editor import *
from moviepy.video.fx.resize import resize
import time
from timeit import default_timer as timer


class Resolution:
    """
    A class to handle video resolution.
    """

    __width = 0
    __height = 0

    @staticmethod
    def set_resolution(width: int, height: int):
        """
        Set the resolution for the video.

        Args:
            width (int): Width of the video.
            height (int): Height of the video.
        """
        Resolution.__width = width
        Resolution.__height = height

    @staticmethod
    def width() -> int:
        """
        Get the width of the video.

        Returns:
            int: Width of the video.
        """
        return Resolution.__width
    
    @staticmethod
    def height() -> int:
        """
        Get the height of the video.

        Returns:
            int: Height of the video.
        """
        return Resolution.__height


class Audio:
    """
    A class to manage audio in video clips.
    """

    def __init__(self):
        self.__audio_clips = []

    def add_audio(self, audio_file_path: str, audio_start: int = 0, audio_end: int = 0, audio_volume: float = 1.0, play_audio_at: int = 0) -> None:
        """
        Add audio to the video.

        Args:
            audio_file_path (str): Path to the audio file.
            audio_start (int, optional): Start time for the audio. Defaults to 0.
            audio_end (int, optional): End time of the audio. Defaults to 0.
            audio_volume (float, optional): Volume of the audio.
            play_audio_at (int, optional): Play audio at given seconds.
        """

        audio_clip = AudioFileClip(audio_file_path)
        audio_clip = audio_clip.subclip(min(audio_clip.duration, audio_start), min(audio_clip.duration, audio_end))
        audio_clip = audio_clip.fx(afx.volumex, audio_volume)
        audio_clip = audio_clip.set_start(play_audio_at)
        self.__audio_clips.append(audio_clip)

    def _set_audio_clip(self, clip: VideoFileClip | CompositeVideoClip) -> VideoFileClip | CompositeVideoClip:
        """
        Set the audio clip for a video.

        Args:
            clip (VideoFileClip | CompositeVideoClip): Video clip to set audio to.

        Returns:
            VideoFileClip | CompositeVideoClip: Video clip with audio added.
        """

        if self.__audio_clips:
            clip = clip.set_audio(CompositeAudioClip(self.__audio_clips))
        
        return clip


class TitleCard(Audio):
    """
    A class to create a title card for a video.
    """

    def __init__(self, bg_video_path: str, duration: int):
        super().__init__()

        self.__bg_video_path = bg_video_path
        self.__duration = duration
        self.__text_clips = []

    def add_text(self, text: str, postionY: int, font: str, font_size: int, color: str = "white", start: int = 1, fadein: int = 1) -> None:
        """
        Add text to the title card.

        Args:
            text (str): Text content.
            postionY (int): Y position of the text.
            font (str): Font to use.
            font_size (int): Font size.
            color (str, optional): Text color. Defaults to "white".
            start (int, optional): Start time for the text. Defaults to 1.
            fadein (int, optional): Fade-in duration. Defaults to 1.
        """

        txt_overlay = TextClip(text, font= font, fontsize= font_size, color= color)
        txt_overlay = txt_overlay.set_position(('center', postionY)).set_start(start).set_end(self.__duration).crossfadein(fadein)

        self.__text_clips.append(txt_overlay)

    def make_title_card(self) -> CompositeVideoClip:
        """
        Create the title card as a CompositeVideoClip.

        Returns:
            CompositeVideoClip: Composite video clip for the title card.
        """

        bg_clip = VideoFileClip(self.__bg_video_path).subclip(0, self.__duration)
        bg_clip = self._set_audio_clip(bg_clip)
        bg_clip = bg_clip.fx(vfx.resize, width= Resolution.width(), height= Resolution.height())

        return CompositeVideoClip([bg_clip] + self.__text_clips)


class Slide(Audio):
    """
    A class to create a slide in a video.
    """

    def __init__(self, image_path: str, slide_duration: int):
        super().__init__()

        self.__image_path = image_path
        self.__slide_duration = slide_duration
        self.__text_clips = []

    def __create_text(self, text: str, font: str, font_size: int, text_bg_path: str, text_color: str, duration: int) -> CompositeVideoClip:
        """
        Create a text overlay.

        Args:
            text (str): Text content.
            font (str): Font to use.
            font_size (int): Font size.
            text_bg_path (str): Path to the text background.
            text_color (str): Text color.
            duration (int): Duration of the text overlay.

        Returns:
            CompositeVideoClip: Composite video clip for the text overlay.
        """
         
        text_duration = self.__slide_duration * 0.45 if duration == -1 else duration

        txt_clip = TextClip(text, font= font, fontsize= font_size, color= text_color)
        txt_width, txt_height = txt_clip.size

        txt_bg = ImageClip(text_bg_path)
        txt_bg = resize(txt_bg, (txt_width * 1.4, txt_height * 1.4))
        txt_bg = txt_bg.set_duration(text_duration)

        txt_clip = txt_clip.set_position('center').set_start(1).set_end(text_duration).crossfadein(1)

        return CompositeVideoClip([txt_bg, txt_clip])
    
    def add_text(self, text: str, postion: tuple[int, int], font: str, font_size: int, text_bg_path: str, text_color: str = "white", direction: str = "right", start: int = 0, text_duration: int = -1) -> None:
        """
        Add text to the slide.

        Args:
            text (str): Text content.
            postion (tuple): Position coordinates (x, y) for the text.
            font (str): Font to use.
            font_size (int): Font size.
            text_bg_path (str): Path to the text background.
            text_color (str, optional): Text color. Defaults to "white".
            direction (str, optional): Direction of text animation. Defaults to "right".
            start (int, optional): Start time for the text. Defaults to 0.
            text_duration (int, optional): Duration for the text. Defaults to -1.
        """

        txt_overlay = self.__create_text(text, font, font_size, text_bg_path, text_color, text_duration)
        txt_overlay_dim = txt_overlay.size
        txt_overlay = txt_overlay.set_fps(60)
        if direction == "left":
            txt_overlay = txt_overlay.set_position(lambda t: (min(txt_overlay_dim[0] + postion[0], t * 1000) - txt_overlay_dim[0], Resolution.height() - (txt_overlay_dim[1] + postion[1])))
        else:
            txt_overlay = txt_overlay.set_position(lambda t: (Resolution.width() - min(txt_overlay_dim[0] + postion[0], t * 1000), Resolution.height() - (txt_overlay_dim[1] + postion[1])))

        self.__text_clips.append(txt_overlay.set_start(start))

    def make_slide(self) -> CompositeVideoClip:
        """
        Create the slide as a CompositeVideoClip.

        Returns:
            CompositeVideoClip: Composite video clip for the slide.
        """

        img_clip = ImageClip(self.__image_path).set_duration(self.__slide_duration)
        img_clip = self._set_audio_clip(img_clip)
        img_clip = resize(img_clip, (Resolution.width(), Resolution.height()))

        return CompositeVideoClip([img_clip] + self.__text_clips)


class EndCard(Audio):
    """
    A class to create an end card for a video.
    """

    def __init__(self, end_video_path: str, duration: int):
        super().__init__()

        self.__end_video_path = end_video_path
        self.__duration = duration
        self.__text_clips = []

    def add_text(self, text: str, postionY: int, font: str, font_size: int, color: str = "white", start: int = 1, fadein: int = 1) -> None:
        """
        Add text to the end card.

        Args:
            text (str): Text content.
            postionY (int): Y position of the text.
            font (str): Font to use.
            font_size (int): Font size.
            color (str, optional): Text color. Defaults to "white".
            start (int, optional): Start time for the text. Defaults to 1.
            fadein (int, optional): Fade-in duration. Defaults to 1.
        """

        txt_overlay = TextClip(text, font= font, fontsize= font_size, color= color)
        txt_overlay = txt_overlay.set_position(('center', postionY)).set_start(start).set_end(self.__duration).crossfadein(fadein)

        self.__text_clips.append(txt_overlay)
    
    def make_end_card(self) -> CompositeVideoClip:
        """
        Create the end card as a CompositeVideoClip.

        Returns:
            CompositeVideoClip: Composite video clip for the end card.
        """

        end_clip = VideoFileClip(self.__end_video_path).subclip(0, self.__duration)
        end_clip = self._set_audio_clip(end_clip)
        end_clip = end_clip.fx(vfx.resize, width= Resolution.width(), height= Resolution.height())

        return CompositeVideoClip([end_clip] + self.__text_clips)
    

class RenderClips(Audio):
    """
    A class to render video clips.
    """

    def __init__(self, clips: list):
        super().__init__()

        self.__final_clip = concatenate_videoclips(clips)
        self.__sub_clip = None

    @staticmethod
    def __render_time(func):
        """
        Decorator to measure rendering time.

        Args:
            func (function): Function to be decorated.

        Returns:
            function: Decorated function.
        """

        def wrapper(*args, **kwargs):
            start = timer()
            result = func(*args, **kwargs)
            end = timer()
            print(f"Render copleted in: {int((end - start))} seconds")

            return result
        
        return wrapper

    def sub_clip(self, start: int, end: int) -> None:
        """
        Subset the final video clip based on the provided start and end times.

        Args:
            start (int): Start time for subsetting.
            end (int): End time for subsetting.
        """

        duration = self.__final_clip.duration
        self.__sub_clip = self.__final_clip.subclip(min(duration, start), min(duration, end))

    @__render_time
    def render(self, output_filename: str = f"SE-{time.strftime('%#d-%#m-%Y')}", audio: bool = True, fps: int = 60, preset: str = "medium", codec: str = None, threads: int = 2) -> None:
        """
        Render the video.

        Args:
            output_filename (str, optional): Output filename. Defaults to "SE-{current date}".
            audio (bool, optional): Include audio. Defaults to True.
            fps (int, optional): Frames per second. Defaults to 60.
            preset (str, optional): Encoding preset. Defaults to "medium".
            codec (str, optional): Video codec. Defaults to None.
            threads (int, optional): Number of threads for rendering. Defaults to 2.
        """

        if self.__sub_clip:
            self.__sub_clip = self._set_audio_clip(self.__sub_clip)
            self.__sub_clip.write_videofile(output_filename, audio= audio, fps= fps, preset= preset, codec= codec, threads= threads)
        else:
            self.__final_clip = self._set_audio_clip(self.__final_clip)
            self.__final_clip.write_videofile(output_filename, audio= audio, fps= fps, preset= preset, codec= codec, threads= threads)