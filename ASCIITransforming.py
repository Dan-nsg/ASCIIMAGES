from PIL import Image, ImageDraw, ImageFont
import numpy as np
import tkinter as tk
from tkinter import filedialog, simpledialog

# Mapa de caracteres ASCII baseados em tons de cinza
ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

def resize_image(image, new_width=100):
    """Redimensiona a imagem mantendo a proporção."""
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.55)
    return image.resize((new_width, new_height))

def grayify(image):
    """Converte a imagem para tons de cinza."""
    return image.convert("L")

def pixels_to_ascii(image, detail_level=10):
    """Converte os pixels da imagem em caracteres ASCII."""
    pixels = np.array(image)
    ascii_str = ""
    for pixel_value in pixels:
        for value in pixel_value:
            ascii_str += ASCII_CHARS[value // (256 // detail_level)]
        ascii_str += "\n"
    return ascii_str

def save_as_image(ascii_art, output_file="ascii_image.png"):
    """Salva a arte ASCII como uma imagem PNG."""
    # Usa uma fonte monoespaçada (Courier) para garantir a consistência
    font = ImageFont.truetype("cour.ttf", 10)
    
    # Cria uma imagem em branco suficientemente grande para o texto
    lines = ascii_art.splitlines()
    max_width = max(len(line) for line in lines)
    max_height = len(lines)
    
    # Calcula o tamanho do texto e cria uma imagem proporcional
    char_width, char_height = font.getbbox("A")[2], font.getbbox("A")[3]
    img_width = char_width * max_width
    img_height = char_height * max_height
    
    image = Image.new("RGB", (img_width, img_height), "white")
    draw = ImageDraw.Draw(image)
    
    # Desenha o texto na imagem
    y = 0
    for line in lines:
        draw.text((0, y), line, fill="black", font=font)
        y += char_height
    
    # Salva a imagem
    image.save(output_file)

def main(new_width=100):
    """Executa o processo de conversão da imagem para arte ASCII."""
    # Configura uma janela para selecionar a imagem
    root = tk.Tk()
    root.withdraw()
    image_path = filedialog.askopenfilename(title="Selecione uma imagem", 
                                            filetypes=[("Image files", "*.jpg *.png *.jpeg *.bmp *.gif")])

    if not image_path:
        print("Nenhuma imagem selecionada.")
        return

    # Executa o processo de conversão da imagem para arte ASCII.
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(f"Erro ao abrir a imagem: {e}")
        return
    
    image = resize_image(image, new_width)
    image = grayify(image)
    
    # Pede ao usuário o nível de detalhe
    detail_level = simpledialog.askinteger("Detalhe", "Escolha o nível de detalhe (1-10):", minvalue=1, maxvalue=10)
    ascii_art = pixels_to_ascii(image, detail_level)

    # Pede ao usuário o formato de saída
    output_format = simpledialog.askstring("Formato", "Escolha o formato de saída (TXT ou PNG):").lower()

    if output_format == "txt":
        with open("ascii_image.txt", "w") as f:
            f.write(ascii_art)
        print("Arte ASCII salva em ascii_image.txt")
    elif output_format == "png":
        save_as_image(ascii_art, "ascii_image.png")
        print("Arte ASCII salva em ascii_image.png")
    else:
        print("Formato desconhecido. Salvando como TXT por padrão.")
        with open("ascii_image.txt", "w") as f:
            f.write(ascii_art)

if __name__ == "__main__":
    main()
