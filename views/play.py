import flet as ft
from Utility import BACKGROUND_COLOR, TEXT_COLOR, ACCENT_COLOR, Track, hover_button, Audioplayer

class playpage(ft.Container):
    def __init__(self, page: ft.Page, audio1:ft.Audio, parent:ft.WindowDragArea):
        super().__init__()
        self.body = ft.Row(
            expand= True,
            alignment= ft.MainAxisAlignment.SPACE_BETWEEN
            )
        self.content = self.body
        self.bgcolor = BACKGROUND_COLOR
        self.Pg = page
        self.audio_properties = Audioplayer(self)
        self.audio1 = audio1
        self.current = self.Pg.session.get('pasted_currrent')
        self.position = 0
        self.audio1.on_loaded = self.audio_properties.loads
        self.audio1.on_state_changed = self.audio_properties.nexts
        self.audio1.on_position_changed = self.audio_properties.change_position
        self.meta = self.Pg.session.get('pasted_meta')
        self.border_radius = 10
        self.nexted = False
        self.audio_duration = round(self.meta[0]*1000)
        self.total = round(self.meta[0]*1000)
        self.started = False
        self.expand = True
        self.skip = False
        self.padding = 15
        mint = round(self.meta[0]//60) if round(self.meta[0]//60) > 10 else f'0{round(self.meta[0]//60)}'
        sec = round(self.meta[0]%60) if round(self.meta[0]%60) > 10 else f'0{round(self.meta[0]%60)}'
        self.track_canvas = Track(
            audio=self.audio1, on_change_position=self.audio_properties.seek_position, width= 200, parent= parent
        )
        self.track_canvas.audio_duration = self.audio_duration
        self.title = f'{mint}:{sec}'
        self.body.controls = [
            ft.Row(
                [
                    hover_button(
                        ft.Icon(
                            ft.icons.FORWARD_10_SHARP,
                            ),
                        onclick= self.audio_properties.ff_song,
                    ),
                    hover_button(
                        ft.Icon(
                            ft.icons.PLAY_CIRCLE,
                            color= ACCENT_COLOR,
                            size= 40,
                            ),
                        onclick= self.audio_properties.play,
                    ),
                    hover_button(
                        ft.Icon(
                            ft.icons.REPLAY_10_SHARP,
                            ),
                        onclick= self.audio_properties.fr_song,
                    ),
                    ft.Column(
                        spacing= 1,
                        alignment= ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Text(self.title, 
                                    color= TEXT_COLOR,
                                    size= 10,
                                    style= ft.TextStyle(
                                        weight= ft.FontWeight.BOLD,
                                    ),
                                ),
                            hover_button(
                                ft.Text('Expand',
                                    color= TEXT_COLOR,
                                    size = 10,
                                    style= ft.TextStyle(
                                        weight= ft.FontWeight.BOLD,
                                    ),
                                ),
                                bgcolor= ACCENT_COLOR,
                                onclick= lambda _: page.go('/expand')
                            )
                        ],
                    ),
                ],
                spacing= 0,
            ),
            self.track_canvas,
            ft.Row([
                hover_button(
                    ft.Icon(
                        ft.icons.REPEAT,
                    )
                ),
                hover_button(
                    ft.Icon(
                        ft.icons.VOLUME_UP,
                    )
                ),
            ], 
            spacing= 0
            ),
            ]
    
class Play(ft.View):
    def __init__(self, page:ft.Page, audio1:ft.Audio):
        super().__init__()
        self.expand = True
        page.window_width = 500
        page.window_height = 150
        self.bgcolor = ft.colors.TRANSPARENT
        self.route = '/play'
        self.parent = ft.WindowDragArea(maximizable= False)
        self.parent.content = playpage(page, audio1, self.parent)
        self.controls=[
            ft.IconButton(ft.icons.CLOSE,
                          bgcolor= BACKGROUND_COLOR,
                          icon_size= 15,
                          on_click= lambda _: self.on_close(page, audio1)# add pausing
                          ),
                self.parent,
                
        ]
        self.spacing= 5

    def on_close(self, page, audio1:ft.Audio):
        audio1.pause()
        audio1.update()
        page.go('/')
