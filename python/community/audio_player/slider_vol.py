#!/usr/bin/env python3

import flet
from flet import (
    Page,
    Audio,
    IconButton,
    ProgressBar,
    Row,
    Column,
    icons,
    Slider,
)


def main(page: Page):
    page.window_width = 320
    page.window_height = 256
    page.theme_mode = "dark"

    def progress(_):
        curr, tot = int(audio.get_current_position()), int(audio.get_duration())
        pb.value = curr / tot
        print(f"Current Progress: {curr}/{tot} (ms)")
        page.update()

    def play_pause(e):
        print(e.data)
        if e.data == "playing":
            pp_button.icon = icons.PAUSE_SHARP
            pp_button.on_click = lambda _: audio.pause()
        elif e.data == "paused":
            pp_button.icon = icons.PLAY_ARROW_SHARP
            pp_button.on_click = lambda _: audio.resume()
        elif e.data == "completed":
            pp_button.icon = icons.PLAY_ARROW_SHARP
            pp_button.on_click = lambda _: audio.play()
            pb.value = 1
        page.update()

    def vol_change(_):
        audio.volume = vol.value
        audio.update()
        print(f"Current Volume: {vol.value}")

    audio = Audio(
        src="file:///home/koton-bads/Documents/Python/Flet/Audio/assets/audio.mp3",
        on_position_changed=progress,
        on_state_changed=play_pause,
        autoplay=True,
    )

    pb = ProgressBar(
        value=0,
        # width=page.width,
        bgcolor="#1a1b26",
    )

    page.overlay.append(audio)
    page.add(
        Column(
            [
                Row(
                    [
                        IconButton(
                            icon=icons.FAST_REWIND_SHARP,
                            on_click=lambda _: audio.seek(
                                int(audio.get_current_position()) - 1_000
                            ),
                        ),
                        pp_button := IconButton(),
                        IconButton(
                            icon=icons.FAST_FORWARD_SHARP,
                            on_click=lambda _: audio.seek(
                                int(audio.get_current_position()) + 1_000
                            ),
                        ),
                    ],
                    alignment="center",
                ),
                pb,
                vol := Slider(
                    max=1,
                    min=0,
                    on_change=vol_change,
                ),
            ]
        )
    )
    page.update()


if __name__ == "__main__":
    flet.app(target=main)
