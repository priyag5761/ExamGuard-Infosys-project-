import cv2
import os

def capture_photo(username):

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("Cannot open camera")
        return False

    while True:

        success, frame = camera.read()

        if not success:
            break

        cv2.putText(
            frame,
            "Press C to Capture | Q to Quit",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0,255,0),
            2
        )

        cv2.imshow("Registration Photo", frame)

        key = cv2.waitKey(1)

        if key == ord('c'):

            os.makedirs("static/images", exist_ok=True)

            filename = f"static/images/{username}.jpg"

            cv2.imwrite(filename, frame)

            print("Photo Saved")

            break

        elif key == ord('q'):
            camera.release()
            cv2.destroyAllWindows()
            return False

    camera.release()
    cv2.destroyAllWindows()

    return True