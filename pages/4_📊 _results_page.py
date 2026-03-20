import streamlit as st
import sys, os
from collections import defaultdict
import matplotlib.pyplot as plt

# Path fix
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sidebar import render_sidebar
from database import get_scores_by_user


st.set_page_config(page_title="Subject Status", layout="wide")

render_sidebar()

st.title("📊 Subject Performance Report")

username = st.session_state.get("name", "student")
selected_subject = st.session_state.get("selected_subject")

data = get_scores_by_user(username)

if not data:
    st.info("No quiz attempts yet.")
    st.stop()

if not selected_subject:
    st.warning("Please select a subject from sidebar.")
    st.stop()


# ---------- FILTER DATA FOR SELECTED SUBJECT ----------

subject_data = []

for subject, chapter, score, total in data:
    if subject == selected_subject:
        subject_data.append((chapter, score, total))


if not subject_data:
    st.info(f"No attempts yet for {selected_subject}")
    st.stop()


# ---------- ORGANIZE DATA ----------

chapters = defaultdict(list)

total_score = 0
total_questions = 0

for chapter, score, total in subject_data:
    chapters[chapter].append((score, total))
    total_score += score
    total_questions += total


st.header(f"📘 {selected_subject}")

# ---------- PIE CHART ----------

st.subheader("📈 Overall Performance")

correct = total_score
incorrect = total_questions - total_score

fig1 = plt.figure()
plt.pie([correct, incorrect], labels=["Correct", "Incorrect"], autopct="%1.1f%%")
plt.title(f"{selected_subject} Accuracy")

st.pyplot(fig1)


# ---------- CHAPTER ANALYSIS ----------

chapter_names = []
avg_scores = []
weak_topics = []

for chapter in chapters:

    attempts = chapters[chapter]

    avg = sum(s/t for s, t in attempts) / len(attempts)
    percentage = int(avg * 100)

    chapter_names.append(chapter)
    avg_scores.append(percentage)

    if percentage < 50:
        weak_topics.append(chapter)

    st.subheader(f"📖 {chapter}")

    latest_score, latest_total = attempts[0]
    latest_pct = int((latest_score / latest_total) * 100)

    st.write(f"Latest Score: {latest_score}/{latest_total}")
    st.progress(latest_pct)

    with st.expander("📜 Attempt History"):
        for i, (s, t) in enumerate(attempts):
            pct = int((s/t) * 100)
            st.write(f"Attempt {i+1}: {s}/{t}")
            st.progress(pct)

    st.divider()


# ---------- BAR CHART ----------

st.subheader("📊 Chapter-wise Performance")

fig2 = plt.figure()
plt.bar(chapter_names, avg_scores)
plt.xlabel("Chapters")
plt.ylabel("Score (%)")
plt.title(f"{selected_subject} Performance")

st.pyplot(fig2)



# -----PERFORMANCE OVER TIME---- 
st.subheader("📈 Performance Over Time")

# Prepare data
attempt_numbers = []
scores_percent = []

for i, (chapter, score, total) in enumerate(subject_data[::-1]):  
    # reverse to show oldest → latest
    attempt_numbers.append(i + 1)
    percentage = int((score / total) * 100)
    scores_percent.append(percentage)

# Plot line graph

fig = plt.figure()
plt.plot(attempt_numbers, scores_percent, marker='o')

plt.xlabel("Attempt Number")
plt.ylabel("Score (%)")
plt.title(f"{selected_subject} Progress Over Time")

plt.xticks(attempt_numbers)

st.pyplot(fig)


# ------Chapter-wise Progress Over Time-----

st.subheader("📊 Chapter-wise Progress Over Time")

from collections import defaultdict
import matplotlib.pyplot as plt

# Organize attempts per chapter
chapter_attempts = defaultdict(list)

# Reverse to maintain time order (oldest → latest)
for chapter, score, total in subject_data[::-1]:
    percentage = int((score / total) * 100)
    chapter_attempts[chapter].append(percentage)

# Plot
fig = plt.figure()

for chapter in chapter_attempts:

    scores = chapter_attempts[chapter]
    attempts = list(range(1, len(scores) + 1))

    plt.plot(attempts, scores, marker='o', label=chapter)

plt.xlabel("Attempt Number")
plt.ylabel("Score (%)")
plt.title(f"{selected_subject} Chapter-wise Progress")

plt.legend()
plt.grid(True)

st.pyplot(fig)

# ---------- WEAK TOPICS ----------

st.subheader("⚠️ Weak Topics")

if weak_topics:
    for topic in weak_topics:
        st.error(f"{topic}")
else:
    st.success("No weak topics 🎉")