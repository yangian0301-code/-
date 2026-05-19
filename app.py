import streamlit as st
import random

# 設定頁面標題
st.set_page_config(page_title="今天吃什麼？🍔🍜", layout="centered")

# 初始化食物資料
if 'food_categories' not in st.session_state:
    st.session_state.food_categories = {
        "日式": ["壽司", "拉麵", "丼飯", "烏龍麵"],
        "中式": ["牛肉麵", "炒飯", "水餃", "滷肉飯"],
        "美式": ["漢堡", "炸雞", "披薩", "熱狗"],
        "韓式": ["韓式炸雞", "石鍋拌飯", "部隊鍋", "韓式烤肉"],
        "東南亞": ["泰式炒河粉", "海南雞飯", "越南河粉", "月亮蝦餅"]
    }

if 'result_message' not in st.session_state:
    st.session_state.result_message = ""

# ==============================
# 側邊欄分頁導覽
# ==============================
st.sidebar.title("🍔 導覽列")
page = st.sidebar.radio("請選擇頁面：", ["🎲 抽籤決定", "⚙️ 管理清單"])

# ==============================
# 頁面 1：抽籤決定（主頁面）
# ==============================
if page == "🎲 抽籤決定":
    st.title("🍔 今天吃什麼？ 🍜")
    
    # 這裡新增了姓名與學號資訊
    st.markdown("#### 👤 開發者：楊哲綸 ｜ 🆔 學號：B3232064")
    st.divider()  # 加一條分隔線讓視覺更乾淨

    st.header("🍕 幫我決定")

    options = ["全部隨機"] + list(st.session_state.food_categories.keys())
    selected_cat = st.selectbox("請選擇想吃的類型：", options)

    if st.button("幫我決定！", type="primary"):
        if selected_cat == "全部隨機":
            all_foods = [food for sublist in st.session_state.food_categories.values() for food in sublist]
            if all_foods:
                st.session_state.result_message = f"🎲 命運的安排：{random.choice(all_foods)}"
            else:
                st.session_state.result_message = "目前沒有食物可供選擇。"
        else:
            foods = st.session_state.food_categories.get(selected_cat, [])
            if foods:
                st.session_state.result_message = f"✨ {selected_cat}推薦：{random.choice(foods)}"
            else:
                st.session_state.result_message = f"{selected_cat} 分類中目前沒有食物。"

    if st.session_state.result_message:
        st.success(st.session_state.result_message)

# ==============================
# 頁面 2：管理清單
# ==============================
elif page == "⚙️ 管理清單":
    st.title("⚙️ 管理食物清單")
    
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("➕ 新增食物")
        with st.form("add_food_form", clear_on_submit=True):
            add_cat = st.selectbox("選擇欲新增的類型：", list(st.session_state.food_categories.keys()))
            new_food = st.text_input("輸入新食物名稱：")
            submit_add = st.form_submit_button("執行新增")

            if submit_add:
                if new_food.strip():
                    if new_food.strip() not in st.session_state.food_categories[add_cat]:
                        st.session_state.food_categories[add_cat].append(new_food.strip())
                        st.toast(f"已新增 {new_food.strip()} 至 {add_cat}")
                        st.rerun()
                    else:
                        st.warning("該食物已存在於清單中。")
                else:
                    st.error("請輸入名稱。")

    with col2:
        st.subheader("🗑️ 刪除食物")
        del_cat = st.selectbox("選擇欲刪除的類型：", list(st.session_state.food_categories.keys()), key="del_cat")
        foods_in_cat = st.session_state.food_categories.get(del_cat, [])
        food_to_del = st.selectbox("選擇要刪除的食物：", foods_in_cat if foods_in_cat else ["無食物可選"])
        
        if st.button("執行刪除"):
            if food_to_del != "無食物可選":
                st.session_state.food_categories[del_cat].remove(food_to_del)
                st.toast(f"已將 {food_to_del} 從 {del_cat} 移除")
                st.rerun()

    st.divider()

    # --- 顯示清單 ---
    st.subheader("📋 當前所有清單")
    for cat, items in st.session_state.food_categories.items():
        st.write(f"**{cat}**: {'、'.join(items) if items else '暫無食物'}")
