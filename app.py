import streamlit as st
import matplotlib.pyplot as plt
import random

# クラシックギター ローポジションの音データ
NOTES_DATA = [
    {"name": "ミ", "string": 6, "fret": 0, "y": -7},
    {"name": "ファ", "string": 6, "fret": 1, "y": -6},
    {"name": "ソ", "string": 6, "fret": 3, "y": -5},
    {"name": "ラ", "string": 5, "fret": 0, "y": -4},
    {"name": "シ", "string": 5, "fret": 2, "y": -3},
    {"name": "ド", "string": 5, "fret": 3, "y": -2},
    {"name": "レ", "string": 4, "fret": 0, "y": -1},
    {"name": "ミ", "string": 4, "fret": 2, "y": 0},
    {"name": "ファ", "string": 4, "fret": 3, "y": 1},
    {"name": "ソ", "string": 3, "fret": 0, "y": 2},
    {"name": "ラ", "string": 3, "fret": 2, "y": 3},
    {"name": "シ", "string": 2, "fret": 0, "y": 4},
    {"name": "ド", "string": 2, "fret": 1, "y": 5},
    {"name": "レ", "string": 2, "fret": 3, "y": 6},
    {"name": "ミ", "string": 1, "fret": 0, "y": 7},
    {"name": "ファ", "string": 1, "fret": 1, "y": 8},
    {"name": "ソ", "string": 1, "fret": 3, "y": 9},
    {"name": "ラ", "string": 1, "fret": 5, "y": 10},
]

BUTTON_NAMES = ["ド", "レ", "ミ", "ファ", "ソ", "ラ", "シ"]

def init_session_state():
    if "current_note" not in st.session_state:
        st.session_state.current_note = random.choice(NOTES_DATA)
    if "correct_count" not in st.session_state:
        st.session_state.correct_count = 0
    if "total_count" not in st.session_state:
        st.session_state.total_count = 0
    if "feedback_msg" not in st.session_state:
        st.session_state.feedback_msg = None
    if "feedback_color" not in st.session_state:
        st.session_state.feedback_color = "black"

def next_question():
    st.session_state.current_note = random.choice(NOTES_DATA)
    st.session_state.feedback_msg = None

def check_answer(answer):
    st.session_state.total_count += 1
    correct_name = st.session_state.current_note["name"]
    string = st.session_state.current_note["string"]
    fret = st.session_state.current_note["fret"]
    
    if answer == correct_name:
        st.session_state.correct_count += 1
        st.session_state.feedback_color = "green"
        st.session_state.feedback_msg = f"✅ 正解！ 直前の音は {string}弦{fret}フレット の『{correct_name}』でした。"
    else:
        st.session_state.feedback_color = "red"
        st.session_state.feedback_msg = f"❌ 不正解... 直前の正解は {string}弦{fret}フレット の『{correct_name}』でした。"
        
    st.session_state.current_note = random.choice(NOTES_DATA)

def draw_music_sheet(note):
    fig, ax = plt.subplots(figsize=(6, 3))
    
    # 五線の描画 (y=0, 2, 4, 6, 8)
    for y in range(0, 9, 2):
        ax.axhline(y, color='black', linewidth=1.5)
        
    # ト音記号（テキストだと環境依存で文字化けするため、単純なG文字で代用するか省略します。今回は省略）
    # ax.text(-0.5, 4, '𝄞', fontsize=60, fontfamily='sans-serif', va='center', ha='right', color='black')
    
    y = note['y']
    
    # 音符の描画 (黒丸)
    ax.scatter(1, y, s=400, color='black', zorder=3)
    
    # 符尾の描画 (3線(y=4)より上は下向き、下は上向き)
    # 簡易的に直線を描画
    if y >= 4:
        # 下向き
        ax.plot([0.9, 0.9], [y, y-3], color='black', linewidth=2)
    else:
        # 上向き
        ax.plot([1.1, 1.1], [y, y+3], color='black', linewidth=2)
        
    # 加線の描画
    # y < 0 (下加線) の場合 (-2, -4, -6...)
    if y < 0:
        for line_y in range(-2, y - 1, -2):
            ax.plot([0.8, 1.2], [line_y, line_y], color='black', linewidth=2)
            
    # y > 8 (上加線) の場合 (10...)
    if y > 8:
        for line_y in range(10, y + 1, 2):
            ax.plot([0.8, 1.2], [line_y, line_y], color='black', linewidth=2)

    ax.set_ylim(-9, 12)
    ax.set_xlim(-1, 3)
    ax.axis('off')  # 枠線オフ
    
    # 背景白
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    
    return fig

def main():
    st.set_page_config(page_title="クラシックギター譜読みトライ！", layout="centered")
    
    # CSSでボタンなどをモバイル向けに大きくする
    st.markdown("""
        <style>
        .stButton button {
            width: 100%;
            height: 60px;
            font-size: 24px;
            font-weight: bold;
        }
        .feedback_text {
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("🎸 ギター譜読みトレーニング")
    
    init_session_state()
    
    # 統計情報の表示
    col_stats_1, col_stats_2, _ = st.columns([1, 1, 1])
    with col_stats_1:
        st.metric("正解数", f"{st.session_state.correct_count} / {st.session_state.total_count}")
    with col_stats_2:
        rate = (st.session_state.correct_count / st.session_state.total_count * 100) if st.session_state.total_count > 0 else 0
        st.metric("正答率", f"{rate:.1f}%")

    st.divider()

    # フィードバック表示
    if st.session_state.feedback_msg:
        color = st.session_state.feedback_color
        st.markdown(f'<div class="feedback_text" style="color: {color};">{st.session_state.feedback_msg}</div>', unsafe_allow_html=True)

    # 五線譜の描画
    fig = draw_music_sheet(st.session_state.current_note)
    st.pyplot(fig)
    
    st.markdown("### この音は何？")
    
    # 回答ボタンの配置 (2列または3列でモバイルでも押しやすく)
    cols1 = st.columns(4)
    for i, name in enumerate(BUTTON_NAMES[:4]):
        with cols1[i]:
            if st.button(name, key=f"btn_{name}", use_container_width=True):
                check_answer(name)
                st.rerun()

    cols2 = st.columns(3)
    for i, name in enumerate(BUTTON_NAMES[4:]):
        with cols2[i]:
            if st.button(name, key=f"btn_{name}", use_container_width=True):
                check_answer(name)
                st.rerun()
                
    st.divider()
    if st.button("🔄 やり直す (リセット)", type="secondary", use_container_width=True):
        st.session_state.clear()
        st.rerun()

if __name__ == "__main__":
    main()
