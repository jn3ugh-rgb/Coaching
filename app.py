import streamlit as st
from datetime import datetime

# ---------------------------------------------------------
# 1. セッション状態の初期化 (データ保持のため)
# ---------------------------------------------------------
# 初回起動時に、データを格納する"箱"を作る
if "form_data" not in st.session_state:
    st.session_state.form_data = {
        "client_name": "",
        "date": datetime.now().strftime("%Y-%m-%d"),
        # 地盤
        "bedrock_values": "",
        "bedrock_notes": "",
        # 堆積物
        "sediment_status": "",
        "sediment_notes": "",
        # 地形
        "topo_cliff": "",
        "topo_slope": "",
        "topo_notes": "",
        # 航路
        "route_goal": "",
        "route_action": "",
        "route_notes": "",
        # 全体総評
        "summary": ""
    }

# ---------------------------------------------------------
# 2. サイドバー設定
# ---------------------------------------------------------
st.sidebar.title("🧭 Life Mapping Console")
st.sidebar.markdown("---")

# メニュー選択
menu = st.sidebar.radio(
    "フェーズ選択",
    ["0. 基本情報", "1. 地盤調査 (Bedrock)", "2. 堆積物確認 (Sediment)", "3. 地形測量 (Topography)", "4. 航路策定 (Routes)", "5. アウトプット生成"]
)

# カンペ：4タイプ診断（いつでも見れるように）
with st.sidebar.expander("🔍 4タイプ診断リファレンス"):
    st.markdown("""
    **① 白地図タイプ**
    * 未来が見えない / 過去を掘る
    **② 遭難中タイプ**
    * ゴールはあるが動けない / 重りを外す
    **③ 現状埋没タイプ**
    * 忙殺・思考停止 / 延長線の先を見せる
    **④ 登山口タイプ**
    * 恐怖で一歩が出ない / 崖を坂にする
    """)

# ---------------------------------------------------------
# 3. メイン画面ロジック
# ---------------------------------------------------------

def section_header(title, purpose, questions):
    """共通ヘッダー表示関数"""
    st.title(title)
    st.info(f"**【目的】** {purpose}")
    with st.expander("🗣️ 参謀の問い（スクリプト）", expanded=True):
        for q in questions:
            st.write(f"- {q}")
    st.markdown("---")

# === 0. 基本情報 ===
if menu == "0. 基本情報":
    st.title("📋 クライアント基本情報")
    st.write("セッションを始める前に、基本情報をセットアップします。")
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.form_data["client_name"] = st.text_input(
            "クライアント氏名", 
            value=st.session_state.form_data["client_name"]
        )
    with col2:
        st.session_state.form_data["date"] = st.text_input(
            "実施日", 
            value=st.session_state.form_data["date"]
        )
    
    st.success("セットアップ完了。左のメニューからフェーズ1へ進んでください。")

# === 1. 地盤調査 ===
elif menu == "1. 地盤調査 (Bedrock)":
    section_header(
        "🪨 Phase 1: 地盤調査 (Bedrock)",
        "表面的な悩みの下にある、決して変わらない『価値観』や『源泉』を特定する。",
        [
            "今の仕事で『無意識にできてしまう（ストレスがない）』瞬間は？",
            "逆に、『これだけは絶対にやりたくない』『許せない』ことは？",
            "過去に一番『自分最強』と感じたエピソードは？",
            "その『やりたい』は、純粋なワクワク？ それとも焦り？"
        ]
    )
    
    st.session_state.form_data["bedrock_values"] = st.text_area(
        "✍️ 地盤・価値観 (Core Beliefs)",
        value=st.session_state.form_data["bedrock_values"],
        height=150,
        placeholder="例：構造化することへの執着、自由であること、嘘をつかないこと..."
    )
    st.session_state.form_data["bedrock_notes"] = st.text_area(
        "📝 特記事項・メモ",
        value=st.session_state.form_data["bedrock_notes"],
        height=100
    )

# === 2. 堆積物確認 ===
elif menu == "2. 堆積物確認 (Sediment)":
    section_header(
        "🧱 Phase 2: 堆積物確認 (Sediment)",
        "現在地を形成している『スキル』『経験』『しがらみ』を棚卸しする。",
        [
            "今の肩書きや役割を、一度すべて書き出してみましょう。",
            "持っているけれど『もう使いたくないスキル』はありますか？",
            "逆に、もっと磨きたい『武器』はどれですか？",
            "足首を掴んでいる『ツタ（しがらみ）』の正体は何ですか？"
        ]
    )
    
    st.session_state.form_data["sediment_status"] = st.text_area(
        "✍️ 堆積物・現状 (Current Status)",
        value=st.session_state.form_data["sediment_status"],
        height=150,
        placeholder="例：マネジメント経験、医療業界の知識、XXの資格... / でも実はXXには飽きている"
    )
    st.session_state.form_data["sediment_notes"] = st.text_area(
        "📝 特記事項・メモ",
        value=st.session_state.form_data["sediment_notes"],
        height=100
    )

