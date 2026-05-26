import requests

class GameEngine:
    def __init__(self):
        self.data = {"score": 0, "xp": 0}

    def get_auto_question(self):
        try:
            # Fetches a random True/False question
            response = requests.get("https://opentdb.com/api.php?amount=1&type=boolean").json()
            item = response['results'][0]
            return {
                "q": item['question'].replace("&quot;", '"').replace("&#039;", "'"),
                "a": item['correct_answer']
            }
        except:
            return {"q": "Error loading question. Check connection.", "a": "Error"}

    def update_score(self, correct):
        if correct:
            self.data["score"] += 1
            self.data["xp"] += 25