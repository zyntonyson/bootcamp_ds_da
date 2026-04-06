import argparse
import os
import re

try:
    import qrcode
except ImportError:
    print("Error: Las librerías 'qrcode' y 'Pillow' son necesarias.")
    print("Por favor, instálalas usando: pip install qrcode[pil]")
    exit(1)

def generate_qr(url, out_path):
    # Aseguramos que el directorio exista
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    
    # Generar y guardar el QR
    img = qrcode.make(url)
    img.save(out_path)
    print(f"QR generado: {out_path} -> {url}")

def main():
    parser = argparse.ArgumentParser(description="Generador de QRs a partir de URLs o archivo Markdown")
    parser.add_argument("--url", type=str, help="URL específica para codificar en formato QR")
    parser.add_argument("--filename", type=str, help="Nombre del archivo de salida (con o sin .png)")
    parser.add_argument("--index_file", type=str,default="Index-notebooks.md" ,help="Archivo md con enlaces a generar")
    

    args = parser.parse_args()

    # Directorio base para los qrs
    base_dir = os.path.join("img", "qrs")

    # Si se pasan los parametros individuales (--url y --filename)
    if args.url and args.filename:
        fname = args.filename
        if not fname.endswith(".png"):
            fname += ".png"
            
        out_path = os.path.join(base_dir, os.path.basename(fname))
        generate_qr(args.url, out_path)
        return

    # Si no hay argumentos, leemos el archivo Index-notebooks.md
    
    if not os.path.exists(args.index_file):
        print(f"No se encontró el archivo {args.index_file} en el directorio actual.")
        print("Uso alternativo: python generate_qrs.py --url <URL> --filename <nombre_archivo>")
        return
    
    print(f"Procesando {args.index_file}...")
    
    # Expresión regular para encontrar enlaces en markdown: [texto](url)
    pattern = re.compile(r'\[([^\]]+)\]\((https?://[^\)]+)\)')
    
    contador = 0
    with open(args.index_file, "r", encoding="utf-8") as f:
        for line in f:
            match = pattern.search(line)
            if match:
                name = match.group(1).strip()
                url = match.group(2).strip()
                
                # Limpiar el nombre para que sea un nombre de archivo válido
                safe_name = "".join(c for c in name if c.isalnum() or c in ('-', '_')).strip()
                
                if not safe_name:
                    continue
                    
                out_path = os.path.join(base_dir, f"{safe_name}.png")
                generate_qr(url, out_path)
                contador += 1
                
    print(f"\nSe generaron {contador} códigos QR exitosamente en la carpeta '{base_dir}'.")

if __name__ == "__main__":
    main()
