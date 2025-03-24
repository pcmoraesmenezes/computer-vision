# bound_box.py
import cv2
import pytesseract

def caixa_texto(resultado, img, i, cor=(255, 100, 0)):
    """
    Desenha um retângulo na imagem 'img' referente ao índice 'i' 
    no dicionário 'resultado' do Tesseract.
    Retorna (x, y, img) para permitir o uso das coordenadas em outro lugar.
    """
    x = resultado['left'][i]
    y = resultado['top'][i]
    w = resultado['width'][i]
    h = resultado['height'][i]
    cv2.rectangle(img, (x, y), (x + w, y + h), cor, 2)
    return x, y, img

def escreve_texto(resultado, img, min_conf=40, cor=(255, 100, 0)):
    """
    Varre todas as detecções em 'resultado' e, se a confiança for maior 
    que 'min_conf', desenha o bounding box e escreve o texto na imagem.
    Retorna a imagem modificada.
    """
    for i in range(len(resultado['text'])):
        confianca = int(resultado['conf'][i])
        if confianca > min_conf:
            x, y, img = caixa_texto(resultado, img, i, cor)
            texto = resultado['text'][i]
            # Desenha o texto logo acima do bounding box
            cv2.putText(
                img, texto, (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2
            )
    return img

# Bloco para testes internos do módulo
if __name__ == "__main__":
    import cv2
    import pytesseract

    # Parâmetros de teste
    MIN_CONF = 40
    IMG = r"C:\Users\PauloMenezes\Desktop\computer-vision\sample_data\text-recognize\Imagens\Aula3-testando.png"
    config = r"--oem 3 --psm 6"

    # Carrega imagem e faz OCR
    img = cv2.imread(IMG)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    resultado = pytesseract.image_to_data(
        rgb, output_type=pytesseract.Output.DICT,
        lang='por', config=config
    )

    # Copia a imagem para desenhar
    img_copia = rgb.copy()

    # Usa a função escreve_texto para desenhar boxes e texto
    img_copia = escreve_texto(resultado, img_copia, MIN_CONF)

    # Exibe o resultado
    cv2.imshow("Teste bound_box.py", img_copia)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
