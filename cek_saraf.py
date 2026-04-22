from groq import Groq

# Masukin API Key lo di sini
client = Groq(api_key="")

try:
    models = client.models.list()
    print("--- DAFTAR MODEL YANG HALAL & AKTIF SEKARANG ---")
    for model in models.data:
        # Kita filter yang ada tulisan 'vision' nya aja biar gak pusing
        if "vision" in model.id.lower():
            print(f"✅ VISION: {model.id}")
        else:
            print(f"🔹 TEXT:   {model.id}")
except Exception as e:
    print(f"Gagal konek: {e}")