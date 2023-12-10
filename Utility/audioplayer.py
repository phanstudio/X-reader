import flet as ft
import flet.canvas as cv
from .utility import *

class Track(ft.GestureDetector):
    def __init__(self, audio, on_change_position, width= 100, parent: ft.WindowDragArea= None):
        super().__init__()

        self.content = ft.Container(
            content=cv.Canvas(
                on_resize=self.canvas_resized,
                shapes=[
                    cv.Rect(
                        x=0,
                        y=0,
                        height=5,
                        border_radius=3,
                        paint=ft.Paint(color= DEFAULT_COLOR),
                        width=100,
                    ),
                    cv.Rect(
                        x=0,
                        y=0,
                        height=5,
                        border_radius=3,
                        paint=ft.Paint(color=ACCENT_COLOR),
                        width=0,
                    ),
                ],
            ),
            height=10,
            width=width,
        )
        self.parent = parent
        self.audio = audio
        self.audio_duration = None
        self.on_pan_start = self.find_position
        self.on_pan_update = self.find_position
        # self.on_tap = self.tap_position
        self.on_hover = self.change_cursor
        self.on_change_position = on_change_position

    def canvas_resized(self, e: cv.CanvasResizeEvent):
        self.track_width = e.width
        e.control.shapes[0].width = e.width
        e.control.update()

    def tap_position(self, e:ft.ControlEvent):
        print('drag instead')

    def find_position(self, e):
        position = int(self.audio_duration * e.local_x / self.track_width)
        position = max(
                0, min(position, self.audio_duration)
            )
        self.content.content.shapes[1].width = max(
            0, min(e.local_x, self.track_width)
        )
        self.update()
        self.on_change_position(position)

    def change_cursor(self, e: ft.HoverEvent):
        e.control.mouse_cursor = ft.MouseCursor.CLICK
        if self.parent != None:
            # self.parent.disabled = True
            # self.parent.update()
            ...
        e.control.update()

class hover_button(ft.GestureDetector):
    def __init__(self, controls, bgcolor = ft.colors.TRANSPARENT, onclick = None):
        super().__init__()
        self.content = ft.Container(
            controls,
            bgcolor= bgcolor,
            border_radius= 2,
            padding= ft.padding.symmetric(horizontal=3, vertical= 1),
            expand= True,
            on_click= onclick
        )
        self.on_hover = self.onhover
    
    def onhover(self, e: ft.HoverEvent):
        e.control.mouse_cursor = ft.MouseCursor.CLICK
        e.control.update()

class Audioplayer():
    def __init__(self, head:ft.Container) -> None:
        self.head = head

    def loads(self, e): # this to load text
        self.head.Pg.session.set('pasted_currrent', self.head.current)
        if self.head.started:
            self.head.started = False
            self.head.audio1.play()
        if self.head.nexted:
            self.head.nexted = False
            self.head.audio1.play()
        if self.head.skip:
            position = self.head.skip
            self.head.skip = False
            self.head.audio1.play()
            self.head.audio1.pause()
            self.head.audio1.seek(position)
            self.head.audio1.resume()
            self.head.Pg.update()

    def change_position(self, e:ft.ControlEvent):
        current = self.head.current
        self.head.position = round(sum(self.head.meta[1][:current]))*1000 + int(e.data) # make animation smother
        progress = self.head.position / self.head.total
        self.head.track_canvas.content.content.shapes[1].width = (progress* self.head.track_canvas.track_width)
        self.head.update()
    
    def seek_position(self, position):
        for i in range(len(self.head.meta[1])):
            if round(sum(self.head.meta[1][:i])*1000) <= position < round(sum(self.head.meta[1][:i+1])*1000):
                self.head.current = i
                position = position - round(sum(self.head.meta[1][:i])*1000)
                self.head.skip = position
                self.load(self.head.current)
                self.head.audio1.play()
                break
    
    def nexts(self, e):
        if e.data == 'completed':
            self.head.nexted = True
            self.head.current += 1
            if self.head.current == self.head.meta[-1]:
                self.head.nexted = False
                self.reload()
            else:
                self.load(self.head.current)

    def reload(self):
        self.head.current = 0
        self.head.position = 0
        self.head.track_canvas.content.content.shapes[1].width = (0)
        self.head.track_canvas.update()

    def ff_song(self, e: ft.ControlEvent):
        new_position = (int(self.head.position) - round(sum(self.head.meta[1][:self.head.current])*1000))+ (10-1)*1000
        self.head.position = round(sum(self.head.meta[1][:self.head.current])*1000) + new_position
        progress = self.head.position / self.head.total
        if progress < 1:
            self.head.track_canvas.content.content.shapes[1].width = (progress* self.head.track_canvas.track_width)
            if not new_position <= round(self.head.meta[1][self.head.current]*1000):
                for i in range(len(self.head.meta[1])): # use numpy to simplify
                    if round(sum(self.head.meta[1][:i])*1000) < self.head.position < round(sum(self.head.meta[1][:i+1])*1000):
                        self.head.current = i
                        position = new_position - round(sum(self.head.meta[1][:i])*1000)
                        self.head.skip = position
                        self.load(self.head.current)
                        self.head.audio1.play()
                        break
            else:
                self.head.seek_position(new_position)
        self.head.update()

    def fr_song(self, e: ft.ControlEvent):
        new_position = (int(self.head.position) - round(sum(self.head.meta[1][:self.head.current])*1000)) - (10-1)*1000
        self.head.position = round(sum(self.head.meta[1][:self.head.current])*1000) + new_position
        if self.head.position < 0: self.head.position = 0
        progress = self.head.position / self.head.total
        if progress < 1:
            self.head.track_canvas.content.content.shapes[1].width = (progress* self.head.track_canvas.track_width)
            
            if not new_position >= 0:
                for i in range(len(self.head.meta[1])): # use numpy to simplify
                    if round(sum(self.head.meta[1][:i])*1000) <= self.head.position < round(sum(self.head.meta[1][:i+1])*1000): # decayng function
                        self.head.current = i
                        position = new_position - round(sum(self.head.meta[1][:i])*1000)
                        self.head.skip = position
                        self.load(self.head.current)
                        self.head.audio1.play()
                        break
            else:
                self.seek_position(new_position)
        self.head.update()

    def load(self, n):
        path = f'{ROOTPATH}/temp_audio/{n}.wav'
        self.head.audio1.src = path
        self.head.audio1.update()

    def play(self, e):
        self.reload()
        self.head.started = True
        self.load(self.head.current)
        self.head.audio1.play()
