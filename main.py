import flet as ft
import threading
import time
from core.engine import GameEngine


def main(page: ft.Page):
    page.title = "Infinite Quiz Master"
    page.theme_mode = "dark"
    page.bgcolor = "#0F172A"
    page.padding = 30

    engine = GameEngine()
    current_q = {"q": "", "a": ""}
    timer_running = [False]  # Using a list to make it mutable in nested functions

    # --- UI Elements ---
    score_text = ft.Text("0", size=32, weight="bold", color="#38BDF8")
    quiz_text = ft.Text("Press Start to begin.", size=22, text_align=ft.TextAlign.CENTER)
    player_a_input = ft.TextField(label="Answer (True/False)", border_color="#38BDF8")
    status = ft.Text("", size=16, weight="bold")
    time_display = ft.Text("00:00", size=40, weight="bold", color="#FBBF24")

    min_input = ft.TextField(label="Mins", value="0", width=80)
    sec_input = ft.TextField(label="Secs", value="10", width=80)
    action_area = ft.Container()

    # --- Helper Functions ---
    def load_q(e):
        timer_running[0] = False  # Stop any previous timer
        time.sleep(0.1)
        timer_running[0] = True

        question_data = engine.get_auto_question()
        current_q.update(question_data)
        quiz_text.value = current_q["q"]
        player_a_input.value = ""
        status.value = ""
        action_area.content = submit_btn

        # Safely get time values
        try:
            m = int(min_input.value) if min_input.value.strip() else 0
            s = int(sec_input.value) if sec_input.value.strip() else 0
        except ValueError:
            m, s = 0, 10

        total_seconds = (m * 60) + s

        def countdown():
            for remaining in range(total_seconds, -1, -1):
                if not timer_running[0]: break
                mins, secs = divmod(remaining, 60)
                time_display.value = f"{mins:02d}:{secs:02d}"
                page.update()
                time.sleep(1)

            if timer_running[0]:
                status.value = "Time's Up!\nGame Over!"
                status.color = "red"
                quiz_text.value = "Click Start to try again."
                action_area.content = start_btn
                page.update()

        threading.Thread(target=countdown, daemon=True).start()
        page.update()

    def check_ans(e):
        if not player_a_input.value.strip():
            status.value = "⚠️ Please fill the answer!"
            status.color = "orange"
        else:
            timer_running[0] = False  # Stop timer when answer is submitted
            if player_a_input.value.lower() == current_q["a"].lower():
                engine.update_score(True)
                status.value = "Correct! +25 XP"
                status.color = "#4ADE80"
                score_text.value = str(engine.data['score'])
            else:
                status.value = f"Wrong! Correct: {current_q['a']}"
                status.color = "#F87171"
            action_area.content = next_btn
        page.update()

    # --- Buttons ---
    start_btn = ft.ElevatedButton("START GAME", on_click=load_q, bgcolor="#38BDF8", color="white")
    next_btn = ft.ElevatedButton("NEXT QUESTION", on_click=load_q, bgcolor="#38BDF8", color="white")
    submit_btn = ft.ElevatedButton("SUBMIT ANSWER", on_click=check_ans, bgcolor="#38BDF8", color="white")

    action_area.content = start_btn

    page.add(
        ft.Row([
            ft.Container(
                content=ft.Column([
                    ft.Text("SCORE", size=10, weight="bold", color="grey"),
                    score_text
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=20, bgcolor="#1E293B", border_radius=20, width=150
            ),
            ft.Container(width=40),
            ft.Column([
                ft.Row([min_input, sec_input]),
                ft.Container(content=quiz_text, padding=20, bgcolor="#1E293B", border_radius=15, width=400),
                player_a_input,
                action_area,
                status,
                time_display
            ])
        ], alignment=ft.MainAxisAlignment.CENTER)
    )


ft.app(target=main)