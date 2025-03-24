import cv2
import pytesseract

MIN_CONF = 40

IMG = r"C:\Users\PauloMenezes\Desktop\computer-vision\sample_data\text-recognize\Imagens\Aula3-testando.png"
rgb = cv2.cvtColor(cv2.imread(IMG), cv2.COLOR_BGR2RGB)
config = r"--oem 3 --psm 6"

resultado = pytesseract.image_to_data(rgb, output_type=pytesseract.Output.DICT, lang='por', config=config)

def caixa_texto(resultado, img, i, cor=(255, 100, 0)):
    x = resultado['left'][i]
    y = resultado['top'][i]
    w = resultado['width'][i]
    h = resultado['height'][i]
    cv2.rectangle(img, (x, y), (x+w, y+h), cor, 2)
    return img

img_copia = rgb.copy()
for i in range(len(resultado['text'])):
    confianca = int(resultado['conf'][i])
    if confianca > MIN_CONF:
        img_copia = caixa_texto(resultado, img_copia, i)
        texto = resultado['text'][i]
        cv2.putText(
            img_copia, texto, (resultado['left'][i], resultado['top'][i] - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2
        )

cv2.imshow("Image", img_copia)
cv2.waitKey(0)
cv2.destroyAllWindows()
