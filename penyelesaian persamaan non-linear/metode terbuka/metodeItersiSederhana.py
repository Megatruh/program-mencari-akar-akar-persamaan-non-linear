import sympy as sp
from tabulate import tabulate

def iterasi_sederhana(persamaan_str, list_x0, epsilon=0.0001):
    x = sp.symbols('x')
    
    # 1. Parsing persamaan g(x) dari string
    try:
        g_x = sp.simplify(persamaan_str)
        g_prime = sp.diff(g_x, x) # Menghitung turunan g'(x) secara otomatis
    except Exception as e:
        return f"Error dalam pembacaan persamaan: {e}"

    semua_hasil = []

    for x0 in list_x0:
        data_pengujian = {
            "x0": x0,
            "status": "Divergen",
            "iterasi_data": []
        }
        
        # 2. Validasi Golden Rule: |g'(x0)| < 1
        val_g_prime = abs(float(g_prime.subs(x, x0)))
        
        if val_g_prime < 1:
            data_pengujian["status"] = "Konvergen"
            
            xn = x0
            iterasi = 0
            while True:
                # Menghitung x_next
                try:
                    xn_plus_1 = float(g_x.subs(x, xn))
                except:
                    data_pengujian["status"] = "Error (Nilai Imajiner/Tak Terdefinisi)"
                    break
                    
                selisih = abs(xn_plus_1 - xn)
                
                # Simpan baris data: [iterasi, xn, g(xn), xn+1, |xn+1 - xn|]
                data_pengujian["iterasi_data"].append([
                    iterasi, 
                    round(xn, 6), 
                    round(xn_plus_1, 6), 
                    round(xn_plus_1, 6), 
                    round(selisih, 8)
                ])
                
                if selisih < epsilon or iterasi > 100: # Limit 100 iterasi agar tidak loop selamanya
                    break
                
                xn = xn_plus_1
                iterasi += 1
        
        semua_hasil.append(data_pengujian)
    
    return semua_hasil

# --- INPUT PENGGUNA ---
print("="*60)
print("METODE ITERASI SEDERHANA")
print("="*60)

# Input formula persamaan g(x)
print("\nMasukkan persamaan g(x):")
print("Contoh: (-x**3 + 3) / 6  atau  x**3 + 4*x**2 - 10")
formula = input("g(x) = ")

# Input tebakan awal
print("\nMasukkan tebakan awal (pisahkan dengan koma):")
print("Contoh: 0.5, 0.1, 2.2, 2.7")
tebakan_input = input("Tebakan awal: ")
tebakan_awal = [float(x.strip()) for x in tebakan_input.split(',')]

# Input toleransi
print("\nMasukkan nilai toleransi:")
toleransi = float(input("Toleransi (misal: 0.0001): "))

# Eksekusi
hasil_uji = iterasi_sederhana(formula, tebakan_awal, toleransi)

# --- DISPLAY HASIL ---
for hasil in hasil_uji:
    print(f"\n{'='*60}")
    print(f"PENGUJIAN UNTUK x0 = {hasil['x0']}")
    print(f"Status Validasi: {hasil['status']}")
    print(f"{'='*60}")
    
    if hasil['status'] == "Konvergen":
        headers = ["Iterasi", "xn", "g(xn)", "xn+1", "|xn+1 - xn|"]
        print(tabulate(hasil['iterasi_data'], headers=headers, tablefmt="grid"))
    else:
        print(f"Perhitungan dihentikan karena nilai x0 bersifat {hasil['status']}.")