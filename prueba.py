import cv2
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame= cv2.flip(frame, 1)
    # Convertir imagen a RGB (MediaPipe usa RGB)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    # Variables para guardar coordenadas
    left_index = None
    right_index = None
    # Centro y tamaño por defecto del rectángulo azul
    center_x, center_y = 200, 200
    base_half = 100  # medio ancho/alto por defecto
    current_half = base_half
    angle = 0  # ángulo de rotación del cuadrado azul
    
    # Función para rotar un punto alrededor de un centro
    def rotate_point(point, center, angle_deg):
        angle_rad = np.deg2rad(angle_deg)
        cx, cy = center
        px, py = point
        qx = cx + np.cos(angle_rad) * (px - cx) - np.sin(angle_rad) * (py - cy)
        qy = cy + np.sin(angle_rad) * (px - cx) + np.cos(angle_rad) * (py - cy)
        return int(qx), int(qy)
            
    if results.multi_hand_landmarks and results.multi_handedness:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            label = handedness.classification[0].label  # 'Left' o 'Right'
            #print(label)
            h, w, _ = frame.shape
            
            # Coordenadas del índice (landmark 8)
            index_tip = hand_landmarks.landmark[8]
            x, y = int(index_tip.x * w), int(index_tip.y * h)
            
            # Obtener más puntos de la mano para calcular la rotación
            wrist = hand_landmarks.landmark[0]  # punto de la muñeca
            middle_tip = hand_landmarks.landmark[12]  # punta del dedo medio
            
            # Guardar según la mano
            if label == 'Left':
                left_index = (x, y)
                # Calcular el ángulo de rotación basado en la orientación de la mano izquierda
                dx = middle_tip.x - wrist.x
                dy = middle_tip.y - wrist.y
                angle = np.degrees(np.arctan2(dy, dx))
            elif label == 'Right':
                right_index = (x, y)

            # Dibujar los landmarks (opcional)
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Si ambas manos detectadas, dibujar línea entre los dos puntos (rectángulo verde)
        if left_index and right_index:
            # Dibujar rectángulo verde entre los índices
            cv2.rectangle(frame, left_index, right_index, (0, 255, 0), 3)
            cv2.circle(frame, left_index, 8, (255, 0, 0), -1)
            cv2.circle(frame, right_index, 8, (0, 0, 255), -1)
            # Calcular tamaño del rectángulo verde y usarlo para escalar el azul
            lx, ly = left_index
            rx, ry = right_index
            green_w = abs(rx - lx)
            green_h = abs(ry - ly)
            green_half = int(max(green_w, green_h) / 2)
            # Mapear/clamp el tamaño para evitar valores extremos
            min_half = 30
            max_half = min(frame.shape[1], frame.shape[0]) // 2 - 10
            green_half = max(min_half, min(max_half, green_half))
            # Actualizar el rectángulo azul para que tenga el mismo tamaño (o escalar según sea necesario)
            current_half = green_half
            # Opcional: mostrar información de tamaño
            cv2.putText(frame, f"verde: {green_half*2}px", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

        # Obtener los puntos del rectángulo rotado con el tamaño actual
        points = [
            (center_x - current_half, center_y - current_half),
            (center_x + current_half, center_y - current_half),
            (center_x + current_half, center_y + current_half),
            (center_x - current_half, center_y + current_half)
        ]
        rotated_points = [rotate_point(p, (center_x, center_y), angle) for p in points]
        # Dibujar el rectángulo azul rotado
        for i in range(4):
            cv2.line(frame, rotated_points[i], rotated_points[(i + 1) % 4], (255, 0, 0), 3)
        
        # Mostrar el ángulo de rotación
        cv2.putText(frame, f"angulo: {int(angle)}°", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2)

    cv2.imshow("Line", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()