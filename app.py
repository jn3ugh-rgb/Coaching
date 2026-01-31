import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime
from fpdf import FPDF

# ==========================================
# 0. 初期設定 & データ管理
# ==========================================
st.set_page_config(layout="wide", page_title="Life Mapping Console v7.1")

DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

DEFAULT_DATA = {
    "name": "",
    "date": datetime.now().strftime("%Y-%m-%d"),
    "temp_pin": "",
    "bedrock": "",
    "bedrock_note": "",
    "sediment": "",
    "sediment_note": "",
    "cliff": "",
    "slope": "",
    "goal": "",
    "action": ""
}

if "data" not in st.session_state:
    st.session_state.data = DEFAULT_DATA.copy()
else:
    for key, value in DEFAULT_DATA.items():
        if key not in st.session_state.data:
            st.session_state.data[key] = value

# --- ⚡️ オートセーブ関数 ---
def auto_save():
    if not st.session_state.data["name"]:
        filename = "autosave_draft.json"
    else:
        filename = f"{st.session_state.data['name']}_{st.session_state.data['date']}.json"
    
    filepath = os.path.join(DATA_DIR, filename)
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(st.session_state.data, f, ensure_ascii=False, indent=4)
        st.toast(f"💾 Auto-saved: {filename}", icon="✅")
    except Exception as e:
        print(f"Auto-save failed: {e}")

# --- 読み込み & 削除関数 ---
def load_data(filename):
    filepath = os.path.join(DATA_DIR, filename)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)
            new_data = DEFAULT_DATA.copy()
            new_data.update(loaded_data)
            st.session_state.data = new_data
        st.sidebar.success(f"📂 読み込み完了: {filename}")
    except Exception as e:
        st.sidebar.error(f"読み込みエラー: {e}")

def delete_data(filename):
    filepath = os.path.join(DATA_DIR, filename)
    try:
        os.remove(filepath)
        st.success(f"🗑️ 削除しました: {filename}")
        return True
    except Exception as e:
        st.error(f"削除エラー: {e}")
        return False

def get_saved_files():
    files = [f for f in os.listdir(DATA_DIR) if f.endswith('.json')]
    return sorted(files, reverse=True)

# ==========================================
# 📄 PDF生成クラス (IPAexゴシック対応)
# ==========================================
class PDFReport(FPDF):
    def header(self):
        # ↓↓↓ ここを変更しました (ipaexg.ttf を指定) ↓↓↓
        font_path = "ipaexg.ttf" 
        
        if os.path.exists(font_path):
            self.add_font('Japanese', '', font_path)
            self.set_font('Japanese', '', 10)
        else:
            self.set_font('Arial', '', 10)
        
        self.cell(0, 10, 'Life Mapping Fieldwork Log', align='R')
        self.ln(15)

    def chapter_title(self, label):
        self.set_font_size(14)
        self.set_fill_color(240, 242, 246) # 薄いグレー
        self.cell(0, 10, f"  {label}", fill=True, ln=True)
        self.ln(4)

    def chapter_body(self, text):
        self.set_font_size(11)
        self.multi_cell(0, 7, text)
        self.ln(8)

    def card_body(self, title, content):
        self.set_font_size(10)
        self.set_text_color(100, 100, 100)
        self.cell(0, 6, title, ln=True)
        self.set_text_color(0, 0, 0)
        self.set_font_size(12)
        self.multi_cell(0, 7, content, border='L')
        self.ln(6)

