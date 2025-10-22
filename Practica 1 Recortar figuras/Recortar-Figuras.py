import cv2 as cv
import numpy as np

img = cv.imread('figura.png', 1)
img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

umbralBajoRojo1 = (0, 80, 80)
umbralAltoRojo1 = (10, 255, 255)
umbralBajoRojo2 = (170, 80, 80)
umbralAltoRojo2 = (180, 255, 255)

umbralBajoVerde = (35, 80, 80)
umbralAltoVerde = (80, 255, 255)

umbralBajoAzul = (100, 80, 80)
umbralAltoAzul = (130, 255, 255)

umbralBajoAmarillo = (20, 80, 80)
umbralAltoAmarillo = (30, 255, 255)

mascaraRojo1 = cv.inRange(img_hsv, umbralBajoRojo1, umbralAltoRojo1)
mascaraRojo2 = cv.inRange(img_hsv, umbralBajoRojo2, umbralAltoRojo2)
mascaraRojo = mascaraRojo1 + mascaraRojo2

mascaraVerde = cv.inRange(img_hsv, umbralBajoVerde, umbralAltoVerde)

mascaraAzul = cv.inRange(img_hsv, umbralBajoAzul, umbralAltoAzul)

mascaraAmarillo = cv.inRange(img_hsv, umbralBajoAmarillo, umbralAltoAmarillo)

cv.imshow('Figuras Rojas', mascaraRojo)
cv.imshow('Figuras Verdes', mascaraVerde)
cv.imshow('Figuras Azules', mascaraAzul)
cv.imshow('Figuras Amarillas', mascaraAmarillo)
cv.waitKey(0)
cv.destroyAllWindows()