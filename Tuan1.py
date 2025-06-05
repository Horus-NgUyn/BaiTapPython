def bai1():
    chuoi = input("Nhập họ tên hoặc câu cần chuẩn hóa: ")
    ket_qua = ' '.join([word.capitalize() for word in chuoi.split()])
    print("Kết quả:", ket_qua)

def bai2():
    chuoi = input("Nhập chuỗi cần đảo ngược: ")
    ket_qua = ' '.join(chuoi.split()[::-1])
    print("Chuỗi sau khi đảo ngược:", ket_qua)

def bai3():
    chuoi = input("Nhập chuỗi: ")
    max_char = max(set(chuoi), key=chuoi.count)
    print(f"Ký tự xuất hiện nhiều nhất là: '{max_char}', số lần: {chuoi.count(max_char)}")

def bai4():
    chuoi = input("Nhập chuỗi: ")
    dem = {}
    for ky_tu in chuoi:
        dem[ky_tu] = dem.get(ky_tu, 0) + 1
    for k, v in dem.items():
        print(f"Ký tự '{k}': {v} lần")

def bai5():
    chuoi = input("Nhập chuỗi: ")
    so = [c for c in chuoi if c.isdigit()]
    if so:
        print("Chuỗi có chứa số. Các số tách ra là:", so)
    else:
        print("Chuỗi không chứa ký tự số.")

def bai6():
    chuoi = input("Nhập họ tên đầy đủ: ")
    ds = chuoi.strip().split()
    ho_lot = " ".join(ds[:-1])
    ten = ds[-1]
    print("Họ lót:", ho_lot)
    print("Tên:", ten)

def bai7():
    chuoi = input("Nhập chuỗi: ")
    ket_qua = ' '.join([tu.capitalize() for tu in chuoi.split()])
    print("Kết quả:", ket_qua)

def bai8():
    chuoi = input("Nhập chuỗi: ")
    ket_qua = ''.join([c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(chuoi)])
    print("Kết quả:", ket_qua)

def bai9():
    chuoi = input("Nhập chuỗi: ")
    if chuoi == chuoi[::-1]:
        print("Chuỗi là chuỗi đối xứng.")
    else:
        print("Chuỗi không đối xứng.")

def bai10():
    chu_so = ["không", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín"]

    def doc_so_ba_chu_so(n):
        tram = n // 100
        chuc = (n % 100) // 10
        donvi = n % 10
        ket_qua = f"{chu_so[tram]} trăm"
        if chuc == 0 and donvi != 0:
            ket_qua += " lẻ"
        elif chuc != 0:
            ket_qua += f" {chu_so[chuc]} mươi"
        if donvi == 1 and chuc > 1:
            ket_qua += " mốt"
        elif donvi == 5 and chuc != 0:
            ket_qua += " lăm"
        elif donvi != 0:
            ket_qua += f" {chu_so[donvi]}"
        return ket_qua

    so = int(input("Nhập số có 3 chữ số (100-999): "))
    if 100 <= so <= 999:
        print("Cách đọc:", doc_so_ba_chu_so(so))
    else:
        print("Vui lòng nhập số từ 100 đến 999.")

def menu():
    while True:
        print("\n=== MENU BÀI TẬP XỬ LÝ CHUỖI ===")
        print("1. Viết đầu câu sang chữ hoa và những từ không phải đầu câu sang chữ thường.")
        print("2. Đảo ngược thứ tự các từ")
        print("3. Ký tự xuất hiện nhiều nhất")
        print("4. Đếm số lần xuất hiện mỗi ký tự")
        print("5. Kiểm tra và tách ký tự số")
        print("6. Cắt chuỗi họ tên")
        print("7. Viết hoa chữ cái đầu từ (title case)")
        print("8. Chữ xen kẽ hoa - thường")
        print("9. Kiểm tra chuỗi đối xứng")
        print("10. Đọc số có 3 chữ số")
        print("0. Thoát")

        chon = input("Chọn bài (0-10): ")

        if chon == '1': bai1()
        elif chon == '2': bai2()
        elif chon == '3': bai3()
        elif chon == '4': bai4()
        elif chon == '5': bai5()
        elif chon == '6': bai6()
        elif chon == '7': bai7()
        elif chon == '8': bai8()
        elif chon == '9': bai9()
        elif chon == '10': bai10()
        elif chon == '0':
            print("Đã thoát chương trình.")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")

# Chạy menu chính
menu()