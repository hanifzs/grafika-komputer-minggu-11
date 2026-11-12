# 3D Visual Realism Suite — Grafika Komputer Minggu 11

Proyek mandiri Java 17 + LWJGL 3 + JOML + OpenGL 3.3 core. Scene berisi sphere UV bermaterial serta lantai bertekstur, dengan lampu bergerak dan bayangan real-time. Dibuat sebagai proyek mandiri karena proyek Minggu 10 tidak tersedia di folder kerja.

## Menjalankan

**Windows:** pasang JDK 17+ dan driver grafis yang mendukung OpenGL 3.3. Di PowerShell, dari folder proyek jalankan `./run.ps1` (atau `powershell -ExecutionPolicy Bypass -File ./run.ps1` jika kebijakan PowerShell membatasi skrip). Skrip menggunakan Maven yang sudah ada; jika belum terpasang, Maven 3.9.11 diunduh saat pertama kali. Akses internet diperlukan untuk dependensi pertama kali.

**Linux/macOS:** dengan Maven tersedia, jalankan `mvn compile exec:java` (natives macOS ARM mungkin perlu mengganti classifier menjadi `natives-macos-arm64` di `pom.xml`). Jalankan dari komputer dengan desktop dan GPU, bukan terminal headless.

## Kontrol dan demonstrasi

| Tombol | Fungsi | Pengujian |
|---|---|---|
| B | Phong ↔ Blinn-Phong | Bandingkan specular highlight saat cahaya berputar. |
| F | Flat ↔ Smooth | Perhatikan sisi sphere menjadi bersudut/halus. |
| Z | Depth test on/off | Saat off, urutan gambar bisa menyebabkan occlusion salah. |
| C | Back-face culling on/off | Aktifkan lalu orbit kamera untuk memeriksa arah winding. |
| T | Tekstur on/off | Bandingkan material UV dan warna polos. |
| M | Nearest ↔ bilinear + trilinear mipmap | Dekatkan kamera dan amati tepi texel/aliasing. |
| L | Bayangan on/off | Amati bayangan sphere yang bergerak pada lantai. |
| Panah, + / - | Orbit dan zoom kamera | Ambil sudut pandang pengujian. |
| Esc | Tutup aplikasi | — |

FPS dan status kontrol tampil pada judul jendela (diperbarui tiap satu detik). Tekstur PNG dalam `src/main/resources/textures/` dibaca dari classpath melalui STBImage.

**Uji otomatis singkat:** `./run.ps1 --smoke` (atau `mvn compile exec:java -Dexec.args=--smoke`) menjalankan dua frame tersembunyi, memeriksa error OpenGL, dan mencoba semua toggle. Template laporan tersedia sebagai `Laporan_Praktikum_Minggu11.docx`; jika mengubah `LAPORAN.md`, pasang `python-docx` lalu jalankan `python buat_laporan.py` untuk memperbaruinya.

## Struktur

- `VisualRealismApp.java`: siklus GLFW, kontrol, kamera, animasi lampu, dua rendering pass.
- `Mesh.java`: VAO/VBO, sphere UV; normal halus diakumulasi berbobot luas dari face yang berbagi vertex, normal flat per-face.
- `ShaderProgram.java`: kompilasi/link GLSL dan pengiriman uniform.
- `Texture2D.java`: load PNG via STB, flip V, filtering, mipmapping.
- `HSRManager.java`: depth test `GL_LESS` dan culling CCW/back.
- `ShadowMapFBO.java`: depth texture 2048², validasi FBO, pengelolaan viewport.
- `shaders/phong.*`: Phong/Blinn per-fragment, UV, PCF 3×3, slope-dependent bias.
- `shaders/depth.*`: pass kedalaman dari sudut pandang lampu.

Catatan: Proyeksi lampu ortografik dipakai untuk efek directional-light, sementara intensitas diffuse/specular dihitung dari posisi lampu animasi; pendekatan ini demonstratif, bukan model fisik PBR. Depth test tetap diaktifkan pada pass bayangan bahkan ketika `Z` off, agar toggle hanya menguji HSR tampilan kamera. Normal sudut seam UV dapat berbeda sedikit sebab vertex seam diduplikasi. Dokumentasi dan template laporan ada di `LAPORAN.md`; lengkapi identitas, tautan repositori, screenshot asli, serta data FPS dari mesin Anda sebelum dikumpulkan.
