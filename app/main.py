import streamlit as st
from annealing.handler import annealing_handler, InvalidNumberGroupError

with st.form("annealing_form"):
    group_input = st.text_area(
        "前回のチーム分けをメンバーはカンマ区切り，チームは改行区切りで入力してください", value="A, B, C \nD, E, F\nG, H, I"
    )
    n_groups = st.number_input("グループ数を入力してください", value=3, min_value=1)
    max_iter = st.number_input(
        "iterを回す数を入力してください", value=1000, min_value=100, max_value=5000, step=100
    )

    submitted = st.form_submit_button("submit")
    if submitted:
        try:
            txt = annealing_handler(group_input, n_groups, max_iter)
        except InvalidNumberGroupError as e:
            txt = str(e)
        except Exception:
            txt = "error"
        st.write("グループ分けは次の通りです．")
        st.text(txt)
