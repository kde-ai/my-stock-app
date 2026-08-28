import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

# ────────────────────────────────
# 페이지 기본 설정
# ────────────────────────────────
st.set_page_config(page_title="주가 조회 앱", page_icon="📈", layout="centered")

# 제목과 설명
st.title("📈 나만의 주가 조회 앱")
st.write("궁금한 종목 코드를 입력하면 최근 1년간의 주가 흐름을 그래프로 보여드려요!")
st.write("예시: 삼성전자 → `005930.KS` / 애플 → `AAPL`")

# ────────────────────────────────
# 종목 입력창
# ────────────────────────────────
ticker_input = st.text_input("종목 코드를 입력하세요", value="005930.KS")

if ticker_input:
    try:
        # yfinance로 최근 1년 데이터 불러오기
        ticker = yf.Ticker(ticker_input)
        df = ticker.history(period="1y")

        if df.empty:
            # 데이터가 없으면 안내 메시지
            st.warning("데이터를 찾을 수 없어요. 종목 코드를 다시 확인해주세요!")
        else:
            # ────────────────────────────────
            # 현재가 & 1년 등락률 계산
            # ────────────────────────────────
            first_price = df["Close"].iloc[0]   # 1년 전 가격
            last_price = df["Close"].iloc[-1]   # 오늘(최근) 가격
            change_pct = (last_price - first_price) / first_price * 100

            # 지표 카드 2개를 나란히 보여주기
            col1, col2 = st.columns(2)
            col1.metric(label="현재가", value=f"{last_price:,.2f}")
            col2.metric(
                label="1년 등락률",
                value=f"{change_pct:+.2f}%",
                delta=f"{change_pct:+.2f}%"
            )

            # ────────────────────────────────
            # 꺾은선 그래프 그리기
            # ────────────────────────────────
            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df["Close"],
                    mode="lines",
                    name="종가",
                    line=dict(color="royalblue", width=2)
                )
            )
            fig.update_layout(
                title=f"{ticker_input} 최근 1년 주가 흐름",
                xaxis_title="날짜",
                yaxis_title="가격",
                template="plotly_white"
            )

            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        # 예상치 못한 오류가 나도 앱이 멈추지 않도록 안내
        st.error("앗, 문제가 생겼어요! 종목 코드를 다시 확인해주세요.")
