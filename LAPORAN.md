# Laporan Praktikum Grafika Komputer — Minggu 11

> Template untuk dilengkapi dengan identitas dan **hasil pengujian nyata**. Jangan mengklaim screenshot/FPS yang belum diambil. Ekspor ke PDF/DOCX dan masukkan bersama kode sumber dalam ZIP sesuai instruksi dosen.

## Cover dan identitas

- Judul: **3D Visual Realism Suite — Rendering Faces**
- Nama: **[isi nama]**
- NIM: **[isi NIM]**
- Kelas: **[isi kelas]**
- Mata kuliah: Grafika Komputer, Minggu 11
- Link GitHub: **[isi setelah push ke repository]**

## Dasar teori dan formulasi

**Phong dan Blinn-Phong.** Dengan normal satuan N, arah lampu L, arah mata V, vektor refleksi R = reflect(−L,N), dan halfway H = normalize(L+V), intensitas lokal adalah ambient + diffuse + specular. Diffuse = max(N·L,0); specular Phong = max(R·V,0)^16, Blinn-Phong = max(N·H,0)^32. Eksponen berbeda agar ukuran highlight relatif dapat dibandingkan. Perhitungan dilakukan per-fragment; warna dasar dari sampel tekstur atau warna material.

**Flat dan smooth.** Flat memakai satu normal hasil cross product sisi segitiga pada seluruh face. Smooth memakai penjumlahan normal face berbobot luas pada setiap vertex lalu dinormalisasi. Normal tersebut diinterpolasi perspektif-korektif oleh GPU, lalu dinormalisasi kembali di fragment shader. Normal matrix `transpose(inverse(model))` menjaga arah normal saat transformasi model.

**Z-buffer dan culling.** Depth buffer menyimpan kedalaman terdekat tiap piksel; `GL_LESS` membuat fragmen yang lebih dekat lolos. Face dengan winding belakang dibuang menggunakan `GL_BACK`, `GL_CCW`. Bidang dekat kamera 0.1, jauh 60 untuk menghindari presisi depth yang terlalu buruk. Geometri coplanar harus dihindari agar tidak z-fighting.

**UV dan filtering.** Sphere memakai u=longitude/(2π), v=1−latitude/π; lantai memakai UV berulang. Rasterizer GPU menginterpolasi UV secara perspektif-korektif: u = Σ(λᵢuᵢ/wᵢ)/Σ(λᵢ/wᵢ). PNG dibalik secara vertikal saat dimuat. Mode nearest menggunakan `GL_NEAREST_MIPMAP_NEAREST`, mode halus `GL_LINEAR_MIPMAP_LINEAR` untuk minifikasi dan `GL_LINEAR` untuk magnifikasi.

**Shadow mapping.** Pass 1 menyimpan kedalaman scene dari lampu dalam depth texture FBO (2048²). Pass 2 memproyeksikan posisi fragmen ke light space, membandingkan kedalaman saat ini dengan depth map; sampel PCF 3×3 menghaluskan tepi. Bias `max(0.006(1−N·L),0.0008)` membatasi shadow acne; bias terlalu besar dapat menyebabkan peter-panning. Ambient tetap terlihat dalam area bayangan.

## Struktur kode dan implementasi

Lihat `README.md` untuk arsitektur kelas. Vertex shader mentransformasi posisi dan normal serta meneruskan UV dan light-space position. Fragment shader menghitung ambient, diffuse, specular dan shadow. `ShadowMapFBO` menyiapkan texture attachment `GL_DEPTH_COMPONENT24`, memeriksa kelengkapan FBO, dan mengembalikan viewport sebelum pass kamera. `HSRManager` mengatur depth dan culling; `Texture2D` mengelola STBImage dan mipmap. Sphere menyimpan dua VAO/VBO agar mode flat dan smooth dapat diganti tanpa membuat ulang mesh setiap frame.

## Tangkapan layar dan hasil pengujian

Jalankan `./run.ps1` dari desktop dengan GPU. Ambil **screenshot asli** untuk tiap baris di bawah; sertakan judul jendela yang memuat mode dan FPS. Untuk pembandingan yang adil, bandingkan dari sudut kamera sama dan selisih waktu lampu yang kecil.

| Indikator | Langkah uji | Bukti yang harus ditempel | Hasil/observasi Anda |
|---|---|---|---|
| Phong vs Blinn | B dua kali | Dua screenshot highlight | [isi] |
| Flat vs smooth | F dua kali | Dua screenshot sisi sphere | [isi] |
| HSR depth/culling | Z dan C on/off | Screenshot occlusion + status judul | [isi] |
| UV/filtering | T, M, zoom dekat/jauh | Screenshot nearest vs linear/mipmap | [isi] |
| Shadow mapping | L on/off | Screenshot bayangan bergerak di lantai | [isi] |

## Pembahasan performa dan bias

Catat resolusi, OS, GPU, dan apakah VSync aktif (kode menggunakan VSync=1 sehingga FPS dapat dibatasi refresh monitor). Rata-ratakan FPS dari judul jendela setelah stabil selama beberapa detik.

| Kondisi | FPS rata-rata | Kondisi tampilan / artefak |
|---|---:|---|
| Blinn, smooth, bayangan on | [isi] | [isi] |
| Phong, smooth, bayangan on | [isi] | [isi] |
| Flat, bayangan on | [isi] | [isi] |
| Bayangan off (pass depth tetap dihitung) | [isi] | [isi] |

Perhatikan bahwa toggle `L` hanya mematikan penggunaan bayangan di pass kamera, **bukan** meniadakan pass depth: perbandingan FPS bukan pengukuran biaya penuh shadow mapping. Perubahan bias terlalu kecil memicu shadow acne; terlalu besar memisahkan bayangan dari objek. Jika perlu, ubah konstanta bias pada `phong.frag`, ulangi uji, dan tulis nilai yang dicoba berikut hasilnya. Jangan menyebut pengukuran yang belum dilakukan sebagai fakta.

## Kesimpulan

[Rangkum perbandingan visual, pengaruh filtering/HSR, kualitas bayangan dan trade-off performa dari pengamatan Anda.]
