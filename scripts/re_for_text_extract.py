# re_for_text_extraction.py
import re
import cv2
import pytesseract
from bound_box import caixa_texto, escreve_texto

img_path = r"C:\Users\PauloMenezes\Desktop\computer-vision\sample_data\text-recognize\Imagens\Aula4-tabela_teste.png"
img = cv2.imread(img_path)
rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
min_conf = 40

resultado = pytesseract.image_to_data(
    rgb,
    output_type=pytesseract.Output.DICT,
    lang='por',
    config='--psm 6'
)

regex = r'^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[012])/(19|20)\d\d$'

img_copia = rgb.copy()

for i in range(len(resultado['text'])):
    confianca = int(resultado['conf'][i])
    if confianca > min_conf:
        texto = resultado['text'][i]

        if re.match(regex, texto):
            # Desenha o bounding box em verde (0, 255, 0)
            x, y, img_copia = caixa_texto(resultado, img_copia, i, (0, 255, 0))
            
            # Se quiser escrever o texto APENAS nos que batem com a regex:
            cv2.putText(img_copia, texto, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        else:
            # Bounding box padrão (laranja)
            x, y, img_copia = caixa_texto(resultado, img_copia, i)

cv2.imshow("Resultado Regex", img_copia)
cv2.waitKey(0)
cv2.destroyAllWindows()
