import flet as ft
from flet import Page as pG
from flet import (View)
from flet import (RouteChangeEvent, ViewPopEvent)
from Utility import ROOTPATH
from views import Home, Play, PlayExpand


def main(page: pG) -> None:
    # Meta
    if True:
        page.window_width = 400
        page.window_height = 100
        page.window_resizable = False
        page.padding = 0
        page.window_frameless = True # to add frames
        page.window_title_bar_hidden = True
        page.window_title_bar_buttons_hidden = True
        page.window_bgcolor = ft.colors.TRANSPARENT
        page.bgcolor = ft.colors.TRANSPARENT
        page.window_always_on_top = True

    audio1 = ft.Audio(src= ROOTPATH)
    page.overlay.append(audio1)
    
    def route_change(e: RouteChangeEvent) -> None:
        #Home
        page.views.clear()
        page.views.append(Home(page))

        if page.route == '/':
            ...

        if page.route == '/play':
            page.views.append(Play(page, audio1))
        
        if page.route == '/expand':
            page.views.append(PlayExpand(page, audio1))

    def view_pop(e: ViewPopEvent) -> None:
        page.views.pop()
        top_view: View = page.views[-1]
        page.go(top_view.route)
    
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")