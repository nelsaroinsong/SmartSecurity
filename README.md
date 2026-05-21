# IoT Security Dashboard

Dashboard web sederhana untuk menerima notifikasi motion dari ESP32/PIR.

## 1) Install dependency

```powershell
cd D:\IoT
pip install -r requirements.txt
```

## 2) Jalankan server

```powershell
python server.py
```

Server berjalan di:
- `http://localhost:5000`
- Endpoint ESP32: `POST /api/motion`

## 3) Contoh payload dari ESP32

```json
{
  "device_id": "esp32-ruang-tamu",
  "motion": true
}
```

## 4) Update kode ESP32

Pastikan URL mengarah ke IP laptop/server yang menjalankan Flask:

```python
SERVER_URL = "http://192.168.1.100:5000/api/motion"
```

`192.168.1.100` ganti dengan IP lokal laptop kamu.

## 5) Cek cepat via curl (opsional)

```powershell
curl -Method POST http://localhost:5000/api/motion -ContentType "application/json" -Body '{"device_id":"esp32-ruang-tamu","motion":true}'
```

Lalu buka dashboard `http://localhost:5000`.

## 6) Deploy publik untuk Wokwi (Render)

Wokwi berjalan dari cloud, jadi paling stabil kirim event ke backend publik.

1. Push folder project ini ke GitHub.
2. Buka Render, pilih `New +` -> `Blueprint`.
3. Pilih repo yang berisi project ini (Render akan membaca `render.yaml`).
4. Tunggu deploy selesai, lalu ambil URL service, contoh:
   `https://iot-security-dashboard.onrender.com`
5. Pakai URL itu di ESP32:
   - Arduino:
     `POST /api/motion` ke host Render.
   - MicroPython:
     `SERVER_URL = "https://iot-security-dashboard.onrender.com/api/motion"`

Tes endpoint:
`https://iot-security-dashboard.onrender.com/health`
# SmartSecurity
