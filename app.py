import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import pandas as pd

# Title
st.title("FIR Filter Design Web App ")

# Description (NEW - for better presentation)
st.write("This app designs FIR filters and shows frequency & impulse responses with coefficient export. It also provides fixed-point coefficients for hardware implementation.")

# Inputs
fs = st.number_input("Sampling Frequency (Hz)", value=1000)
fc = st.number_input("Cutoff Frequency 1 (Hz)", value=100)
order = st.slider("Filter Order", 1, 100, 50)

# Filter type
filter_type = st.selectbox(
    "Select Filter Type",
    ["Lowpass", "Highpass", "Bandpass"]
)

# Bandpass second cutoff
if filter_type == "Bandpass":
    fc2 = st.number_input("Cutoff Frequency 2 (Hz)", value=200)

# Button
if st.button("Design Filter"):

    wn = fc / (fs/2)

    # Filter design
    if filter_type == "Lowpass":
        b = signal.firwin(order, wn)

    elif filter_type == "Highpass":
        b = signal.firwin(order, wn, pass_zero=False)

    elif filter_type == "Bandpass":
        wn2 = fc2 / (fs/2)
        b = signal.firwin(order, [wn, wn2], pass_zero=False)

    # ==============================
    # COEFFICIENTS
    # ==============================
    st.subheader("Filter Coefficients")
    st.write(b)

    # ==============================
    # FREQUENCY RESPONSE
    # ==============================
    w, h = signal.freqz(b)

    fig, ax = plt.subplots()
    ax.plot(w, abs(h), label="Magnitude Response")  # improved
    ax.set_title("Frequency Response")
    ax.set_xlabel("Frequency")
    ax.set_ylabel("Magnitude")
    ax.legend()

    st.pyplot(fig)

    # ==============================
    # IMPULSE RESPONSE
    # ==============================
    st.subheader("Impulse Response")

    fig2, ax2 = plt.subplots()
    ax2.stem(b)
    ax2.set_title("Impulse Response")

    st.pyplot(fig2)

    # ==============================
    # FIXED POINT (Q15)
    # ==============================
    b_fixed = np.round(b * 32768).astype(int)

    st.subheader("Fixed Point Coefficients (Q15)")
    st.write(b_fixed)

    # ==============================
    # SAVE FILE
    # ==============================
    np.savetxt("coeff.txt", b)
    st.success("Coefficients saved as coeff.txt")

    # ==============================
    # DOWNLOAD BUTTON
    # ==============================
    df = pd.DataFrame(b)

    st.download_button(
        label="Download Coefficients",
        data=df.to_csv(index=False),
        file_name="coefficients.csv",
        mime="text/csv"
    )