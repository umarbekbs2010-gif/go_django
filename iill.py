from pathlib import Path
import qrcode

OUTPUT_DIR = Path("qrcodes")


def sanitize_filename(raw_name: str) -> str:
    """Fayl nomidagi xavfli belgilarni tozalaydi."""
    cleaned = "".join(
        ch for ch in raw_name.strip() if ch.isalnum() or ch in ("-", "_")
    )
    return cleaned if cleaned else "qr_code"


def generate_qr_code(data: str, filename: str) -> Path:
    """Berilgan matn yoki havola asosida PNG formatda QR kod yaratadi."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    safe_name = sanitize_filename(filename)
    file_path = OUTPUT_DIR / f"{safe_name}.png"

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    image = qr.make_image(fill_color="black", back_color="white")
    image.save(file_path)
    return file_path


def run_app() -> None:
    """Foydalanuvchidan ma'lumot olib, QR kod yaratish siklini yuritadi."""
    print("=== QR Kod Generator ===")

    while True:
        data = input("\nHavola yoki matn kiriting (chiqish uchun 'exit' yozing): ").strip()

        if data.lower() == "exit":
            print("Dastur yakunlandi. Xayr!")
            break

        if not data:
            print("Xato: Bo'sh matn yoki havola kiritib bo'lmaydi.")
            continue

        raw_name = input("Saqlanadigan rasm nomi (masalan: my_github): ").strip()
        saved_path = generate_qr_code(data, raw_name)
        print(f"Tayyor! QR kod saqlandi: {saved_path}")


if __name__ == "__main__":
    run_app()