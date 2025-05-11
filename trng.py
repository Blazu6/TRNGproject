import sys
import numpy as np
import os
import matplotlib.pyplot as plt

TARGET_SIZE = 13_500_000  # 13.5 MB

def entropy(labels, base=2):
    vals, counts = np.unique(labels, return_counts=True)
    probs = counts / counts.sum()
    return -(probs * np.log(probs) / np.log(base)).sum()

def collect_data_from_multiple_files(target_size=TARGET_SIZE):
    data = bytearray()
    while len(data) < target_size:
        remaining = target_size - len(data)
        print(f"🔹 Potrzebuję jeszcze {remaining} bajtów. Podaj ścieżkę do pliku:")
        path = input("> ").strip()

        if not os.path.isfile(path):
            print(f"❌ Plik '{path}' nie istnieje.")
            continue

        with open(path, 'rb') as f:
            chunk = f.read(remaining)
            data.extend(chunk)
            print(f"📥 Dodano {len(chunk)} bajtów z '{path}'.")

    return bytes(data[:target_size])  # Na wszelki wypadek przytnij

def copy_binary_file_fixed_size(output_file, block_size=64):
    try:
        data = collect_data_from_multiple_files()
        all_bytes = []
        entropy_per_block = []

        with open(output_file, 'wb') as f_out:
            for i in range(0, len(data), block_size):
                chunk = data[i:i+block_size]
                if len(chunk) < block_size:
                    chunk += b'\x00' * (block_size - len(chunk))
                all_bytes.extend(chunk)
                f_out.write(chunk)

                entropy_block = entropy(chunk)
                entropy_per_block.append(entropy_block)

        print(f"✅ Zapisano do pliku '{output_file}' blokami ({block_size} B).")
        overall_ent = entropy(all_bytes)
        print(f"ℹ️ Entropia bajtów: {overall_ent:.6f} bitów na bajt")

        byte_values = np.array(all_bytes)
        plt.figure(figsize=(10, 5))
        plt.hist(byte_values, bins=256, range=(0, 255), color='steelblue', edgecolor='black')
        plt.title("Histogram rozkładu wartości bajtów (0–255)")
        plt.xlabel("Wartość bajtu")
        plt.ylabel("Liczba wystąpień")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"❌ Wystąpił błąd: {e}")

if __name__ == "__main__":
    copy_binary_file_fixed_size("output.bin")
