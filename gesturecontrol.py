
# Import required libraries
import cv2                      # OpenCV for image processing and webcam input
import mediapipe as mp          # MediaPipe for hand tracking
import math                     # For calculating Euclidean distance

# HandDetector Class Definition
class HandDetector:
    """
    A class to detect and track hands using MediaPipe, extract landmark positions,
    calculate distances, and identify finger states (up/down).
    """

    # Initialization
    def __init__(self, mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        """
        Initialize the HandDetector with optional configuration.
        """
        self.mode = mode
        self.max_num_hands = max_num_hands
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        # MediaPipe Hands initialization
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.max_num_hands,
            min_detection_confidence=self.min_detection_confidence,
            min_tracking_confidence=self.min_tracking_confidence
        )

        # Utility for drawing hand landmarks
        self.mp_drawing = mp.solutions.drawing_utils

        # State variables
        self.results = None
        self.lm_list = []
        self.tip_ids = [4, 8, 12, 16, 20]  # Landmark indices of fingertips

    # Find Hands in an Image
    def find_hands(self, img, draw=True):
        """
        Detect hands and optionally draw landmarks on the image.
        """
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_drawing.draw_landmarks(
                        img, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                    )

        return img

    # Find Position of Hand Landmarks
    def find_position(self, img=None, hand_no=0, draw=True):
        """
        Extract the landmark positions of a specified hand.

        Parameters:
        - img: Image to draw landmarks on (optional if draw=True)
        - hand_no: Which hand to process (default 0)
        - draw: Whether to draw landmarks and bounding box

        Returns:
        - lm_list: list of landmark positions [[id, x, y], ...]
        - bbox: bounding box [xmin, ymin, xmax, ymax]
        """
        self.lm_list = []
        x_list, y_list = [], []
        bbox = []

        if self.results and self.results.multi_hand_landmarks:
            if hand_no < len(self.results.multi_hand_landmarks):
                hand_landmarks = self.results.multi_hand_landmarks[hand_no]

                for idx, lm in enumerate(hand_landmarks.landmark):
                    if img is not None:
                        h, w, _ = img.shape
                    else:
                        # Cannot draw or compute position without image shape
                        # Return empty if img not provided and draw requested
                        if draw:
                            return [], []
                        # If draw is False, just continue with zeros (skip)
                        h, w = 1, 1

                    cx, cy = int(lm.x * w), int(lm.y * h)
                    self.lm_list.append([idx, cx, cy])
                    x_list.append(cx)
                    y_list.append(cy)

                    if draw and img is not None:
                        cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

                # Bounding box calculation
                xmin, xmax = min(x_list), max(x_list)
                ymin, ymax = min(y_list), max(y_list)
                bbox = [xmin, ymin, xmax, ymax]

                if draw and img is not None:
                    cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

        return self.lm_list, bbox

    # Find Distance Between Two Landmarks
    def find_distance(self, p1, p2, img=None, draw=True):
        """
        Calculate Euclidean distance between two hand landmarks.

        Parameters:
        - p1, p2: landmark indices
        - img: image for drawing (optional)
        - draw: whether to draw visual markers (default True)

        Returns:
        - distance: float Euclidean distance
        - img: image with drawings if img provided
        - info: list [x1, y1, x2, y2, cx, cy] positions
        """
        if len(self.lm_list) <= max(p1, p2):
            return 0, img, [0, 0, 0, 0, 0, 0]

        x1, y1 = self.lm_list[p1][1], self.lm_list[p1][2]
        x2, y2 = self.lm_list[p2][1], self.lm_list[p2][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw and img is not None:
            cv2.circle(img, (x1, y1), 10, (0, 128, 255), cv2.FILLED)     # Orange-ish
            cv2.circle(img, (x2, y2), 10, (75, 0, 130), cv2.FILLED)      # Indigo
            cv2.line(img, (x1, y1), (x2, y2), (60, 179, 113), 2)         # Medium Sea Green
            cv2.circle(img, (cx, cy), 10, (255, 215, 0), cv2.FILLED)     # Gold


        distance = math.hypot(x2 - x1, y2 - y1)
        return distance, img, [x1, y1, x2, y2, cx, cy]

    # Determine Which Fingers Are Up
    def finger_up(self):
        """
        Check which fingers are raised (1) or folded (0).

        Returns:
        - List of 5 integers (0 or 1) representing thumb to pinky
        """
        fingers = []

        if not self.lm_list or len(self.lm_list) < 21:
            return fingers

        # Thumb (based on x-coordinate difference between tip and adjacent landmark)
        if self.lm_list[self.tip_ids[0]][1] > self.lm_list[self.tip_ids[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Other fingers (based on y-coordinate: tip vs pip joint)
        for i in range(1, 5):
            if self.lm_list[self.tip_ids[i]][2] < self.lm_list[self.tip_ids[i] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers
