import sqlite3
import json

import streamlit as st
import pandas as pd
import numpy as np

pHs = [7.2, 6.8]

temperatures = [310, 307]
isHypoxics = [True, False]
isos = [0.0, 0.1]
all_g_Kr_multiplier_first = [1.0, 2.0, 4.0]
all_g_Kr_multiplier_last = [0.2, 0.4, 1.0]
all_g_Ks_multiplier_first = [1.0, 2.0, 4.0]
all_g_Ks_multiplier_last = [0.2, 0.4, 1.0]
all_PCa_multiplier_first = [1.0, 2.0, 4.0]
all_PCa_multiplier_last = [0.2, 0.4, 1.0]


def data2df(data):
    V = np.transpose(data["V"])
    ICaL = np.transpose(data["ICaL"])
    INa = np.transpose(data["INa"])
    INaL = np.transpose(data["INaL"])
    INaCa = np.transpose(data["INaCa"])
    t = np.array(data["t"])
    d = {"t": t}

    for i in range(20):
        d[f"V{i}"] = V[i]
        d[f"ICaL{i}"] = ICaL[i]
        d[f"INa{i}"] = INa[i]
        d[f"INaL{i}"] = INaL[i]
        d[f"INaCa{i}"] = INaCa[i]

    return pd.DataFrame(d)


def plot_data(data):
    st.header("Voltage")
    chart = st.line_chart(data, x="t", y=[f"V{i}" for i in range(20)])

    st.header("ICaL")
    chart = st.line_chart(data, x="t", y=[f"ICaL{i}" for i in range(20)])

    st.header("INa")
    chart = st.line_chart(data, x="t", y=[f"INa{i}" for i in range(20)])

    st.header("INaL")
    chart = st.line_chart(data, x="t", y=[f"INaL{i}" for i in range(20)])

    st.header("INaCa")
    chart = st.line_chart(data, x="t", y=[f"INaCa{i}" for i in range(20)])


def lqt1():
    con = sqlite3.connect("pvc.db")

    @st.cache_data
    def feth_data(
        g_Kr_multiplier_first,
        g_Kr_multiplier_last,
        PCa_multiplier_first,
        PCa_multiplier_last,
        isHypoxic,
        pH,
        temperature,
        iso,
    ):
        res = con.execute(
            "SELECT data FROM lqt1 WHERE g_Kr_multiplier_first = ? AND g_Kr_multiplier_last = ? AND PCa_multiplier_first = ? AND PCa_multiplier_last = ? AND isHypoxic = ? AND pH = ? AND temperature = ? AND iso = ?",
            (
                g_Kr_multiplier_first,
                g_Kr_multiplier_last,
                PCa_multiplier_first,
                PCa_multiplier_last,
                isHypoxic,
                pH,
                temperature,
                iso,
            ),
        )

        result = res.fetchall()
        if len(result) == 0:
            return None
        return json.loads(result[0][0])

    st.markdown("## LQT1 condition")
    st.sidebar.header("LQT1 condition")
    st.write(
        """The following show the results using a LQT1 condition 
        with 200 cells and g_Ks set to 0.0"""
    )

    # Create selectors for each variable that is possible to change
    g_Kr_multiplier_first = st.sidebar.selectbox(
        "g_Kr_multiplier_first", all_g_Kr_multiplier_first
    )
    g_Kr_multiplier_last = st.sidebar.selectbox(
        "g_Kr_multiplier_last", all_g_Kr_multiplier_last
    )
    PCa_multiplier_first = st.sidebar.selectbox(
        "PCa_multiplier_first", all_PCa_multiplier_first
    )
    PCa_multiplier_last = st.sidebar.selectbox(
        "PCa_multiplier_last", all_PCa_multiplier_last
    )
    isHypoxic = st.sidebar.selectbox("isHypoxic", isHypoxics)
    pH = st.sidebar.selectbox("pH", pHs)
    temperature = st.sidebar.selectbox("temperature", temperatures)
    iso = st.sidebar.selectbox("iso", isos)

    # Fetch data and plot with with matplotlib
    data = data2df(
        feth_data(
            g_Kr_multiplier_first,
            g_Kr_multiplier_last,
            PCa_multiplier_first,
            PCa_multiplier_last,
            isHypoxic,
            pH,
            temperature,
            iso,
        )
    )

    if data is not None:
        plot_data(data)


def lqt2():
    con = sqlite3.connect("pvc.db")

    @st.cache_data
    def feth_data(
        g_Ks_multiplier_first,
        g_Ks_multiplier_last,
        PCa_multiplier_first,
        PCa_multiplier_last,
        isHypoxic,
        pH,
        temperature,
        iso,
    ):
        res = con.execute(
            "SELECT data FROM lqt2 WHERE g_Ks_multiplier_first = ? AND g_Ks_multiplier_last = ? AND PCa_multiplier_first = ? AND PCa_multiplier_last = ? AND isHypoxic = ? AND pH = ? AND temperature = ? AND iso = ?",
            (
                g_Ks_multiplier_first,
                g_Ks_multiplier_last,
                PCa_multiplier_first,
                PCa_multiplier_last,
                isHypoxic,
                pH,
                temperature,
                iso,
            ),
        )

        result = res.fetchall()
        if len(result) == 0:
            st.error("No data found")
            return None
        return json.loads(result[0][0])

    st.markdown("## LQT2 condition")
    st.sidebar.header("LQT2 condition")
    st.write(
        """The following show the results using a LQT2 condition 
        with 200 cells and g_Kr set to 0.0"""
    )

    # Create selectors for each variable that is possible to change
    g_Ks_multiplier_first = st.sidebar.selectbox(
        "g_Ks_multiplier_first", all_g_Ks_multiplier_first
    )
    g_Ks_multiplier_last = st.sidebar.selectbox(
        "g_Ks_multiplier_last", all_g_Ks_multiplier_last
    )
    PCa_multiplier_first = st.sidebar.selectbox(
        "PCa_multiplier_first", all_PCa_multiplier_first
    )
    PCa_multiplier_last = st.sidebar.selectbox(
        "PCa_multiplier_last", all_PCa_multiplier_last
    )
    isHypoxic = st.sidebar.selectbox("isHypoxic", isHypoxics)
    pH = st.sidebar.selectbox("pH", pHs)
    temperature = st.sidebar.selectbox("temperature", temperatures)
    iso = st.sidebar.selectbox("iso", isos)

    # Fetch data and plot with with matplotlib
    data = data2df(
        feth_data(
            g_Ks_multiplier_first,
            g_Ks_multiplier_last,
            PCa_multiplier_first,
            PCa_multiplier_last,
            isHypoxic,
            pH,
            temperature,
            iso,
        )
    )

    if data is not None:
        plot_data(data)


st.set_page_config(page_title="PVC", page_icon="🫀")
st.sidebar.header("PVC")
lqt = st.sidebar.selectbox("LQT condition", ["LQT1", "LQT2"])
if lqt == "LQT1":
    lqt1()
else:
    lqt2()
