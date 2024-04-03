import streamlit as st
import pandas as pd
import statsmodels.api as sm

# タイトル
st.title('目指せ300ヤード!（飛距離予測）')

# CSVファイルのアップロード
uploaded_file = st.file_uploader("CSVファイルをこの下の欄にアップロードしてください", type=['csv'])
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write(data)  # アップロードされたデータを表示

    # 説明変数と目的変数の設定
    X = data[['Height (cm)', 'Weight (kg)', 'Launch Angle (degrees)', 'Ball Spin (rpm)', 'Club Head Speed (m/s)']]  # 説明変数
    Y = data['Driver Distance (yards)']  # 目的変数
    X = sm.add_constant(X)  # 定数項（バイアス）を追加

    # モデルの構築とフィッティング
    model = sm.OLS(Y, X).fit()



    # 推論用の入力フォームをサイドバーに作成
    st.sidebar.header("あなたの情報を教えて!")
    input_A = st.sidebar.slider("Height (cm)", min_value=140, max_value=210, value=175, step=1)
    input_B = st.sidebar.slider("Weight (kg)", min_value=50, max_value=120, value=75, step=1)
    input_C = st.sidebar.slider("Launch Angle (degrees)", min_value=0, max_value=20, value=10, step=1)
    input_D = st.sidebar.slider("Ball Spin (rpm)", min_value=2000, max_value=6000, value=4000, step=100)
    input_F = st.sidebar.slider("Club Head Speed (m/s)", min_value=10, max_value=60, value=35, step=1)

    # 推論ボタン
    if st.sidebar.button("予測する!"):
        new_data = pd.DataFrame({
            'const': 1,  # 定数項
            'Height (cm)': [input_A],
            'Weight (kg)': [input_B],
            'Launch Angle (degrees)': [input_C],
            'Ball Spin (rpm)': [input_D],
            'Club Head Speed (m/s)': [input_F]
        })
        # 推論実行
        prediction = model.predict(new_data)


        # 推論結果の表示
        predicted_distance = prediction[0]
        if predicted_distance >= 300:
            message = "すでにあなたはローリー・マキロイ！"
            color = "green"
        else:
            message = "let's トレーニング！"
            color = "blue"
        
        st.markdown(f"<h1 style='text-align: center; color: {color};'>あなたのドライバーの飛距離は: {predicted_distance:.2f} yards</h1>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align: center; color: {color};'>{message}</h2>", unsafe_allow_html=True)