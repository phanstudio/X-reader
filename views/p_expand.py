import flet as ft
from Utility import *

class textBox(ft.ListView):
    def __init__(self, page: ft.Page, defualt=1):
        super().__init__()
        self.expand = True
        self.padding = 40
        self.spacing = 20
        self.selected = defualt
        self.Pg = page
        self.meta = self.Pg.session.get('pasted_meta')
        self.content = self.Pg.session.get('pasted_content')
        self.controls = [
            self.Text_content(
                self.content[0],
                color= ACCENT_COLOR,
                style= ft.TextThemeStyle.HEADLINE_SMALL,
                text_align= ft.TextAlign.CENTER,
                overflow= ft.TextOverflow.ELLIPSIS
            ),
        ]

        first = [self.content[i] for i in range(len(self.content)) if i%2==0]
        second = [self.content[i] for i in range(len(self.content)) if i%2==1]

        if len(self.content) % 2 == 1:
            second.append(None)

        content = list(zip(first, second))

        for i in content:
            self.controls.append(self.paragraph(
                i
            ))

        self.highlight(defualt, default=True)

    def highlight(self, num, default= False):
        if not default:
            for i in self.controls[1:]:
                for j in i.controls:
                    j.color = PRIMARY_COLOR
            self.update()

        num_of_paragraphs = sum(len(i.controls) for  i in self.controls[1:])+1
        # can remove title        
        paragraph = round((num/2)+0.1) # calculated to work with 1,2 -> 0,1
        text = (num//2)//paragraph
        if num_of_paragraphs > num > 0:
           self.controls[paragraph].controls[text].color = ACCENT_COLOR
           if not default:
            self.controls[paragraph].controls[text].update()
            self.selected = num
    
    def paragraph(self, txt = ['','']):
        column = ft.Column(spacing= 0)
        for i in txt:
            if i == None: continue
            column.controls.append(self.Text_content(
                i,
                size= 12
            ))
        return column
    
    def Text_content(self, txt, color= PRIMARY_COLOR, overflow= None,
                     style= None, text_align= None, size = None):
        return ft.Text(
                txt,
                color= color,
                style= style,
                text_align= text_align,
                size= size,
                overflow= overflow
            )

class expandpage(ft.Container): # change all the assets
    def __init__(self, page: ft.Page, audio1):
        super().__init__()
        self.body = ft.Row(
            expand= True,
            alignment= ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment= ft.CrossAxisAlignment.START,
            spacing= 10
            )
        self.content = self.body
        self.bgcolor = BACKGROUND_COLOR
        self.Pg = page
        self.border_radius = 10
        self.expand = True
        self.audio_properties = Audioplayer(self)
        self.audio1 = audio1
        self.current = self.Pg.session.get('pasted_currrent')
        self.position = 0
        self.audio1.on_loaded = self.loads
        self.audio1.on_state_changed = self.audio_properties.nexts
        self.audio1.on_position_changed = self.audio_properties.change_position
        self.meta = self.Pg.session.get('pasted_meta')
        self.nexted = False
        self.started = False
        self.audio_duration = round(self.meta[0]*1000)
        self.total = round(self.meta[0]*1000)
        self.padding = 15
        self.skip = False
        self.text_box = textBox(page, defualt=self.current+1)

        self.track_canvas = Track(
            audio=self.audio1, on_change_position=self.audio_properties.seek_position, width= 400
        )
        self.track_canvas.audio_duration = self.audio_duration
        self.body.controls = [
            # item property
            ft.Column([
                hover_button(
                    ft.Icon(
                        ft.icons.PLAY_CIRCLE,
                        color= ACCENT_COLOR,
                        size= 40,
                    ),
                    onclick= self.audio_properties.play,
                ),
                ft.Container(ft.Column(
                    controls=[
                        hover_button(
                            ft.Icon(
                                ft.icons.FORWARD_10_SHARP,
                                color= PRIMARY_COLOR
                            ),
                            onclick= self.audio_properties.ff_song,
                        ),
                        hover_button(
                            ft.Icon(
                                ft.icons.REPLAY_10_SHARP,
                                color= PRIMARY_COLOR
                            ),
                            onclick= self.audio_properties.fr_song,
                        ),
                        hover_button(
                            ft.Icon(
                                ft.icons.REPEAT,
                                color= PRIMARY_COLOR
                            ),
                        ),
                        hover_button(
                            ft.Icon(
                                ft.icons.VOLUME_UP,
                                color= PRIMARY_COLOR
                            ),
                        ),
                    ],
                    spacing= 0,
                ),
                bgcolor= SECONDARY_COLOR,
                border_radius= 10
            ),
            ft.IconButton(ft.icons.CLOSE,
                bgcolor= BACKGROUND_COLOR,
                icon_size= 15,
                on_click= lambda _: self.on_close(page, audio1)
                ),
            ],
            horizontal_alignment= ft.CrossAxisAlignment.CENTER,
            ),
            # text area
            ft.Container(
                ft.Column([
                    self.track_canvas,
                    hover_button(
                        ft.Text('Only audio',
                            color= TEXT_COLOR,
                            size = 10,
                            style= ft.TextStyle(
                                weight= ft.FontWeight.BOLD,
                            ),
                        ),
                        bgcolor= ACCENT_COLOR,
                        onclick= lambda _: page.go('/play')
                        ),
                    ft.Container(
                        self.text_box,
                        bgcolor= SECONDARY_COLOR,
                        height= 380,
                        width= 570,
                        border_radius= 5
                    ),
                ],
                expand= 1, 
                alignment= ft.MainAxisAlignment.START),
                margin= ft.margin.all(8),
            )
        ]
    
    def loads(self, e):
        self.text_box.highlight(self.current+1)
        self.audio_properties.loads(e)

    def on_close(self, page, audio1:ft.Audio):
        audio1.pause()
        page.go('/')

class PlayExpand(ft.View):
    def __init__(self, page:ft.Page, audio1):
        super().__init__()
        self.expand = True
        page.window_width = 700
        page.window_height = 500
        self.bgcolor = ft.colors.TRANSPARENT
        self.route = '/expand'
        self.controls=[
            ft.WindowDragArea(
                expandpage(page, audio1),
                maximizable= False
            )
        ]
        self.spacing= 5
