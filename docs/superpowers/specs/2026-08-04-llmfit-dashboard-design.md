# Rekaan Sistem: llmfit Universal LLM Dashboard

**Tarikh:** 2026-08-04
**Topik:** Integrasi Papan Pemuka Ejen & API Cloud ke dalam `llmfit` (Opsyen B - Plugin-Driven)

## 1. Ringkasan & Objektif
Evolusi `llmfit` daripada sekadar alat penyemak kapasiti memori VRAM kepada "Terminal Perintah Berpusat (Centralized Command Center)". TUI ini akan berfungsi sebagai payung paparan (*dashboard*) utama untuk:
- Memantau status semasa Ejen CLI tempatan (Kimi Code, Agy, OpenCode, Codex).
- Memaparkan kuota baki untuk akaun-akaun API (jika disokong oleh penyedia).
- Menjalankan penanda aras masa-nyata (*live benchmark*) untuk kependaman (ping/latency) dan kelajuan *Token/s* bagi penyedia Cloud (OpenCode, Ollama Cloud, Antigravity, OpenCode Zen, ChatGPT, Nvidia Nim).

## 2. Senibina Sistem (Plugin-Driven Architecture)

Bagi mengekalkan teras Rust `llmfit` supaya sentiasa pantas dan selamat daripada kerosakan (akibat perubahan API luaran), sistem direka berasaskan dua komponen terpisah:

### A. Teras TUI Rust (`llmfit-tui`)
Aplikasi terminal Rust tidak akan mempunyai kod rahsia API yang "di-hardcode". Ia akan bertindak sebagai klien visual.
1.  **Tab Baharu:** UI akan ditambah dengan Menu navigasi (contoh: kekunci F1-F4):
    - `[F1] Local Fit` (Fungsi Asal VRAM)
    - `[F2] Agents` (Status Ejen)
    - `[F3] Quotas` (Baki Akaun)
    - `[F4] Cloud Bench` (Kelajuan Cloud)
2.  **Klien Data:** `llmfit-tui` akan membaca data dari satu fail log JSON tempatan atau memanggil REST API tempatan secara *async* (contoh: `http://localhost:9421/api/stats` atau membaca dari paip soket `mcp_server`).

### B. Enjin Pengumpul Data / Aggregator (Python/Node.js Plugin)
Satu skrip pelayan kecil (*Aggregator*) berjalan di latar belakang (mungkin diintegrasikan ke dalam ekosistem Kimi Proxy/WebBridge sedia ada).
1.  **Pengesan Ejen (Process Scanner):** Menggunakan utiliti OS (seperti OS `ps` / WMI) untuk mengesan kelangsungan proses (PID) ejen `agy`, `kimicode`, dll.
2.  **Pemantau Kuota:** Memanggil *endpoint* bil API (contoh: `/dashboard/billing/credit_grants` bagi OpenAI) menggunakan senarai kunci (*keys pool*) tempatan.
3.  **Benchmarker (Ping & Token):** Menghantar isyarat *ping* kecil berkala dan *prompt* panas ke hujung titik (endpoints) cloud untuk mengukur sela masa jawapan (Time-to-First-Token).

## 3. Aliran Data (Data Flow)

1.  **Mula:** Skrip *Aggregator* (Python) berjalan di latar (daemon). Ia merekodkan dan mengemas kini data metrik ke memori/fail cache setiap 60 saat.
2.  **TUI Dimulakan:** Pengguna menaip `llmfit` di CLI.
3.  **Navigasi:** Apabila pengguna menekan `[F2]`, kod UI Ratatui menghantar *GET request* ke *Aggregator*.
4.  **Paparan:** Rust menghuraikan (*parse*) JSON yang dipulangkan dan merender tabel/graf berkelip (*pulsing*) dengan pantas.

## 4. Pengendalian Ralat (Error Handling)
- Jika Skrip *Aggregator* tidak dijumpai atau dimatikan, tab Dashboard di dalam Rust `llmfit` akan memaparkan mesej `[Aggregator Offline - Tekan 'R' untuk spawn daemon]`. UI tidak akan *crash*.
- Jika satu API penyedia mencapai *Rate Limit* (429), ia akan memaparkan `[RATE LIMITED]` berwarna merah pada sel TUI berkaitan, tanpa menjejaskan ping penyedia lain.

## 5. Pelan Pengujian
- **Ujian Semantik:** Jalankan `cargo run` pada `llmfit-tui` untuk menguji paparan *Bento-box* TUI (tidak terpotong).
- **Ujian Mock:** Membina *mock server* ringkas yang memberikan data JSON palsu kepada Rust untuk mengesahkan penyusunan tabel/graf berjalan dengan betul di Terminal.

---
*(Dokumen Spesifikasi Selesai - Sedia untuk Pelaksanaan)*
