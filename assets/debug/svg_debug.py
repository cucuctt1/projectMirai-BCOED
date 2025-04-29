import flet as ft


def svg_decorator(func):
    def wrapper(*args, **kwargs):
        svg_body = func(*args, **kwargs)
        full_svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-40 -40 500 500">{svg_body}</svg>'

        def main(page: ft.Page):
            page.title = "SVG Viewer"
            svg_display =ft.Container(content = ft.Image(f'```xml\n{full_svg}\n```'),bgcolor="red")

            page.add(svg_display)
            page.add(ft.Text(value=full_svg,width=1000,height=900))

        ft.app(target=main)

    return wrapper



