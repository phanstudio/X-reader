import flet as ft
from pyperclip import paste
import pyttsx3, os, shutil
from Utility import BACKGROUND_COLOR, ACCENT_COLOR, TEXT_COLOR, ROOTPATH, full_lenght, remove

class homepage(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.body = ft.Row(
            expand= True,
            alignment= ft.MainAxisAlignment.SPACE_BETWEEN
            )
        self.content = self.body
        self.bgcolor = BACKGROUND_COLOR
        self.Pg = page
        self.border_radius = 10
        self.expand = True
        self.padding = 15
        self.progress_but = ft.Ref[ft.Icon]()
        self.progress_ring = ft.Ref[ft.ProgressRing]()
        self.engine = pyttsx3.init()
        self.body.controls = [
            ft.Row([
                ft.IconButton(ft.icons.CLOSE, on_click=self.close), # change this to option
                ft.Column(
                    spacing= 1,
                    alignment= ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Text('X Reader', 
                                color= TEXT_COLOR,
                                size= 14,
                                style= ft.TextStyle(
                                    weight= ft.FontWeight.BOLD,
                                ),
                            ),
                        ft.Text('Click the \'+\' botton to ',
                                color= TEXT_COLOR, 
                                size = 10,
                                spans=[
                                    ft.TextSpan(
                                        'add from clipboard',
                                        style= ft.TextStyle(
                                            weight= ft.FontWeight.W_600,
                                            color= ACCENT_COLOR,
                                            size= 11,
                                        )
                                    ),
                                ],
                                style= ft.TextStyle(
                                    weight= ft.FontWeight.BOLD,
                                ),
                            ),
                ],),
            ]),      
            ft.GestureDetector(
                ft.Container(
                    content= ft.Row([
                        ft.Icon(
                            ft.icons.ADD, 
                            color= TEXT_COLOR,
                            size= 18,
                            ref= self.progress_but
                            ),
                        ft.ProgressRing(
                            color= TEXT_COLOR,
                            visible= False,
                            ref= self.progress_ring,
                            width=18,
                            height=18,
                        )
                        ]),
                    bgcolor= ACCENT_COLOR,
                    padding= 10,
                    border_radius= 8,
                    on_click= self.onclick
                ),
                on_hover= self.onhover,  
            ),
        ]
    
    def onhover(self, e: ft.HoverEvent):
        e.control.mouse_cursor = ft.MouseCursor.CLICK
        e.control.update()
    
    def onclick(self, e: ft.TapEvent):
        # change to
        Pasted_content = [i for i in paste().replace('\r','\n').split('\n') 
                          if len(i) != 0]
        if len(Pasted_content) > 1:
            self.progress_but.current.visible = False
            self.progress_ring.current.visible = True
            self.update()
            self.Pg.session.set('pasted_content', Pasted_content)
            self.Pg.session.set('pasted_currrent', 0)
            #convert to audio
            self.make_audio(Pasted_content) #implement loading screen
            dur, total, length = full_lenght()
            self.Pg.session.set('pasted_meta', [total, dur, length])

            self.Pg.go('/play')
        else:
            ...
    
    def make_audio(self, txt):
        temp_path = f"{ROOTPATH}/temp_audio"
        if os.path.exists(temp_path): # implement memory
            shutil.rmtree(temp_path)
        os.mkdir(temp_path)

        def tts_thread(tex="", index=0):
            self.engine.save_to_file(tex, f'{temp_path}/{index}.wav')
            self.engine.runAndWait()
    
        for i, text in enumerate(txt):
            tts_thread(text, i)

    def close(self, e):
        remove()
        self.Pg.window_close()

class Home(ft.View):
    def __init__(self, page):
        super().__init__()
        self.expand = True
        self.bgcolor = ft.colors.TRANSPARENT
        page.window_width = 400
        page.window_height = 100
        self.route = '/'
        self.controls=[ft.WindowDragArea(
            homepage(page),
            maximizable= False
            )
        ]
        self.spacing= 26
        # self.padding = 0
        self.horizontal_alignment= ft.CrossAxisAlignment.CENTER
