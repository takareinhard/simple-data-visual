import streamlit as st
import pandas as pd
import plotly.express as px

# --- Streamlit App Configuration ---
st.set_page_config(
    page_title="シンプルなデータ可視化ツール",
    page_icon="📊",
    layout="wide"
)

# --- Sidebar for File Upload and Options ---
with st.sidebar:
    st.header("設定")
    uploaded_file = st.file_uploader("CSVファイルをアップロードしてください", type=["csv"])

# --- Main App Logic ---
st.title("📊 シンプルなデータ可視化ツール")
st.write("サイドバーからCSVファイルをアップロードして開始します。")

if uploaded_file is not None:
    try:
        # Read the uploaded CSV file
        df = pd.read_csv(uploaded_file)

        st.header("データプレビュー")
        st.dataframe(df.head())

        st.header("データを可視化")

        # Get column names for user selection
        numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
        categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()

        # Allow user to select columns for plotting
        x_axis = st.selectbox("X軸を選択 (カテゴリ別)", categorical_columns)
        y_axis = st.selectbox("Y軸を選択 (数値)", numeric_columns)
        
        chart_type = st.selectbox("グラフの種類を選択", ["棒グラフ", "折れ線グラフ", "円グラフ"])

        if st.button("グラフを作成"):
            if x_axis and y_axis:
                st.subheader(f"{x_axis}別{y_axis}の{chart_type}")
                
                # Generate the selected chart type
                if chart_type == "棒グラフ":
                    fig = px.bar(df, x=x_axis, y=y_axis, title=f"{x_axis}別{y_axis}", color=x_axis)
                elif chart_type == "折れ線グラフ":
                    # For line charts, it's often better to aggregate data if x-axis has duplicates
                    df_agg = df.groupby(x_axis)[y_axis].sum().reset_index()
                    fig = px.line(df_agg, x=x_axis, y=y_axis, title=f"{x_axis}別{y_axis}")
                elif chart_type == "円グラフ":
                    fig = px.pie(df, names=x_axis, values=y_axis, title=f"{x_axis}別{y_axis}の分布")
                
                # Display the chart
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("X軸とY軸の両方を選択してください。")

    except Exception as e:
        st.error(f"エラーが発生しました: {e}")

else:
    # Display a sample chart if no file is uploaded
    st.info("CSVファイルのアップロードを待っています。提供された`sample_data.csv`を使用したサンプルグラフを表示します。")
    try:
        sample_df = pd.read_csv("sample_data.csv")
        st.dataframe(sample_df.head())
        fig = px.bar(sample_df, x="category", y="sales", color="category", title="カテゴリ別のサンプル売上データ")
        st.plotly_chart(fig, use_container_width=True)
    except FileNotFoundError:
        st.error("`sample_data.csv`が見つかりません。ファイルをアップロードしてください。")
