import sympy as sp
from tabulate import tabulate

def regula_falsi(persamaan_str, a, b, epsilon=0.0001, max_iterasi=100):
    """
    Metode Regula Falsi untuk mencari akar persamaan non-linear
    
    Formula: c = (a * f(b) - b * f(a)) / (f(b) - f(a))
    
    Parameter:
    - persamaan_str: string persamaan f(x)
    - a: batas bawah interval
    - b: batas atas interval
    - epsilon: toleransi error
    - max_iterasi: maksimum jumlah iterasi
    """
    x = sp.symbols('x')
    
    # Parsing persamaan f(x)
    try:
        f_x = sp.sympify(persamaan_str)
    except Exception as e:
        return {"status": "Error", "pesan": f"Error dalam pembacaan persamaan: {e}"}
    
    # Evaluasi f(a) dan f(b)
    fa = float(f_x.subs(x, a))
    fb = float(f_x.subs(x, b))
    
    # Validasi: f(a) dan f(b) harus berlawanan tanda
    if fa * fb > 0:
        return {
            "status": "Error",
            "pesan": f"f(a) dan f(b) harus berlawanan tanda. f({a}) = {fa:.6f}, f({b}) = {fb:.6f}"
        }
    
    iterasi_data = []
    iterasi = 0
    c_sebelumnya = a
    
    while iterasi < max_iterasi:
        # Hitung c menggunakan rumus Regula Falsi
        # c = (a * f(b) - b * f(a)) / (f(b) - f(a))
        c = (a * fb - b * fa) / (fb - fa)
        fc = float(f_x.subs(x, c))
        
        # Hitung error
        if iterasi > 0:
            error = abs(c - c_sebelumnya)
        else:
            error = abs(b - a)
        
        # Simpan data iterasi
        iterasi_data.append([
            iterasi,
            round(a, 8),
            round(b, 8),
            round(c, 8),
            round(fa, 8),
            round(fb, 8),
            round(fc, 8),
            round(error, 10)
        ])
        
        # Cek konvergensi
        if abs(fc) < epsilon or error < epsilon:
            return {
                "status": "Konvergen",
                "akar": c,
                "iterasi": iterasi + 1,
                "iterasi_data": iterasi_data,
                "f_akar": fc
            }
        
        # Update interval
        if fa * fc < 0:
            # Akar berada di [a, c]
            b = c
            fb = fc
        else:
            # Akar berada di [c, b]
            a = c
            fa = fc
        
        c_sebelumnya = c
        iterasi += 1
    
    # Jika mencapai max iterasi
    return {
        "status": "Max Iterasi",
        "akar": c,
        "iterasi": iterasi,
        "iterasi_data": iterasi_data,
        "pesan": f"Mencapai maksimum iterasi ({max_iterasi})"
    }

# --- INPUT PENGGUNA ---
print("="*70)
print("METODE REGULA FALSI (FALSE POSITION)")
print("="*70)

# Input persamaan f(x)
print("\nMasukkan persamaan f(x):")
print("Contoh: x**3 + 4*x**2 - 10  atau  x**3 - x - 2")
persamaan = input("f(x) = ")

# Input interval [a, b]
print("\nMasukkan interval [a, b]:")
a = float(input("a = "))
b = float(input("b = "))

# Input toleransi
print("\nMasukkan nilai toleransi:")
toleransi = float(input("Toleransi (misal: 0.0001): "))

# Input max iterasi (opsional)
print("\nMasukkan maksimum iterasi (tekan Enter untuk default 100):")
max_iter_input = input("Max iterasi: ")
max_iter = int(max_iter_input) if max_iter_input else 100

print("\n" + "="*70)
print("HASIL PERHITUNGAN")
print("="*70)

# Eksekusi
hasil = regula_falsi(persamaan, a, b, toleransi, max_iter)

# --- DISPLAY HASIL ---
if hasil["status"] == "Error":
    print(f"\n❌ ERROR: {hasil['pesan']}")
else:
    print(f"\nPersamaan: f(x) = {persamaan}")
    print(f"Interval: [{a}, {b}]")
    print(f"Toleransi: {toleransi}")
    print(f"\nStatus: {hasil['status']}")
    
    # Tampilkan tabel iterasi
    headers = ["Iterasi", "a", "b", "c", "f(a)", "f(b)", "f(c)", "Error"]
    print("\n" + tabulate(hasil['iterasi_data'], headers=headers, tablefmt="grid"))
    
    # Tampilkan akar
    print(f"\n✓ AKAR PERSAMAAN: x ≈ {hasil['akar']:.10f}")
    print(f"  f(x) ≈ {hasil['f_akar']:.10e}")
    print(f"  Jumlah Iterasi: {hasil['iterasi']}")
    
    if "pesan" in hasil:
        print(f"\n⚠ Catatan: {hasil['pesan']}")

print("\n" + "="*70)
