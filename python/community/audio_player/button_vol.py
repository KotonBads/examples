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

    def vol_up(_):
        audio.volume += 0.1
        audio.update()
        print(f"Current Volume: {audio.volume}")

    def vol_down(_):
        audio.volume -= 0.1
        audio.update()
        print(f"Current Volume: {audio.volume}")

    audio = Audio(
        src="https://github.com/mdn/webaudio-examples/blob/main/audio-analyser/viper.mp3?raw=true",
        on_position_changed=progress,
        on_state_changed=play_pause,
        volume=0.5,
    )

    page.overlay.append(audio)
    page.add(
        Column(
            [
                Row(
                    [
                        IconButton(icon=icons.VOLUME_DOWN_SHARP, on_click=vol_down),
                        IconButton(
                            icon=icons.FAST_REWIND_SHARP,
                            on_click=lambda _: audio.seek(
                                int(audio.get_current_position()) - 1_000
                            ),
                        ),
                        pp_button := IconButton(
                            icon=icons.PLAY_ARROW_SHARP,
                            on_click=lambda _: audio.resume(),
                        ),
                        IconButton(
                            icon=icons.FAST_FORWARD_SHARP,
                            on_click=lambda _: audio.seek(
                                int(audio.get_current_position()) + 1_000
                            ),
                        ),
                        IconButton(icon=icons.VOLUME_UP_SHARP, on_click=vol_up),
                    ],
                    alignment="center",
                ),
                pb := ProgressBar(
                    value=0,
                    bgcolor="#1a1b26",
                ),
            ]
        )
    )
    page.update()


if __name__ == "__main__":
    flet.app(target=main)
