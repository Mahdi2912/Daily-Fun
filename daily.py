import requests
import subprocess
from datetime import datetime
import random

def get_riddle():
    try:
        response = requests.get("https://riddles-api.vercel.app/random", timeout=5)
        if response.status_code == 200:
            data = response.json()
            riddle = data.get("riddle", "I speak without a mouth and hear without ears. What am I?")
            answer = data.get("answer", "An echo")
            return f"Riddle: {riddle}\n(Answer: {answer})"
    except Exception:
        pass
    return "Riddle: I speak without a mouth and hear without ears. What am I?\n(Answer: An echo)"

def get_daily_quote():
    try:
        response = requests.get("https://zenquotes.io/api/random", timeout=5)
        if response.status_code == 200:
            data = response.json()
            quote = data[0]["q"]
            author = data[0]["a"]
            return f'"{quote}" — {author}'
    except Exception:
        pass
    return '"Be yourself; everyone else is already taken." — Oscar Wilde'

def get_fun_fact():
    try:
        response = requests.get("http://numbersapi.com/random/trivia?json", timeout=5)
        if response.status_code == 200:
            return response.json()["text"]
    except Exception:
        pass
    return "Honey never spoils and has been found edible after thousands of years."

def get_programming_tip():
    try:
        response = requests.get("https://api.adviceslip.com/advice", timeout=5)
        if response.status_code == 200:
            data = response.json()
            advice = data.get("slip", {}).get("advice")
            if advice:
                return advice
    except Exception:
        pass

    fallback_tips = [
        "Use meaningful variable names to improve code readability.",
        "Write comments to explain why, not what.",
        "Keep functions small and focused on a single task.",
        "Use version control to manage your code changes.",
        "Test your code frequently and automate tests where possible."
    ]
    return random.choice(fallback_tips)

def append_to_file(filename, content):
    with open(filename, "a", encoding="utf-8") as f:
        f.write(content + "\n\n")

def git_commit(commit_message):
    try:
        subprocess.run(["git", "add", "daily_digest.md"], check=True)
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Git commit failed: {e}")

def main():
    filename = "daily_digest.md"
    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Add date header
    append_to_file(filename, f"## 📅 {today}")
    git_commit(f"Start daily digest entry for {today}")

    # Riddles
    for i in range(3):
        riddle = get_riddle()
        content = f"🧩 Riddle #{i+1}:\n{riddle}"
        append_to_file(filename, content)
        git_commit(f"Added riddle #{i+1}")

    # Quotes
    for i in range(3):
        quote = get_daily_quote()
        content = f"💬 Daily Quote #{i+1}:\n{quote}"
        append_to_file(filename, content)
        git_commit(f"Added quote #{i+1}")

    # Fun Facts
    for i in range(3):
        fact = get_fun_fact()
        content = f"🧐 Fun Fact #{i+1}:\n{fact}"
        append_to_file(filename, content)
        git_commit(f"Added fun fact #{i+1}")

    # Programming Tip
    tip = get_programming_tip()
    content = f"💡 Programming Tip:\n{tip}"
    append_to_file(filename, content)
    git_commit("Added programming tip")

    # Final push
    try:
        subprocess.run(["git", "push"], check=True)
        print("All changes committed and pushed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Git push failed: {e}")

if __name__ == "__main__":
    main()
