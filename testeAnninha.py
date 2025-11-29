import numpy as np
import cv2
import serial, time



def main():
	ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

	print("Serial aberta em:", ser.port)
	time.sleep(2)
	#ser.write(b'a')
	
	face_classifier = cv2.CascadeClassifier(
		'/home/lennedy/software/testes/venv/lib/python3.10/site-packages/cv2/data/haarcascade_lefteye_2splits.xml' #lembrar de mudar isso quando for pro comp de hellen
	)

	cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

	faces_detec = 0

	if not cap.isOpened():
		print("Erro!")
		return

	print("Sucesso! Q pra sair")

	face_presente = False   # Estado: tem ou não tem face na frente da câmera



	while True:
		ret, frame = cap.read()

		if not ret:
			print("Erro na captura")
			break
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		faces = face_classifier.detectMultiScale(
			gray, scaleFactor=1.05, minNeighbors=7, minSize=(80, 80)
		)
			
		#comunicação serial
		#if len(faces) > 0:
    			#ser.write(b"a")   # abre
    			#break
		#else:
    			#ser.write(b"f")   # fecha

		#if len(faces) > faces_detec:
			#faces_detec = len(faces)

		for (x, y, w, h) in faces:
			cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

		cv2.imshow("IFSAFE", frame)

		if cv2.waitKey(1)  == ord('q'):
			break
			
		if len(faces) > 0:
			if not face_presente:  
				print("Nova face detectada → enviando comando para abrir catraca.")
				ser.write(b'a')       # abre
				face_presente = True      # registra que a face está presente
				time.sleep(2)				
			else:
				pass
				
		else:
			if face_presente:
        			print("Face saiu → pronto para detectar novamente.")
			face_presente = False

	#print(f"Detectamos {faces_detec} face(s)")
	cap.release()
	cv2.destroyAllWindows()

if __name__== "__main__":
	main()
