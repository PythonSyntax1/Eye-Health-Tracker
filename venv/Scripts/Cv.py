import math
import cv2
import dlib
import report
from datetime import timedelta, datetime

blinkCount = 0
threshold = 0.2
countThreshold = 1
tracking = False


# Uses trigonometry to calculate distance between points
def distance(p0, p1):
    return math.sqrt((p0.x - p1.x) ** 2 + (p0.y - p1.y) ** 2)


def calibrate():
    # If calibration is finished and tracking has begun
    global tracking
    # The amount of blinks
    global blinkCount
    # The maximum ratio that is counted as eyes closed
    global threshold
    # The number of consecutive eyes closed detections it takes to count as one blink
    global countThreshold
    print("Press 'c' to calibrate, otherwise, press any letter to begin")
    val = input("Choose option: ")
    if val == 'c':
        print("Please blink 5 times while looking at the web-cam, with a one second break between each blink. Press "
              "'q' "
              "when complete.")
        count = record()
        # If the number of blinks is counted correctly with a margin of error of 1 blink, tracking will begin
        if 4 <= count <= 6:
            print("The program is calibrated well. Blink tracking will now begin.")
            tracking = True
            blinkCount = 0
            record()
            return
        # If the program tracks too little blinks, it will increase sensitivity
        elif count < 4:
            print("The program is not sensitive enough. It is now adjusted. Please try again.")
            threshold += 0.01
            blinkCount = 0
            calibrate()
            return
        # If the program tracks too many blinks, it will decrease sensitivity.
        else:
            print("The program is too sensitive. It is now adjusted. Please try again.")
            countThreshold += 1
            blinkCount = 0
            calibrate()
            return
    else:
        blinkCount = 0
        record()
        return



def record():
    # Sets a timer for one hour from when recording begins
    dt = datetime.now() + timedelta(hours=1)
    vid = cv2.VideoCapture(0)
    # Facial landmark library
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    currentCount = 0
    while True:
        check, frame = vid.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        for face in faces:
            landmarks = predictor(gray, face)

            # Finds position of landmarks in right eye.
            leftVerticalDistOne = distance(landmarks.part(37), landmarks.part(41))
            leftVerticalDistTwo = distance(landmarks.part(38), landmarks.part(40))
            leftHorizontalDist = distance(landmarks.part(36), landmarks.part(39))
            leftEyeRatio = (leftVerticalDistOne + leftVerticalDistTwo) / (2 * leftHorizontalDist)

            # Finds position of landmarks in left eye.
            rightVerticalDistOne = distance(landmarks.part(43), landmarks.part(47))
            rightVerticalDistTwo = distance(landmarks.part(44), landmarks.part(46))
            rightHorizontalDist = distance(landmarks.part(42), landmarks.part(45))
            rightEyeRatio = (rightVerticalDistTwo + rightVerticalDistOne) / (2 * rightHorizontalDist)

            avgEyeRatio = (leftEyeRatio + rightEyeRatio) / 2

            # Checks if you blinked. Other if statements are to ensure that one blink is not counted as multiple
            if avgEyeRatio < threshold:
                print(avgEyeRatio)
                currentCount += 1
            if currentCount == countThreshold and avgEyeRatio < threshold:
                global blinkCount
                blinkCount += 1
                print(blinkCount)
            if currentCount > 0 and avgEyeRatio > 0.18:
                currentCount = 0

        cv2.imshow("Frame", frame)

        # Sends a report of blinking status every hour.
        global Tracking
        if datetime.now() > dt and Tracking:
            newReport = report.Report(blinkCount, 60)
            newReport.sendMail()
            dt = datetime.now() + timedelta(hours=1)

        #Quits when pressing q
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    vid.release()
    cv2.destroyAllWindows()
    print(blinkCount)
    return blinkCount



if __name__ == "__main__":
    calibrate()
