import math

def f(x, persamaan):
    """Fungsi untuk mengevaluasi persamaan matematika dari input user."""
    # Menyiapkan konteks fungsi matematika agar user bisa mengetik 'exp', 'sin', dll.
    context = {
        'x': x,
        'exp': math.exp,
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'log': math.log,
        'sqrt': math.sqrt,
        'e': math.e,
        'pi': math.pi
    }
    return eval(persamaan, {"__builtins__": None}, context)

def metode_bagi_dua():
    print("=== Program Analisis Numerik: Metode Bagi Dua ===")
    
    # 1. Input Persamaan
    persamaan = input("Masukkan f(x) (contoh: x + exp(x)): ")
    
    # 2. Input Range
    try:
        a = float(input("Batas bawah (a): "))
        b = float(input("Batas atas (b): "))
    except ValueError:
        print("Error: Batas harus berupa angka.")
        return

    # 3. Input Epsilon (Default 0.0001)
    eps_input = input("Nilai Epsilon (kosongkan untuk default 0.0001): ")
    epsilon = float(eps_input) if eps_input.strip() != "" else 0.0001
    
    # 4. Pengecekan Awal (Teorema Bolzano)
    fa = f(a, persamaan)
    fb = f(b, persamaan)
    
    print(f"\nMelakukan pengecekan awal...")
    print(f"f(a) = {fa:.6f}")
    print(f"f(b) = {fb:.6f}")
    
    # Sesuai gambar aturan: f(a)*f(b) < 0 maka terdapat akar
    if fa * fb > 0:
        print("\n[PENGHENTIAN PROGRAM]")
        print("Alasan: Tidak ditemukan akar persamaan dalam range ini.")
        print("Penjelasan: Berdasarkan Teorema, f(a) * f(b) harus < 0 (berlawanan tanda) agar dipastikan terdapat akar.")
        return

    # 5. Iterasi Inti
    max_iter = 1000
    iterasi = 0
    
    print(f"\n{'Iterasi':<8} | {'a':<14} | {'b':<14} | {'x (Tengah)':<14} | {'f(a)':<20}| {'f(x)':<16}")
    print("-" * 102)

    while iterasi < max_iter:
        iterasi += 1
        
        # Hitung titik tengah x
        x = (a + b) / 2
        fx = f(x, persamaan)
        fa = f(a, persamaan)
        
        print(f"{iterasi:<8} | a = {a:<10.6f} | b = {b:<10.6f} | x = {x:<10.6f} | f(a) = {fa:<13.6f}| f(x) = {fx:<16.6f}")

        # Cek apakah nilai f(x) sudah memenuhi toleransi epsilon
        if abs(fx) < epsilon:
            print("-" *102)
            print(f"\nAKAR DITEMUKAN PADA ITERASI KE-{iterasi}")
            print(f"Nilai x      : {x:.6f}")
            print(f"Nilai f(x)   : {fx:.6f}")
            print(f"Range akhir  : [{a:.6f}, {b:.6f}]")
            break
            
        # 6. Syarat Pembaruan Selang (Interval Updating Rules)
        # Sesuai aturan: f(a)*f(x) < 0 maka x = b (a tetap)
        if fa * fx < 0:
            b = x
        # Sesuai aturan: f(a)*f(x) > 0 maka x = a (b tetap)
        else:
            a = x

        # Cek penghentian berdasarkan lebar selang (alternatif stop condition)
        if abs(b - a) < epsilon:
            print("-" * 102)
            print(f"\nAKAR DITEMUKAN (Batas toleransi lebar selang tercapai)")
            print(f"Akar pendekatan x = {(a+b)/2:.6f} pada iterasi ke-{iterasi}")
            break
            
    if iterasi >= max_iter:
        print(f"\nProgram berhenti karena mencapai batas maksimum {max_iter} iterasi.")

if __name__ == "__main__":
    metode_bagi_dua()