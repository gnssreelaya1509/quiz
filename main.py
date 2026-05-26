import flet as ft
from core.engine import BaseEngine

def main(page: ft.Page):
    page.title = "New Flet Project"
    engine = BaseEngine()
    page.add(ft.Text("Automated Setup Successful!", size=30))

if __name__ == "__main__":
    ft.run(main)
