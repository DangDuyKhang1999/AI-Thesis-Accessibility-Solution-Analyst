# Happy Case MVP: 1 image -> Vietnamese description

Muc tieu: Chay nhanh 1 luong thanh cong de chung minh y tuong MVP.

## 1) Cai dat

Từ thư mục gốc của dự án:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 2) Cau hinh API key Gemini

```powershell
Copy-Item .env.example .env
# Điền GEMINI_API_KEY; HF_TOKEN là tùy chọn cho web nhưng CLI legacy cần để thử HF TTS.
```

## 3) Chay demo

Chay nhanh voi anh mau da co san (`assets/samples/bar.png`):

```powershell
python .\run_happy_case.py
```

Hoac truyen anh bat ky:

```powershell
python .\run_happy_case.py --image "duong_dan_den_anh.png"
```

Neu muon doi file output:

```powershell
python .\run_happy_case.py --image "duong_dan_den_anh.png" --out "output/mo_ta_vi.txt"
```

## 4) Ket qua

- Console in ra mo ta tieng Viet co cau truc
- File text duoc luu mac dinh tai `output/description_vi.txt`

## 5) Pham vi happy case

- Dau vao: 1 anh ro net, mot man hinh/chu de chinh
- Dau ra: 1 ban mo ta tieng Viet de dua qua TTS o buoc sau
- Chua xu ly fallback local, chua co multi-image, chua co schema validation day du
