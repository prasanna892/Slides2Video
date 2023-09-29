from Slides2Video import *
import time


def main():
    Resolution.set_resolution(1920, 1080)

    title_card = TitleCard("./resources/intro.mp4", 5)
    title_card.add_text(time.strftime("%#d - %#m - %#y"), 300, "Roboto-Light", 80)
    title_card.add_text("Example video", 460, "AbrilFatface-Regular", 110)
    title_card.add_text("created using Slide2Video", 640, "Roboto-Light", 90, start= 2)
    title_card_clip = title_card.make_title_card()

    animal_clips = []
    for img in ("lion", "tiger", "elephant", "fox"):
        slide = Slide(f"./resources/{img}.jpg", 5)
        slide.add_text(img, (0, 65), "PatuaOne-Regular", 70, "./resources/txt_bg.png")
        animal_clips.append(slide.make_slide())

    end_card = EndCard("./resources/end.mp4", 5).make_end_card()

    clips_list = [title_card_clip, *animal_clips, end_card]
    
    final_clip = RenderClips(clips_list)
    final_clip.add_audio("./resources/bg_music.mp3", 0, 5, 1, 0)
    final_clip.add_audio("./resources/bg_music.mp3", 5, 25, 3, 5)
    final_clip.add_audio("./resources/bg_music.mp3", 25, 30, 1, 25)
    final_clip.render(f"{time.strftime('%#d-%#m-%Y')}.mp4", True, 24, "medium", "nvenc_h264", 14)


if __name__ == "__main__":
    main()