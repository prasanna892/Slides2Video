# Slides2Video

The Slides2Video is a Python module designed to facilitate the creation of videos with customized title cards, slides, and end cards.

## Classes

### `Resolution`

A class for setting the video resolution.

#### Methods

- `set_resolution(width: int, height: int) -> None`: Sets the resolution for the video.
- `width() -> int`: Returns the set width of the video.
- `height() -> int`: Returns the set height of the video.

### `Audio`

A class for managing audio in video clips.

#### Methods

- `add_audio(audio_file_path: str, start: int = 0, duration: int = 0) -> AudioFileClip`: Adds audio to the video.
- `set_audio_clip(clip: VideoFileClip) -> VideoFileClip`: Sets the audio clip for a video.

### `TitleCard(Audio)`

A class for creating a title card for a video.

#### Methods

- `add_text(text: str, postionY: int, font: str, font_size: int, color: str = "white", start: int = 1, fadein: int = 1) -> None`: Adds text to the title card.
- `make_title_card() -> CompositeVideoClip`: Creates the title card as a CompositeVideoClip.

### `Slide(Audio)`

A class for creating a slide in a video.

#### Methods

- `add_text(text: str, postion: tuple[int, int], font: str, font_size: int, text_bg_path: str, text_color: str = "white", direction: str = "right", start: int = 0, text_duration: int = -1) -> None`: Adds text to the slide.
- `make_slide() -> CompositeVideoClip`: Creates the slide as a CompositeVideoClip.

### `EndCard(Audio)`

A class for creating an end card for a video.

#### Methods

- `make_end_card() -> CompositeVideoClip`: Creates the end card as a CompositeVideoClip.

### `RenderClips(Audio)`

A class for rendering video clips.

#### Methods

- `sub_clip(start: int, end: int) -> None`: Subsets the final video clip based on the provided start and end times.
- `render(output_filename: str = "output_video.mp4", audio: bool = True, fps: int = 60, preset: str = "medium", codec: str = None, threads: int = 2) -> None`: Renders the final video.

## Usage

1. Create instances of `Resolution`, `TitleCard`, `Slide`, and `EndCard` based on your requirements.
2. Use the appropriate methods to set resolution, add text, and create video clips.
3. Concatenate the desired video clips.
4. Use the `RenderClips` class to render the final video.