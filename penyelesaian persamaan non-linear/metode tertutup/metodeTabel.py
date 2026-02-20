import math

def f(x, persamaan):
    """Fungsi untuk mengevaluasi persamaan matematika dari input user."""
    # Context menyediakan fungsi matematika standar agar user bisa mengetik 'exp', 'sin', dll.
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

def metode_tabel():
    print("=== Program Analisis Numerik: Metode Tabel ===")
    
    # 1. Input Persamaan [cite: 136]
    persamaan = input("Masukkan f(x) (contoh: x + exp(x)): ")
    
    # 2. Input Range [cite: 137]
    try:
        x_bawah = float(input("Batas bawah (x_bawah dalam bentuk desimal : 11.22): "))
        x_atas = float(input("Batas atas (x_atas dalam bentuk desimal : 33.44): "))
    except ValueError:
        print("Error: Batas harus berupa angka.")
        return

    # 3. Input Epsilon (Default 0.0001)
    eps_input = input("Nilai Epsilon (kosongkan untuk default 0.0001): ")
    epsilon = float(eps_input) if eps_input.strip() != "" else 0.0001
    
    # Jumlah baris pembagi tetap 10 (N=10) [cite: 138, 157]
    N = 10
    iterasi_tabel = 1
    maks_refinement = 10 # Batas agar tidak terjadi looping abadi

    while iterasi_tabel <= maks_refinement:
        # 4. Hitung step pembagi h [cite: 140]
        h = (x_atas - x_bawah) / N
        
        print(f"\nTABEL ITERASI KE-{iterasi_tabel} (Range: [{x_bawah:.6f}, {x_atas:.6f}])")
        print(f"Interval = {h:.6f}\n")
        print(f"{'i':<4} | {'x_i':<12} | {'f(x_i)':<12}")
        print("-" * 35)
        
        data_tabel = []
        for i in range(N + 1):
            # 5. Hitung xi dan yi [cite: 142, 143]
            xi = x_bawah + i * h
            try:
                yi = f(xi, persamaan)
            except Exception as e:
                print(f"Error dalam kalkulasi: {e}")
                return
            
            data_tabel.append((xi, yi))
            print(f"{i:<4} | {xi:<12.6f} | {yi:<12.6f}")
            
        # 6. Cari k dimana f(xk) * f(xk+1) < 0 (Perubahan tanda) [cite: 113, 146]
        k = -1
        for i in range(N):
            if data_tabel[i][1] * data_tabel[i+1][1] <= 0:
                k = i
                break
        
        if k == -1:
            print("\nError: Akar tidak ditemukan (tidak ada perubahan tanda di range ini).")
            break
            
        # Ambil nilai yang paling mendekati nol sebagai kandidat akar [cite: 116, 147]
        if abs(data_tabel[k][1]) < abs(data_tabel[k+1][1]):
            akar_terdekat = data_tabel[k]
        else:
            akar_terdekat = data_tabel[k+1]
            
        # Cek apakah error (|f(x)|) sudah lebih kecil dari epsilon [cite: 233]
        if abs(akar_terdekat[1]) < epsilon:
            print(f"\nAKAR DITEMUKAN!")
            print(f"Setelah {iterasi_tabel} iterasi tabel:")
            print(f"Range akhir: [{x_bawah:.6f}, {x_atas:.6f}]")
            print(f"x = {akar_terdekat[0]:.6f}")
            print(f"f(x) = {akar_terdekat[1]:.6f} (Error < {epsilon})")
            break
        else:
            # Jika belum teliti, buat range baru dari [xk, xk+1] 
            x_bawah = data_tabel[k][0]
            x_atas = data_tabel[k+1][0]
            iterasi_tabel += 1

    if iterasi_tabel > maks_refinement:
        print("\nBatas pengulangan tabel tercapai. Gunakan metode lain untuk ketelitian lebih tinggi.")

if __name__ == "__main__":
    metode_tabel()