def generate_pdf(data):
    pdf = PDFReport()
    pdf.add_page()
    
    # フォントチェック (ipaexg.ttf)
    if not os.path.exists("ipaexg.ttf"):
        st.error("⚠️ フォント(ipaexg.ttf)が見つかりません。PDFが文字化けする可能性があります。")
        pdf.set_font("Arial", size=12)
    else:
        pdf.set_font("Japanese", size=12)

    # タイトル
    pdf.set_font_size(24)
    pdf.cell(0, 15, f"{data['name']}'s Fieldwork Log", ln=True, align='C')
    pdf.set_font_size(12)
    pdf.cell(0, 10, f"Date: {data['date']}", ln=True, align='C')
    pdf.ln(10)

    # Phase 1
    pdf.chapter_title("1. Bedrock (地盤・価値観)")
    pdf.chapter_body(data['bedrock'])
    
    # Phase 2
    pdf.chapter_title("2. Sediment (スキル・経験)")
    pdf.chapter_body(data['sediment'])

    # Phase 3
    pdf.chapter_title("3. Topography (地形再定義)")
    pdf.card_body("😱 Cliff (崖に見えているもの)", data['cliff'])
    pdf.card_body("🚶 Slope (登れる坂への再定義)", data['slope'])

    # Phase 4
    pdf.chapter_title("4. Routes (航路)")
    pdf.card_body("🏁 Destination (3ヶ月後のゴール)", data['goal'])
    pdf.card_body("👟 Next Action (最初の一歩)", data['action'])

    # 【修正ポイント】
    # encode('latin-1') を削除し、bytearray を bytes に変換して返すだけにする
    return bytes(pdf.output())

# ==========================================
# 1. サイドバー
# ==========================================
with st.sidebar:
    st.title("🧭 Mapping Console")
    st.caption("v7.1: IPAex Gothic Ready")
    
    app_mode = st.radio("App Mode", ["📝 セッション実施 (Edit)", "📂 過去ログ管理 (Archives)"])
    st.divider()

    if app_mode == "📝 セッション実施 (Edit)":
        menu = st.radio("フェーズ選択", [
            "0. 基本情報 (Setup)",
            "1. 地盤調査 (Bedrock)",
            "2. 堆積物確認 (Sediment)",
            "3. 地形測量 (Topography)",
            "4. 航路策定 (Routes)",
            "5. クライアント出力 (View)"
        ])
        
        st.divider()
        st.subheader("💾 Data Control")
        if st.button("Force Save"):
            auto_save()
            st.success("Saved!")
        
        saved_files = get_saved_files()
        if saved_files:
            selected_file = st.selectbox("Load Past Record", saved_files)
            if st.button("Load Selected"):
                load_data(selected_file)
                st.rerun()

# ==========================================
# 2. メイン画面
# ==========================================
def section_header(title, purpose, questions):
    st.title(title)
    st.info(f"**【目的】** {purpose}")
    with st.expander("🗣️ 参謀の問い", expanded=True):
        for q in questions:
            st.markdown(f"- {q}")
    st.markdown("---")

