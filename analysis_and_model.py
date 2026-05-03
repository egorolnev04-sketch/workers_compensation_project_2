import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, Ridge
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def load_and_preprocess():
    data = fetch_openml(data_id=42876, as_frame=True, parser='auto')
    df = data.frame

    df['DateTimeOfAccident'] = pd.to_datetime(df['DateTimeOfAccident'])
    df['DateReported'] = pd.to_datetime(df['DateReported'])
    df['AccidentMonth'] = df['DateTimeOfAccident'].dt.month
    df['AccidentDayOfWeek'] = df['DateTimeOfAccident'].dt.dayofweek
    df['ReportingDelay'] = (df['DateReported'] - df['DateTimeOfAccident']).dt.days
    df = df.drop(columns=['DateTimeOfAccident', 'DateReported'])

    categorical_cols = ['Gender', 'MaritalStatus', 'PartTimeFullTime', 'ClaimDescription']
    for col in categorical_cols:
        df[col] = LabelEncoder().fit_transform(df[col])

    return df

def analysis_and_model_page():
    st.title("Прогнозирование стоимости страховых выплат")

    if 'df' not in st.session_state:
        st.session_state.df = None
    if 'model' not in st.session_state:
        st.session_state.model = None
    if 'scaler' not in st.session_state:
        st.session_state.scaler = None
    if 'feature_names' not in st.session_state:
        st.session_state.feature_names = None

    if st.button("Загрузить данные"):
        with st.spinner("Загрузка данных..."):
            st.session_state.df = load_and_preprocess()
        st.success("Данные загружены!")

    if st.session_state.df is not None:
        df = st.session_state.df
        st.subheader("Просмотр данных")
        st.write(df.head())
        st.subheader("Статистика")
        st.write(df.describe())

        if st.button("Обучить модели"):
            with st.spinner("Обучение..."):
                X = df.drop(columns=['UltimateIncurredClaimCost'])
                y = df['UltimateIncurredClaimCost']

                numerical_features = ['Age', 'DependentChildren', 'DependentsOther', 'WeeklyPay',
                                       'HoursWorkedPerWeek', 'DaysWorkedPerWeek', 'InitialCaseEstimate',
                                       'AccidentMonth', 'AccidentDayOfWeek', 'ReportingDelay']

                scaler = StandardScaler()
                X[numerical_features] = scaler.fit_transform(X[numerical_features])

                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

                models = {
                    "Linear Regression": LinearRegression(),
                    "Ridge Regression": Ridge(alpha=1.0, random_state=42),
                    "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
                    "XGBoost": XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
                }

                results = []
                for name, model in models.items():
                    model.fit(X_train, y_train)
                    y_pred = model.predict(X_test)
                    mae = mean_absolute_error(y_test, y_pred)
                    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
                    r2 = r2_score(y_test, y_pred)
                    results.append({"Модель": name, "MAE": f"${mae:.2f}", "RMSE": f"${rmse:.2f}", "R²": f"{r2:.4f}"})
                    if name == "Random Forest":
                        st.session_state.model = model
                        st.session_state.scaler = scaler
                        st.session_state.feature_names = list(X.columns)

                st.subheader("Результаты моделей")
                st.dataframe(pd.DataFrame(results))

                if st.session_state.model is not None:
                    importance = pd.DataFrame({
                        'Признак': st.session_state.feature_names,
                        'Важность': st.session_state.model.feature_importances_
                    }).sort_values('Важность', ascending=False).head(10)

                    fig, ax = plt.subplots(figsize=(10, 6))
                    ax.barh(importance['Признак'], importance['Важность'])
                    ax.set_xlabel('Важность')
                    ax.set_title('Топ-10 важных признаков')
                    ax.invert_yaxis()
                    st.pyplot(fig)

        st.header("Предсказание стоимости возмещения")
        with st.form("prediction_form"):
            col1, col2 = st.columns(2)
            with col1:
                age = st.number_input("Возраст", 13, 76, 35)
                gender = st.selectbox("Пол", ["M", "F"])
                marital = st.selectbox("Семейное положение", ["Single", "Married", "Divorced", "Widowed"])
                dependents_children = st.number_input("Детей на иждивении", 0, 10, 0)
                dependents_other = st.number_input("Других иждивенцев", 0, 10, 0)
            with col2:
                weekly_pay = st.number_input("Еженедельная зарплата ($)", 0, 10000, 500)
                part_time_full = st.selectbox("Занятость", ["Full Time", "Part Time"])
                hours_per_week = st.number_input("Часов работы в неделю", 0, 80, 40)
                days_per_week = st.number_input("Дней работы в неделю", 0, 7, 5)
                initial_estimate = st.number_input("Начальная оценка ($)", 0, 500000, 5000)

            claim_description = st.selectbox("Тип травмы", ["back injury", "hand injury", "leg injury", "other", "shoulder injury"])
            submitted = st.form_submit_button("Предсказать")

            if submitted:
                if st.session_state.model is None:
                    st.warning("Сначала обучите модель!")
                else:
                    gender_map = {"M": 0, "F": 1}
                    marital_map = {"Single": 0, "Married": 1, "Divorced": 2, "Widowed": 3}
                    part_time_map = {"Full Time": 0, "Part Time": 1}
                    claim_map = {
                        "back injury": 0,
                        "hand injury": 1,
                        "leg injury": 2,
                        "other": 3,
                        "shoulder injury": 4,
                    }

                    input_dict = {col: 0 for col in st.session_state.feature_names}
                    
                    input_dict['Age'] = age
                    input_dict['DependentChildren'] = dependents_children
                    input_dict['DependentsOther'] = dependents_other
                    input_dict['WeeklyPay'] = weekly_pay
                    input_dict['HoursWorkedPerWeek'] = hours_per_week
                    input_dict['DaysWorkedPerWeek'] = days_per_week
                    input_dict['InitialCaseEstimate'] = initial_estimate
                    input_dict['AccidentMonth'] = 1
                    input_dict['AccidentDayOfWeek'] = 1
                    input_dict['ReportingDelay'] = 0
                    input_dict['Gender'] = gender_map[gender]
                    input_dict['MaritalStatus'] = marital_map[marital]
                    input_dict['PartTimeFullTime'] = part_time_map[part_time_full]
                    input_dict['ClaimDescription'] = claim_map[claim_description]

                    input_df = pd.DataFrame([input_dict])

                    numerical_features = ['Age', 'DependentChildren', 'DependentsOther', 'WeeklyPay',
                                           'HoursWorkedPerWeek', 'DaysWorkedPerWeek', 'InitialCaseEstimate',
                                           'AccidentMonth', 'AccidentDayOfWeek', 'ReportingDelay']
                    
                    input_df[numerical_features] = st.session_state.scaler.transform(input_df[numerical_features])

                    prediction = st.session_state.model.predict(input_df)[0]
                    st.success(f" Прогнозируемая стоимость: ${prediction:,.2f}")

if __name__ == "__main__":
    analysis_and_model_page()