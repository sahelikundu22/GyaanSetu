import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def render_comparison(chapters_data, chapters_list):
    st.subheader("🔍 Compare Chapters")
    
    col1, col2 = st.columns(2)
    with col1:
        ch1 = st.selectbox("Chapter 1", chapters_list, key="ch1")
    with col2:
        ch2 = st.selectbox("Chapter 2", chapters_list, key="ch2")
    
    if ch1 and ch2 and ch1 != ch2:
        att1 = chapters_data[ch1]
        att2 = chapters_data[ch2]
        
        avg1 = sum(s/t for s, t in att1) / len(att1) * 100
        avg2 = sum(s/t for s, t in att2) / len(att2) * 100
        latest1 = att1[0][0]/att1[0][1] * 100
        latest2 = att2[0][0]/att2[0][1] * 100
        best1 = max(s/t for s, t in att1) * 100
        best2 = max(s/t for s, t in att2) * 100

        left_col, right_col = st.columns([1, 1])

        # LEFT SIDE
        with left_col:
            st.markdown(f"**{ch1}**")
            c1, c2, c3 = st.columns(3)
            c1.metric("Avg", f"{avg1:.1f}%", f"{avg1 - avg2:.1f}%")
            c2.metric("Latest", f"{latest1:.1f}%", f"{latest1 - latest2:.1f}%")
            c3.metric("Best", f"{best1:.1f}%", f"{best1 - best2:.1f}%")

            st.markdown(f"**{ch2}**")
            c1, c2, c3 = st.columns(3)
            c1.metric("Avg", f"{avg2:.1f}%", f"{avg2 - avg1:.1f}%")
            c2.metric("Latest", f"{latest2:.1f}%", f"{latest2 - latest1:.1f}%")
            c3.metric("Best", f"{best2:.1f}%", f"{best2 - best1:.1f}%")

            better = ch1 if avg1 > avg2 else ch2
            st.success(f"Better: {better}")

        # RIGHT SIDE (SMALL GRAPH)
        with right_col:
            fig, ax = plt.subplots(figsize=(3,2))

            metrics = ['Avg', 'Latest', 'Best']
            val1 = [avg1, latest1, best1]
            val2 = [avg2, latest2, best2]

            x = np.arange(len(metrics))

            ax.bar(x - 0.15, val1, 0.3, label=ch1)
            ax.bar(x + 0.15, val2, 0.3, label=ch2)

            ax.set_xticks(x)
            ax.set_xticklabels(metrics, fontsize=8)
            ax.legend(fontsize=7)

            plt.tight_layout()

            st.pyplot(fig, use_container_width=False)