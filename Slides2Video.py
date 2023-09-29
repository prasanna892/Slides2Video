# Import everything needed to edit video clips
from moviepy.editor import *
from moviepy.video.fx.resize import resize
import time
from timeit import default_timer as timer


class Resolution:
    _width = 0
    _height = 0

    @staticmethod
    def set_resolution(width: int, height: int):
        Resolution._width = width
        Resolution._height = height

    @staticmethod
    def width() -> int:
        return Resolution._width
    
    @staticmethod
    def height() -> int:
        return Resolution._height


class Audio:
    def __init__(self):
        self._has_audio = False

    def add_audio(self, audio_file_path: str, start: int = 0, duration: int = 0) -> AudioFileClip:
        self._has_audio = True
        self._audio_clip = AudioFileClip(audio_file_path)
        self._audio_clip = self._audio_clip.subclip(start, min(self._audio_clip.duration, start + duration))

    def set_audio_clip(self, clip: VideoFileClip) -> VideoFileClip:
        if self._has_audio: 
            clip = clip.set_audio(self._audio_clip)
        
        return clip


class TitleCard(Audio):
    def __init__(self, bg_video_path: str, duration: int):
        super().__init__()

        self._bg_video_path = bg_video_path
        self._duration = duration
        self._text_clips = []
        self._has_audio = False

    def add_text(self, text: str, postionY: int, font: str, font_size: int, color: str = "white", start: int = 1, fadein: int = 1) -> None:
        txt_overlay = TextClip(text, font= font, fontsize= font_size, color= color)
        txt_overlay = txt_overlay.set_position(('center', postionY)).set_start(start).set_end(self._duration).crossfadein(fadein)

        self._text_clips.append(txt_overlay)

    def make_title_card(self) -> CompositeVideoClip:
        bg_clip = VideoFileClip(self._bg_video_path).subclip(0, self._duration)
        bg_clip = self.set_audio_clip(bg_clip)
        bg_clip = bg_clip.fx(vfx.resize, width= Resolution.width(), height= Resolution.height())

        return CompositeVideoClip([bg_clip] + self._text_clips)


class Slide(Audio):
    def __init__(self, image_path: str, slide_duration: int):
        super().__init__()

        self._image_path = image_path
        self._slide_duration = slide_duration
        self.text_clips = []

    def _create_text(self, text: str, font: str, font_size: int, text_bg_path: str, text_color: str, duration: int) -> CompositeVideoClip:
        text_duration = self._slide_duration * 0.45 if duration == -1 else duration

        txt_clip = TextClip(text, font= font, fontsize= font_size, color= text_color)
        txt_width, txt_height = txt_clip.size

        txt_bg = ImageClip(text_bg_path)
        txt_bg = resize(txt_bg, (txt_width * 1.4, txt_height * 1.4))
        txt_bg = txt_bg.set_duration(text_duration)

        txt_clip = txt_clip.set_position('center').set_start(1).set_end(text_duration).crossfadein(1)

        return CompositeVideoClip([txt_bg, txt_clip])
    
    def add_text(self, text: str, postion: tuple[int, int], font: str, font_size: int, text_bg_path: str, text_color: str = "white", direction: str = "right", start: int = 0, text_duration: int = -1) -> None:
        txt_overlay = self._create_text(text, font, font_size, text_bg_path, text_color, text_duration)
        txt_overlay_dim = txt_overlay.size
        txt_overlay = txt_overlay.set_fps(60)
        if direction == "left":
            txt_overlay = txt_overlay.set_position(lambda t: (min(txt_overlay_dim[0] + postion[0], t * 1000) - txt_overlay_dim[0], Resolution.height() - (txt_overlay_dim[1] + postion[1])))
        else:
            txt_overlay = txt_overlay.set_position(lambda t: (Resolution.width() - min(txt_overlay_dim[0] + postion[0], t * 1000), Resolution.height() - (txt_overlay_dim[1] + postion[1])))

        self.text_clips.append(txt_overlay.set_start(start))

    def make_slide(self) -> CompositeVideoClip:
        img_clip = ImageClip(self._image_path).set_duration(self._slide_duration)
        img_clip = self.set_audio_clip(img_clip)
        img_clip = resize(img_clip, (Resolution.width(), Resolution.height()))

        return CompositeVideoClip([img_clip] + self.text_clips)


class EndCard(Audio):
    def __init__(self, end_video_path: str, duration: int):
        super().__init__()

        self._end_video_path = end_video_path
        self._duration = duration
    
    def make_end_card(self) -> CompositeVideoClip:
        end_clip = VideoFileClip(self._end_video_path).subclip(0, self._duration)
        end_clip = self.set_audio_clip(end_clip)
        end_clip = end_clip.fx(vfx.resize, width= Resolution.width(), height= Resolution.height())

        return CompositeVideoClip([end_clip])
    

class RenderClips(Audio):
    def __init__(self, clips: list):
        super().__init__()

        self._final_clip = concatenate_videoclips(clips)
        self._final_clip = self.set_audio_clip(self._final_clip)

    @staticmethod
    def _render_time(func):
        def wrapper(*args, **kwargs):
            start = timer()
            result = func(*args, **kwargs)
            end = timer()
            print(f"Render copleted in: {int((end - start))} seconds")

            return result
        
        return wrapper

    def sub_clip(self, start: int, end: int) -> None:
        self._final_clip = self._final_clip.subclip(start, end)

    @_render_time
    def render(self, output_filename: str = f"SE-{time.strftime('%#d-%#m-%Y')}", audio: bool = True, fps: int = 60, preset: str = "medium", codec: str = None, threads: int = 2) -> None:
        self._final_clip.write_videofile(output_filename, audio= audio, fps= fps, preset= preset, codec= codec, threads= threads)