# 설치: python -m pip install streamlit supabase
# 실행: python -m streamlit run app.py
# 환경 변수 SUPABASE_URL, SUPABASE_KEY를 먼저 설정하세요.
# suggestions 테이블의 id와 created_at은 자동 생성 기본값이 필요합니다.

import os

import streamlit as st
from supabase import create_client

st.set_page_config(page_title="한 줄 건의함", page_icon="📮")

st.title("📮 한 줄 건의함")
st.write("이름 없이 자유롭게 건의해 주세요.")

try:
    supabase_url = os.environ["SUPABASE_URL"]
    supabase_key = os.environ["SUPABASE_KEY"]
except KeyError:
    st.error("환경 변수 SUPABASE_URL과 SUPABASE_KEY를 설정해 주세요.")
    st.stop()

try:
    supabase = create_client(supabase_url, supabase_key)
except Exception:
    st.error("Supabase 연결 설정을 확인해 주세요.")
    st.stop()

with st.form("suggestion_form", clear_on_submit=True):
    content = st.text_input(
        "건의 내용",
        placeholder="건의를 한 줄로 입력하세요."
    )
    submitted = st.form_submit_button("제출")

if submitted:
    content = content.strip()

    if not content:
        st.warning("건의 내용을 입력해 주세요.")
    else:
        try:
            supabase.table("suggestions").insert({
                "content": content,
                "category": "일반",
                "likes": 0,
            }).execute()
        except Exception:
            st.error("저장하지 못했습니다. 연결 상태와 테이블의 INSERT 권한을 확인해 주세요.")
        else:
            st.success("건의가 제출되었습니다!")

st.subheader("제출된 건의")
st.caption("최신순으로 표시됩니다.")

try:
    response = (
        supabase.table("suggestions")
        .select("id, content, category, likes, created_at")
        .order("created_at", desc=True)
        .order("id", desc=True)
        .execute()
    )
    suggestions = response.data or []
except Exception:
    st.error("건의를 불러오지 못했습니다. 연결 상태와 테이블의 SELECT 권한을 확인해 주세요.")
    st.stop()

if suggestions:
    for suggestion in suggestions:
        with st.container(border=True):
            st.text(suggestion["content"])
            category = suggestion.get("category") or "일반"
            likes = suggestion.get("likes") or 0
            st.caption(f"{category} · 좋아요 {likes}")
else:
    st.info("아직 제출된 건의가 없습니다.")