if app_mode == "📝 セッション実施 (Edit)":

    # === 0. Setup ===
    if menu == "0. 基本情報 (Setup)":
        st.title("📋 基本情報のセットアップ")
        col1, col2 = st.columns([2, 1])
        with col1:
            st.text_input("Client Name", key="name_input", value=st.session_state.data["name"], 
                        on_change=lambda: [st.session_state.data.update({"name": st.session_state.name_input}), auto_save()])
        with col2:
            st.text_input("Date", key="date_input", value=st.session_state.data["date"],
                        on_change=lambda: [st.session_state.data.update({"date": st.session_state.date_input}), auto_save()])
        
        st.divider()
        st.subheader("📍 仮ピン（現時点での目標・仮説）")
        st.text_area("Temporary Goal", key="temp_pin_input", value=st.session_state.data["temp_pin"], height=100, label_visibility="collapsed",
                     on_change=lambda: [st.session_state.data.update({"temp_pin": st.session_state.temp_pin_input}), auto_save()])

    # === 1. Bedrock ===
    elif menu == "1. 地盤調査 (Bedrock)":
        section_header("🪨 Phase 1: 地盤調査", "価値観や原動力を特定する。", ["無意識にできてしまうことは？", "絶対に許せないことは？"])
        st.text_area("✍️ 譲れない価値観", key="bedrock_input", value=st.session_state.data["bedrock"], height=200,
                    on_change=lambda: [st.session_state.data.update({"bedrock": st.session_state.bedrock_input}), auto_save()])
        st.text_area("📝 メモ", key="bedrock_note_input", value=st.session_state.data.get("bedrock_note", ""), height=100,
                    on_change=lambda: [st.session_state.data.update({"bedrock_note": st.session_state.bedrock_note_input}), auto_save()])

    # === 2. Sediment ===
    elif menu == "2. 堆積物確認 (Sediment)":
        section_header("🧱 Phase 2: 堆積物確認", "スキルやしがらみを棚卸しする。", ["今の肩書きは？", "もう使いたくないスキルは？"])
        st.text_area("✍️ スキル・肩書き", key="sediment_input", value=st.session_state.data["sediment"], height=200,
                    on_change=lambda: [st.session_state.data.update({"sediment": st.session_state.sediment_input}), auto_save()])

    # === 3. Topography ===
    elif menu == "3. 地形測量 (Topography)":
        section_header("🧗 Phase 3: 地形測量", "『崖』を『坂』に再定義する。", ["何が怖い？", "失敗したらどうなる？"])
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("😱 崖に見えているもの")
            st.text_area("Cliff", key="cliff_input", value=st.session_state.data["cliff"], label_visibility="collapsed", height=150, 
                        on_change=lambda: [st.session_state.data.update({"cliff": st.session_state.cliff_input}), auto_save()])
        with col2:
            st.subheader("🚶 登れる坂への再定義")
            st.text_area("Slope", key="slope_input", value=st.session_state.data["slope"], label_visibility="collapsed", height=150,
                        on_change=lambda: [st.session_state.data.update({"slope": st.session_state.slope_input}), auto_save()])

    # === 4. Routes ===
    elif menu == "4. 航路策定 (Routes)":
        section_header("🚩 Phase 4: 航路策定", "3ヶ月後の目的地を決める。", ["最低限どうなっていたい？", "明日何をする？"])
        st.text_area("🏁 3ヶ月後のゴール", key="goal_input", value=st.session_state.data["goal"], height=100,
                    on_change=lambda: [st.session_state.data.update({"goal": st.session_state.goal_input}), auto_save()])
        st.text_area("👟 Next Action", key="action_input", value=st.session_state.data["action"], height=100,
                    on_change=lambda: [st.session_state.data.update({"action": st.session_state.action_input}), auto_save()])

    # === 5. View (Export機能追加) ===
    elif menu == "5. クライアント出力 (View)":
        if not st.session_state.data["name"]:
            st.warning("名前を入力してください。")
        else:
            st.title(f"🗺️ {st.session_state.data['name']}'s Fieldwork Log")
            
            # --- Export Buttons ---
            col_dl1, col_dl2 = st.columns(2)
            
            # PDF Download
            with col_dl1:
                try:
                    pdf_bytes = generate_pdf(st.session_state.data)
                    st.download_button(
                        label="📄 PDFレポートをダウンロード",
                        data=pdf_bytes,
                        file_name=f"{st.session_state.data['name']}_LifeMap.pdf",
                        mime='application/pdf',
                        type="primary"
                    )
                except Exception as e:
                    st.error(f"PDF生成エラー: {e}")
                    st.caption("※フォルダに 'ipaexg.ttf' があるか確認してください。")

            # CSV Download
            with col_dl2:
                df = pd.DataFrame([st.session_state.data])
                csv = df.to_csv(index=False).encode('utf-8_sig')
                st.download_button(
                    label="📊 CSVデータをダウンロード",
                    data=csv,
                    file_name=f"{st.session_state.data['name']}_data.csv",
                    mime='text/csv'
                )
            
            st.markdown("---")

            # 表示ロジック
            st.markdown("""
            <style>
            .badge { background-color: #e3f2fd; color: #1565c0; padding: 5px 12px; border-radius: 15px; border: 1px solid #90caf9; margin: 4px; display: inline-block; font-weight: bold; }
            .core { background-color: #fff3e0; color: #ef6c00; border: 1px solid #ffcc80; }
            .flow-box { width: 90%; padding: 15px; border-radius: 8px; margin: 10px auto; box-shadow: 0 2px 5px rgba(0,0,0,0.05); font-family: 'Meiryo', sans-serif; background-color: #fff; }
            .box-title { font-size: 0.8em; color: #888; font-weight: bold; text-transform: uppercase; margin-bottom: 5px; }
            .box-content { font-size: 1.1em; font-weight: bold; color: #333; }
            .arrow { text-align: center; font-size: 20px; color: #ccc; margin: -5px 0; }
            .section-inventory { background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
            </style>
            """, unsafe_allow_html=True)

            st.subheader("🎒 Inventory")
            skills = st.session_state.data["sediment"].split('\n')
            values = st.session_state.data["bedrock"].split('\n')
            html = '<div class="section-inventory">'
            for v in values:
                if v.strip(): html += f'<span class="badge core">❤️ {v}</span>'
            for s in skills:
                if s.strip(): html += f'<span class="badge">💎 {s}</span>'
            html += "</div>"
            st.markdown(html, unsafe_allow_html=True)

            st.subheader("🧭 Adventure Map")
            col_map, col_quest = st.columns([3, 2])
            with col_map:
                slope = st.session_state.data["slope"] if st.session_state.data["slope"] else "???"
                action = st.session_state.data["action"] if st.session_state.data["action"] else "???"
                goal = st.session_state.data["goal"] if st.session_state.data["goal"] else "???"
                st.markdown(f"""
                <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px;">
                    <div class="flow-box" style="border-left: 5px solid #6c757d;">
                        <div class="box-title">📍 Current Location</div>
                        <div class="box-content">ぬるま湯の港 / 迷いの森</div>
                    </div>
                    <div class="arrow">⬇️</div>
                    <div class="flow-box" style="border-left: 5px solid #fbc02d;">
                        <div class="box-title">🚧 Quest</div>
                        <div class="box-content">{slope}</div>
                    </div>
                    <div class="arrow">⬇️</div>
                    <div class="flow-box" style="border-left: 5px solid #43a047;">
                        <div class="box-title">🏃 Next Action</div>
                        <div class="box-content">{action}</div>
                    </div>
                    <div class="arrow">⬇️</div>
                    <div class="flow-box" style="border-left: 5px solid #e53935;">
                        <div class="box-title">🏁 Destination</div>
                        <div class="box-content">{goal}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col_quest:
                st.info(f"**Main Quest:**\n\n{goal}")
                st.success(f"**Daily Mission:**\n\n{action}")

# ==========================================
# 3. Archives
# ==========================================
elif app_mode == "📂 過去ログ管理 (Archives)":
    st.title("📂 Session Archives")
    files = get_saved_files()
    if not files:
        st.info("データなし")
    else:
        all_records = []
        for f in files:
            path = os.path.join(DATA_DIR, f)
            try:
                with open(path, 'r', encoding='utf-8') as json_file:
                    d = json.load(json_file)
                    all_records.append(d)
            except:
                continue
        
        df = pd.DataFrame(all_records)
        display_cols = ["name", "date", "goal"]
        existing_cols = [c for c in display_cols if c in df.columns]
        st.dataframe(df[existing_cols], use_container_width=True)
        
        st.divider()
        st.subheader("🗑️ Delete")
        c1, c2 = st.columns([3, 1])
        with c1:
            file_to_delete = st.selectbox("削除ファイル", files)
        with c2:
            st.write("")
            st.write("")
            if st.button("❌ 削除"):
                delete_data(file_to_delete)
                st.rerun()