# === 3. 地形測量 ===
elif menu == "3. 地形測量 (Topography)":
    section_header(
        "🧗 Phase 3: 地形測量 (Topography)",
        "クライアントが『崖（不可能）』と感じているものを、『坂（タスク）』に再定義する。",
        [
            "その一歩目が『怖い』のは、具体的に何が起きると思っているから？",
            "それは『能力的に登れない崖』？ それとも『装備があれば登れる急斜面』？",
            "最悪のケース、失敗したらどうなりますか？（元の場所に戻るだけでは？）"
        ]
    )
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.form_data["topo_cliff"] = st.text_area(
            "😱 崖に見えているもの (Fear)",
            value=st.session_state.form_data["topo_cliff"],
            placeholder="例：独立したら収入がゼロになる恐怖、批判される恐怖"
        )
    with col2:
        st.session_state.form_data["topo_slope"] = st.text_area(
            "🚶 登れる坂への再定義 (Task)",
            value=st.session_state.form_data["topo_slope"],
            placeholder="例：まずは副業で月5万稼ぐ、批判は『認知された証拠』と捉える"
        )
        
    st.session_state.form_data["topo_notes"] = st.text_area(
        "📝 特記事項・メモ",
        value=st.session_state.form_data["topo_notes"],
        height=100
    )

# === 4. 航路策定 ===
elif menu == "4. 航路策定 (Routes)":
    section_header(
        "🚩 Phase 4: 航路策定 (Routes)",
        "3ヶ月後の『目的地』と、明日踏み出す『最初の一歩』を決める。",
        [
            "3ヶ月後、最低限『これだけは変わっていたい』という景色は？",
            "そのために、明日スマホで最初に何を検索しますか？",
            "誰に連絡しますか？"
        ]
    )
    
    st.session_state.form_data["route_goal"] = st.text_area(
        "🏁 3ヶ月後のゴール (Destination)",
        value=st.session_state.form_data["route_goal"],
        placeholder="例：サービスをローンチして最初の1円を稼ぐ"
    )
    st.session_state.form_data["route_action"] = st.text_area(
        "👟 Next Action (Baby Step)",
        value=st.session_state.form_data["route_action"],
        placeholder="例：明日10時にXXさんにアポのLINEを送る"
    )
    st.session_state.form_data["route_notes"] = st.text_area(
        "📝 特記事項・メモ",
        value=st.session_state.form_data["route_notes"],
        height=100
    )

# === 5. アウトプット生成 ===
elif menu == "5. アウトプット生成":
    st.title("📄 Strategy Map 生成")
    st.write("入力内容をまとめ、ドキュメントとして出力します。")
    
    # 最後の総評欄
    st.session_state.form_data["summary"] = st.text_area(
        "💬 参謀からのメッセージ (Feedback)",
        value=st.session_state.form_data["summary"],
        height=100,
        placeholder="例：あなたは遭難していません。ただ装備が重すぎただけです。この地図を持って進みましょう。"
    )
    
    # テキストデータの整形
    output_text = f"""
================================================
Life Mapping Strategy Report
================================================
■ Client: {st.session_state.form_data['client_name']} 様
■ Date  : {st.session_state.form_data['date']}
■ Strategist: Nozomi Yoneyama

------------------------------------------------
1. BEDROCK (地盤・価値観)
------------------------------------------------
{st.session_state.form_data['bedrock_values']}

[Memo]
{st.session_state.form_data['bedrock_notes']}

------------------------------------------------
2. SEDIMENT (堆積物・現状)
------------------------------------------------
{st.session_state.form_data['sediment_status']}

[Memo]
{st.session_state.form_data['sediment_notes']}

------------------------------------------------
3. TOPOGRAPHY (地形の再定義)
------------------------------------------------
▼ 崖（恐怖の正体）:
{st.session_state.form_data['topo_cliff']}

▼ 坂（具体的タスク）:
{st.session_state.form_data['topo_slope']}

[Memo]
{st.session_state.form_data['topo_notes']}

------------------------------------------------
4. ROUTES (航路・戦略)
------------------------------------------------
🏁 3ヶ月後のゴール:
{st.session_state.form_data['route_goal']}

👟 Next Action (明日やること):
{st.session_state.form_data['route_action']}

------------------------------------------------
★ 参謀からのメッセージ
------------------------------------------------
{st.session_state.form_data['summary']}

================================================
"""
    
    # プレビュー表示
    st.text_area("プレビュー", value=output_text, height=400)
    
    # ダウンロードボタン
    filename = f"StrategyMap_{st.session_state.form_data['client_name']}_{st.session_state.form_data['date']}.txt"
    st.download_button(
        label="📥 マップをダウンロード (Text)",
        data=output_text,
        file_name=filename,
        mime="text/plain"
    )