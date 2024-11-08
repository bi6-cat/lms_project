
import  numpy as np
import  cv2
from exams.Scan_score import utlis
from exams.Scan_score import student
import  pandas as pd
class Test_Scanner:
    def __init__(self,ans,img):
        self.ans = ans
        self.img = img
    def get_Infor(self):
        # ans = [1, 2, 3, 4, 3, 1, 2, 3, 4, 4, 1, 2, 2, 4, 4, 1, 1, 1, 2, 2, 3, 3, 3, 3, 1, 1, 1, 3, 3, 2, 2, 2, 2, 2, 4,
        #        3, 3, 1, 1, 1, 1, 2, 2, 1, 4, 4, 4, 4, 4, 2]
        self.widthImg = 800
        self.heightImg = 800

        # path = "img1.jpg"
        # img = cv2.imread(path)
        # img = cv2.resize(img, (widthImg, heightImg))

        imgContour = self.img.copy()
        imgFinal = self.img.copy()
        imgBiggestContour = self.img.copy()
        questions = 25
        choices = 5

        # processing------------------------------------------------
        imgGray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
        # Detect edges (using County function)
        imgCanny = cv2.Canny(imgBlur, 10, 30)

        # find all Contour
        contour, hierarchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(imgContour, contour, -1, (0, 255, 0), 8)

        # find rectangles
        rectcon = utlis.rectContour(contour)

        ScoreContour1 = utlis.getCornerPoint(rectcon[0])
        ScoreContour2 = utlis.getCornerPoint(rectcon[1])
        IdStudentContour = utlis.getCornerPoint(rectcon[4])
        IdExamCountour = utlis.getCornerPoint(rectcon[5])
        cnt = 0
        if (
                ScoreContour1.size != 0 and ScoreContour2.size != 0 and IdStudentContour.size != 0 and IdExamCountour.size != 0):
            cv2.drawContours(imgBiggestContour, ScoreContour1, -1, (0, 255, 0), 15)
            cv2.drawContours(imgBiggestContour, ScoreContour2, -1, (255, 0, 0), 15)
            cv2.drawContours(imgBiggestContour, IdStudentContour, -1, (255, 0, 0), 15)
            cv2.drawContours(imgBiggestContour, IdExamCountour, -1, (255, 0, 0), 15)

            ScoreContour1 = utlis.reorder(ScoreContour1)
            ScoreContour2 = utlis.reorder(ScoreContour2)

            IdStudentContour = utlis.reorder(IdStudentContour)
            IdExamCountour = utlis.reorder(IdExamCountour)
            # ----------------------------------------------------
            # Set Bird Eyes
            pt1 = np.float32(ScoreContour1)
            pt2 = np.float32([[0, 0], [self.widthImg, 0], [0, self.heightImg], [self.widthImg, self.heightImg]])
            matrix = cv2.getPerspectiveTransform(pt1, pt2)
            imgWarpColored = cv2.warpPerspective(self.img, matrix, (self.widthImg, self.heightImg))

            # Apply threshold
            imgWarpGray = cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2GRAY)
            imgThresh = cv2.threshold(imgWarpGray, 130, 200, cv2.THRESH_BINARY_INV)[1]

            boxes = utlis.splitBoxes(imgThresh)

            # # Getting the non zero pixel val of each
            myPixelVal = np.zeros((questions, choices))
            countC = 0
            countR = 0
            for image in boxes:
                totalPixels = cv2.countNonZero(image)
                myPixelVal[countR][countC] = totalPixels
                countC += 1
                if countC == choices:
                    countC = 0
                    countR += 1

            myPixelVal = np.delete(myPixelVal, 0, axis=1)

            # Fiding index val of markings
            myIndex = []
            for x in range(0, questions):
                arr = myPixelVal[x]
                myIndexVal = np.where(arr == np.amax(arr))
                # print(myIndexVal[0])
                myIndex.append(myIndexVal[0][0])

            # Grading
            grading = []
            for x in range(0, questions):
                cnt += 1
                if (self.ans[x] == myIndex[x] + 1):
                    grading.append(1)
                else:
                    grading.append(0)

            # FinalScore
            score = sum(grading) * 0.2

            # ----------------------------------------------------------------SCORE2

            # Set Bird Eyes
            # Set Bird Eyes
            pt1 = np.float32(ScoreContour2)
            pt2 = np.float32([[0, 0], [self.widthImg, 0], [0, self.heightImg], [self.widthImg, self.heightImg]])
            matrix = cv2.getPerspectiveTransform(pt1, pt2)
            imgWarpColored = cv2.warpPerspective(self.img, matrix, (self.widthImg, self.heightImg))

            # Apply threshold
            imgWarpGray = cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2GRAY)
            imgThresh = cv2.threshold(imgWarpGray, 100, 250, cv2.THRESH_BINARY_INV)[1]

            boxes = utlis.splitBoxes(imgThresh)
            # cv2.imshow("test" , boxes[10])

            # Getting the non zero pixel val of each
            myPixelVal = np.zeros((questions, choices))
            countC = 0
            countR = 0
            for image in boxes:
                totalPixels = cv2.countNonZero(image)
                myPixelVal[countR][countC] = totalPixels
                countC += 1
                if countC == choices:
                    countC = 0
                    countR += 1
            myPixelVal = np.delete(myPixelVal, 0, axis=1)

            # Fiding index val of markings
            myIndex = []
            for x in range(0, questions):
                arr = myPixelVal[x]
                myIndexVal = np.where(arr == np.amax(arr))

                myIndex.append(myIndexVal[0][0])

            # Grading
            grading = []
            for x in range(0, questions):
                if (self.ans[x + cnt] == myIndex[x] + 1):
                    grading.append(1)
                else:
                    grading.append(0)

            # FinalScore
            score1 = sum(grading) * 0.2
            # ---------------------------------------------------------------------------------
            totalScore = score1 + score
            # --------------------------------------------------------------------IdStudent

            # Set Bird Eyes

            pt1 = np.float32(IdStudentContour)
            pt2 = np.float32([[0, 0], [self.widthImg, 0], [0, self.heightImg], [self.widthImg, self.heightImg]])
            matrix = cv2.getPerspectiveTransform(pt1, pt2)
            imgWarpColored = cv2.warpPerspective(self.img, matrix, (self.widthImg, self.heightImg))

            # Apply threshold
            imgWarpGray = cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2GRAY)
            imgThresh = cv2.threshold(imgWarpGray, 130, 250, cv2.THRESH_BINARY_INV)[1]
            scaler = imgThresh.shape[0] // 6
            idX = 0
            idStudent = []

            for i in range(6):

                boxes = utlis.splitBoxes2(imgThresh[0:, idX:idX + scaler])
                idX += scaler
                # Getting the non zero pixel val of each
                myPixelVal = np.zeros((10, 1))
                countC = 0
                countR = 0
                for image in boxes:
                    totalPixels = cv2.countNonZero(image)
                    myPixelVal[countR][countC] = totalPixels
                    countC += 1
                    if countC == 1:
                        countC = 0
                        countR += 1

                    # Fiding index val of markings
                maxS = max(myPixelVal)
                for i in range(10):
                    if (myPixelVal[i][0] == maxS):
                        idStudent.append(i)
                        break
            IdStudent = ""
            for id in idStudent:
                IdStudent += str(id)
            # print(IdStudent)

            # ----------------------------------------------------------------IdExam
            pt1 = np.float32(IdExamCountour)
            pt2 = np.float32([[0, 0], [self.widthImg, 0], [0, self.heightImg], [self.widthImg, self.heightImg]])
            matrix = cv2.getPerspectiveTransform(pt1, pt2)
            imgWarpColored = cv2.warpPerspective(self.img, matrix, (self.widthImg, self.heightImg))

            # Apply threshold
            imgWarpGray = cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2GRAY)
            imgThresh = cv2.threshold(imgWarpGray, 130, 250, cv2.THRESH_BINARY_INV)[1]
            scaler = imgThresh.shape[0] // 3
            idX = 0
            idEx = []

            for i in range(3):

                boxes = utlis.splitBoxes2(imgThresh[0:, idX:idX + scaler])
                idX += scaler
                # Getting the non zero pixel val of each
                myPixelVal = np.zeros((10, 1))
                countC = 0
                countR = 0
                for image in boxes:
                    totalPixels = cv2.countNonZero(image)
                    myPixelVal[countR][countC] = totalPixels
                    countC += 1
                    if countC == 1:
                        countC = 0
                        countR += 1

                    # Fiding index val of markings
                maxS = max(myPixelVal)
                for i in range(10):
                    if (myPixelVal[i][0] == maxS):
                        idEx.append(i)
                        break
            IdExam = ""
            for id in idEx:
                IdExam += str(id)
            # print(IdExam)
        # new_student = student.Student(IdStudent, totalScore, IdExam)
        return [IdStudent, totalScore, IdExam]