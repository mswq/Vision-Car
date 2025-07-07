import cv2
import mediapipe

cap = cv2.VideoCapture(0)

class Hand:
    def __init__(self):
        self.mp_drawing = mediapipe.solutions.drawing_utils
        self.mp_drawing_styles = mediapipe.solutions.drawing_styles
        self.mp_hands = mediapipe.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.landmark_list = []

    def detect(self, frame):
        results = self.hands.process(frame)
        if results.multi_hand_landmarks:
            annotated = frame.copy()

            for landmarks in results.multi_hand_landmarks:
                self.landmark_list = []
                for lm in landmarks.landmark:
                    self.landmark_list.append(lm)

                self.mp_drawing.draw_landmarks(
                    annotated, landmarks,
                    self.mp_hands.HAND_CONNECTIONS, 
                    self.mp_drawing_styles.get_default_hand_landmarks_style(), 
                    self.mp_drawing_styles.get_default_hand_connections_style())
            return annotated
        return frame

    def pinky_down(self):
        if self.landmark_list[20].y > self.landmark_list[17].y:
            return True
        return False
    
    def ring_down(self):
        if self.landmark_list[16].y > self.landmark_list[13].y:
            return True
        return False
    
    def middle_down(self):
        if self.landmark_list[12].y > self.landmark_list[9].y:
            return True
        return False
    
    def index_down(self):
        if self.landmark_list[8].y > self.landmark_list[5].y:
            return True
        return False
    
    def no_hand_detected(self):
        if len(self.landmark_list) != 21:
            return True
        return False
    
    def tilt(self):
        tilt = self.landmark_list[8].x - self.landmark_list[0].x
        return tilt
    
    def stop(self):
        if len(self.landmark_list) == 21:
            if self.index_down() and self.middle_down() and self.ring_down() and self.pinky_down():
                return True
        return False
    
    def go(self):
        if len(self.landmark_list) == 21:
            if not self.index_down() and not self.middle_down() and self.ring_down() and self.pinky_down():
                return True
            return False
        
    def right(self):
        if len(self.landmark_list) == 21:
            if self.go() and self.tilt() > 0.15:
                return True
        return False
    
    def left(self):
        if len(self.landmark_list) == 21:
            if self.go() and self.tilt() < -0.15:
                return True
        return False
            

        

if __name__ == "__main__":
    hand = Hand()

    while cap.isOpened():
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        frame = hand.detect(frame)

        if hand.stop():
            print ("\nSTOPPED")
    
        if hand.right():
            print ("\nRIGHT")
        elif hand.left():
            print ("\nLEFT")
        elif hand.go():
            print ("\nGO")

        cv2.imshow("Webcam", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
