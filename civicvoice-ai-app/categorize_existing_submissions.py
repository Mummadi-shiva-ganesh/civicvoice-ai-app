import sqlite3
import openai

# OpenAI API Key
openai.api_key = "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"

CATEGORIES = [
    "Roads/Transport",
    "Water",
    "Electricity",
    "Sanitation",
    "Health",
    "Education",
    "Other"
]

def categorize_issue_with_openai(issue_text):
    system_prompt = f"You are an assistant that categorizes civic problems into one of these categories: {', '.join(CATEGORIES)}. Only return the category name."
    user_prompt = f"Problem: {issue_text}\nCategory:"
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=10,
            temperature=0
        )
        category = response.choices[0].message.content.strip()
        if category not in CATEGORIES:
            category = "Other"
        return category
    except Exception as e:
        print(f"AI categorization failed for: {issue_text}\nError: {e}\nDefaulting to 'Other'.")
        return "Other"

def main():
    conn = sqlite3.connect("civicvoice.db")
    c = conn.cursor()
    c.execute("SELECT id, issue_text FROM submissions WHERE category IS NULL OR category = ''")
    rows = c.fetchall()
    print(f"Found {len(rows)} uncategorized submissions.")
    for row in rows:
        sub_id, issue_text = row
        if not issue_text or not issue_text.strip():
            continue
        category = categorize_issue_with_openai(issue_text)
        c.execute("UPDATE submissions SET category = ? WHERE id = ?", (category, sub_id))
        print(f"Submission {sub_id} categorized as '{category}'.")
    conn.commit()
    conn.close()
    print("Done updating categories.")

if __name__ == "__main__":
    main() 