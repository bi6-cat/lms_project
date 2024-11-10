import pandas as pd


import  cv2
import  os

from exams.Scan_score.test_scanner import Test_Scanner

def get_files_inTestPics():
    return [x for x in os.listdir('D:/Code/Project_Python/Scan_score/images')] #Duong dan tuyet doi ta co the thay bang duong dan tuong doi

folder_path = "images"
def main(answer): #Input dap an bai kiem tra / OutPut list[[IdStudent,Score,IdExam]] tat ca Sv
    Student_list_TestScore = []
    files = get_files_inTestPics()
    folder_path = "images"
    for filename in os.listdir(folder_path):
        # Answer input : 50 dap an
        # ans = list(map(int, input().split()))
        # path = "D:/Code/Project_PythonScan_score/images/" + path
        path = os.path.join(folder_path, filename)
        widthImg = 800
        heightImg = 800
        img = cv2.imread(path)
        img = cv2.resize(img, (widthImg, heightImg))
        T_scanner = Test_Scanner(answer, img)

        Student_list_TestScore.append(T_scanner.get_Infor())
        # print(Student_list_TestScore[0])

    df = pd.DataFrame(Student_list_TestScore, columns=['IdStudent', 'Score', 'IdExam'])
    df.to_csv('Test_Scanner.csv')
    return  Student_list_TestScore

# answer = ["A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A", "A","A", "A","A", "A","A", "A","A", "A","A", "A","A", "A","A", "A","A", "A","A", "A","A", "A","A", "A"]
# m = main(answer)
# print (m)