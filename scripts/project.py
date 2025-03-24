import os
import cv2
import pytesseract
import re
from bound_box import caixa_texto, escreve_texto

# ================================
# Configurações iniciais
# ================================

IMAGE_DIR = r'C:\Users\PauloMenezes\Desktop\computer-vision\sample_data\text-recognize\Atividades\Aula 5'
OUTPUT_TXT = "ocr_result.txt"
OCR_LANG = 'por'  # Idioma do Tesseract
SEARCH_TERM = 'ambiente'  # Termo a ser buscado

# ================================
# Funções auxiliares
# ================================

def list_images(directory, extension=".png"):
    """Retorna uma lista com os caminhos das imagens no diretório, ignorando as que já têm bbox_ no nome."""
    return [
        os.path.join(directory, filename)
        for filename in os.listdir(directory)
        if filename.lower().endswith(extension) and not filename.startswith("bbox_")
    ]


def ocr_process(image):
    """Executa OCR em uma imagem com Tesseract."""
    return pytesseract.image_to_string(image, lang=OCR_LANG, config='--psm 6')

def save_ocr_results(image_paths, output_file):
    """Salva o resultado de OCR de várias imagens em um arquivo de texto."""
    full_text = ""
    for image_path in image_paths:
        image = cv2.imread(image_path)
        image_name = os.path.basename(image_path)

        full_text += f"================\n{image_name}\n================\n"
        extracted_text = ocr_process(image)
        full_text += extracted_text + '\n\n'

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(full_text)
    print(f"Arquivo {output_file} criado com sucesso!")

def search_term_in_text(file_path, term):
    """Procura por um termo em um arquivo de texto e retorna as posições."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        matches = [m.start() for m in re.finditer(term, content)]
    print(f"O termo '{term}' foi encontrado nas posições: {matches}")
    return matches

def search_term_in_images(image_paths, term):
    """Procura por um termo nas imagens e desenha bounding boxes nas ocorrências."""
    config = r"--oem 3 --psm 6"
    bbox_paths = []

    for image_path in image_paths:
        image = cv2.imread(image_path)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        resultado = pytesseract.image_to_data(
            rgb, output_type=pytesseract.Output.DICT,
            lang=OCR_LANG, config=config
        )

        encontrou = False
        for i, palavra in enumerate(resultado["text"]):
            if palavra.lower() == term.lower():
                encontrou = True
                caixa_texto(resultado, image, i)
                x = resultado['left'][i]
                y = resultado['top'][i]
                cv2.putText(
                    image, palavra, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2
                )

        image_name = os.path.basename(image_path)
        print(f"Imagem: {image_name}")
        print(f'O termo "{term}" foi {"encontrado" if encontrou else "não encontrado"}.\n')

        if encontrou:
            output_image_path = os.path.join(os.path.dirname(image_path), f"bbox_{image_name}")
            # Evita sobrescrever várias vezes
            if not os.path.basename(image_path).startswith("bbox_"):
                cv2.imwrite(output_image_path, image)
                print(f"Imagem com bounding boxes salva em: {output_image_path}")
                bbox_paths.append(output_image_path)

    return bbox_paths



def show_bboxed_images(image_paths):
    """Abre as imagens com bounding boxes para visualização."""
    for image_path in image_paths:
        image_name = os.path.basename(image_path)
        bbox_image_path = os.path.join(os.path.dirname(image_path), f"bbox_{image_name}")
        
        if os.path.exists(bbox_image_path):
            img = cv2.imread(bbox_image_path)
            cv2.imshow(f"Resultado: {image_name}", img)
            print(f"Abrindo imagem: {bbox_image_path}")
            cv2.waitKey(0)
            cv2.destroyAllWindows()




# ================================
# Execução principal
# ================================

if __name__ == "__main__":
    image_paths = list_images(IMAGE_DIR)

    if not image_paths:
        print("Nenhuma imagem encontrada no diretório.")
    else:
        save_ocr_results(image_paths, OUTPUT_TXT)
        search_term_in_text(OUTPUT_TXT, SEARCH_TERM)
        bbox_image_paths = search_term_in_images(image_paths, SEARCH_TERM)
        show_bboxed_images(bbox_image_paths)
