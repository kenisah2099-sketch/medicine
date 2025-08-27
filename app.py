import streamlit as st
import google.generativeai as genai
import os

# ==============================================================================
# PENGATURAN API KEY DAN MODEL (PENTING! UBAH SESUAI KEBUTUHAN ANDA)
# ==============================================================================

# GANTI INI DENGAN API KEY GEMINI ANDA!
# Untuk penggunaan pribadi, simpan API Key di file secrets.toml Streamlit.
# JANGAN BAGIKAN KODE INI DENGAN API KEY DI DALAMNYA KE PUBLIK.
# Atau Anda bisa mendapatkan API Key dari secrets.toml seperti ini:
# API_KEY = st.secrets["GEMINI_API_KEY"]
API_KEY = "AIzaSyB6-Qs5OOKzfc3pIedqUQO_E5VFgQoHxWA" # <--- GANTI BAGIAN INI!

# Nama model Gemini yang akan digunakan.
MODEL_NAME = 'gemini-1.5-flash'

# ==============================================================================
# KONTEKS AWAL CHATBOT
# ==============================================================================

# Definisikan peran chatbot Anda di sini.
INITIAL_CHATBOT_CONTEXT = [
    {
        "role": "user",
        "parts": ["Saya adalah seorang tenaga medis. Tuliskan penyakit yang perlu di diagnosis. Jawaban singkat dan jelas. Tolak pertanyaan selain tentang penyakit."]
    },
    {
        "role": "model",
        "parts": ["Baik! Tuliskan penyakit yang perlu di diagnosis."]
    }
]

# ==============================================================================
# APLIKASI STREAMLIT
# ==============================================================================

# Konfigurasi API Gemini
try:
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error(f"Kesalahan saat mengkonfigurasi API Key: {e}")
    st.stop()

# Inisialisasi model dan chat
model = genai.GenerativeModel(model_name=MODEL_NAME)
chat = model.start_chat(history=INITIAL_CHATBOT_CONTEXT)

# Pengaturan halaman Streamlit
st.set_page_config(
    page_title="Chatbot Penyakit",
    page_icon="�",
    layout="wide"
)

# Tampilan utama aplikasi
st.title("👨‍⚕️ Chatbot Diagnosis Penyakit")
st.markdown("Ini adalah chatbot khusus untuk mendiagnosis penyakit. Tanyakan tentang penyakit yang ingin Anda ketahui.")

# Inisialisasi riwayat chat di Streamlit session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan pesan dari riwayat chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kolom input untuk pengguna
if prompt := st.chat_input("Tulis pertanyaan Anda di sini..."):
    # Tambahkan pesan pengguna ke riwayat chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Kirim pesan pengguna ke model Gemini dan tampilkan responsnya
    with st.chat_message("model"):
        # Tampilkan respons secara bertahap (streaming)
        with st.spinner("Memproses..."):
            response = chat.send_message(prompt, stream=True)
            full_response = ""
            message_placeholder = st.empty()
            for chunk in response:
                full_response += chunk.text
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
    
    # Tambahkan respons model ke riwayat chat
    st.session_state.messages.append({"role": "model", "content": full_response})

�
