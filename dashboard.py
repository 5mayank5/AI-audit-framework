import streamlit as st
import sqlite3
import json
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="AI Audit Dashboard", layout="wide")

st.title("🧠 Agent-Based AI Audit Dashboard")

DB_NAME = "audit_results.db"

if not os.path.exists(DB_NAME):
    st.error("Database not found. Run main.py first.")
    st.stop()

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

cursor.execute("SELECT results FROM audit ORDER BY id DESC LIMIT 1")
row = cursor.fetchone()

if not row:
    st.warning("No audit records found. Run main.py first.")
    st.stop()

data = json.loads(row[0])

# --------------------------
# Summary Section
# --------------------------

col1, col2 = st.columns(2)

col1.metric("Total Risk Score", data["total_score"])
col2.metric("Severity Level", data["severity"])

st.divider()

# --------------------------
# Agent Breakdown Table
# --------------------------

st.subheader("📊 Agent Risk Breakdown")

agent_names = []
scores = []

for detail in data["details"]:
    agent_names.append(detail["agent"])
    scores.append(detail["score"])
    st.write(f"**{detail['agent']}** → {detail['score']}")

# --------------------------
# Visualization
# --------------------------

st.subheader("📈 Risk Score Visualization")

fig, ax = plt.subplots()
ax.bar(agent_names, scores)
ax.set_xlabel("Agents")
ax.set_ylabel("Risk Score")
plt.xticks(rotation=45)

st.pyplot(fig)

conn.close()