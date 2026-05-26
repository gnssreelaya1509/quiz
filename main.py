import flet as ft
import threading
import time
from core.engine import GameEngine

timer_running = False


def load_q(e):
    global timer_running
    timer_running = False  # Stop the previous timer if it exists
    time.sleep(0.2)  # Small delay to let the old thread exit

    question_data = engine.get_auto_question()
    current_q.update(question_data)
    quiz_text.value = current_q["q"]
    player_a_input.value = ""
    status.value = ""
    action_area.content = submit_btn

    # Timer Logic
    total_seconds = (int(min_input.value) * 60) + int(sec_input.value)
    timer_running = True  # Signal that a new timer has started

    def countdown():
        for remaining in range(total_seconds, -1, -1):
            if not timer_running: break  # Stop if another button was clicked
            mins, secs = divmod(remaining, 60)
            time_display.value = f"{mins:02d}:{secs:02d}"
            page.update()
            time.sleep(1)

        if timer_running:  # Only trigger if this timer finished naturally
            status.value = "Time's Up!\nGame Over!"
            status.color = "red"
            quiz_text.value = "Click Start to try again."
            action_area.content = start_btn
            page.update()

    threading.Thread(target=countdown, daemon=True).start()
    page.update()

def main(page: ft.Page):
    page.title = "Infinite Quiz Master"
    page.theme_mode = "dark"
    page.bgcolor = "#0F172A"
    page.padding = 30

    engine = GameEngine()
    current_q = {"q": "", "a": ""}

    # UI Elements
    score_text = ft.Text("0", size=32, weight="bold", color="#38BDF8")
    quiz_text = ft.Text("Press Start to begin.", size=22, text_align=ft.TextAlign.CENTER)
    player_a_input = ft.TextField(label="Answer (True/False)", border_color="#38BDF8")
    status = ft.Text("", size=16, weight="bold")
    time_display = ft.Text("00:00", size=40, weight="bold", color="#FBBF24")

    min_input = ft.TextField(label="Mins", value="0", width=80)
    sec_input = ft.TextField(label="Secs", value="10", width=80)
    action_area = ft.Container()

    # --- Game Logic ---
    def load_q(e):
        question_data = engine.get_auto_question()
        current_q.update(question_data)
        quiz_text.value = current_q["q"]
        player_a_input.value = ""
        status.value = ""
        action_area.content = submit_btn

        # Timer Logic
        total_seconds = (int(min_input.value) * 60) + int(sec_input.value)

        def countdown():
            for remaining in range(total_seconds, -1, -1):
                mins, secs = divmod(remaining, 60)
                time_display.value = f"{mins:02d}:{secs:02d}"
                page.update()
                time.sleep(1)

            # Game Over State
            status.value = "Time's Up!\nGame Over!"
            status.color = "red"
            quiz_text.value = "Click Start to try again."
            action_area.content = start_btn  # Bring back Start button
            page.update()

        threading.Thread(target=countdown, daemon=True).start()
        page.update()

    def check_ans(e):
        if not player_a_input.value.strip():
            status.value = "⚠️ Please fill the answer!"
            status.color = "orange"
        elif player_a_input.value.lower() == current_q["a"].lower():
            engine.update_score(True)
            status.value = "Correct! +25 XP"
            status.color = "#4ADE80"
            score_text.value = str(engine.data['score'])
            action_area.content = next_btn  # Allow moving forward
        else:
            status.value = f"Wrong! Correct: {current_q['a']}"
            status.color = "#F87171"
            action_area.content = next_btn  # Allow moving forward

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