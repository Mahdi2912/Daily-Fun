import requests
import subprocess
from datetime import datetime

def get_guess_the_word():
    try:
        # Use random word API, e.g. random-word-api.herokuapp.com
        word_resp = requests.get("https://random-word-api.herokuapp.com/word?number=1")
        if word_resp.status_code == 200:
            word = word_resp.json()[0]
            # Use dictionary API to get definition
            dict_resp = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
            if dict_resp.status_code == 200:
                definitions = dict_resp.json()[0]['meanings'][0]['definitions']
                definition = definitions[0]['definition']
                return f"Definition: {definition}\n\n(Answer: {word})"
            else:
                # fallback if no definition
                return f"Guess the word starting with '{word[0].upper()}'\n\n(Answer: {word})"
    except Exception:
        pass
    # fallback
    return "Definition: A domesticated carnivorous mammal typically kept as a pet or for catching mice.\n\n(Answer: Cat)"

def get_daily_quote():
    try:
        response = requests.get("https://api.quotable.io/random")
        if response.status_code == 200:
            data = response.json()
            content = data.get("content")
            author = data.get("author")
            return f'"{content}" — {author}'
    except Exception:
        pass
    return '"Be yourself; everyone else is already taken." — Oscar Wilde'  # fallback quote

def get_fun_fact():
    try:
        response = requests.get("http://numbersapi.com/random/trivia?json")
        if response.status_code == 200:
            data = response.json()
            return data.get("text")
    except Exception:
        pass
    return "Honey never spoils and has been found edible after thousands of years."  # fallback fact

def get_daily_content():
    today = datetime.now().strftime("%Y-%m-%d")
    guess_word = get_guess_the_word()
    quote = get_daily_quote()
    fact = get_fun_fact()

    content = f"""## 📅 {today}

### 🧩 Guess the Word  
*{guess_word}*

---

### 💬 Daily Quote  
{quote}

---

### 🧐 Fun Fact  
{fact}

---

"""
    return content

def append_to_file(filename, content):
    with open(filename, "a", encoding="utf-8") as f:
        f.write(content)

def git_commit_and_push():
    try:
        subprocess.run(["git", "add", "daily_digest.md"], check=True)
        subprocess.run(["git", "commit", "-m", f"Daily update {datetime.now().strftime('%Y-%m-%d')}"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("Committed and pushed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {e}")

if __name__ == "__main__":
    filename = "daily_digest.md"
    daily_content = get_daily_content()
    append_to_file(filename, daily_content)
    git_commit_and_push()
