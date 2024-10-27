
# CREATE TABLE Exam (
#     exam_id INT PRIMARY KEY AUTO_INCREMENT,
#     course_id INT NOT NULL,
#     exam_name VARCHAR(255) NOT NULL,
#     exam_date DATE
# );

# -- Bảng đáp án chuẩn của bài thi
# CREATE TABLE ExamKey (
#     examkey_id INT PRIMARY KEY AUTO_INCREMENT,
#     exam_id INT NOT NULL,
#     question_number INT NOT NULL,
#     correct_answer ENUM('A', 'B', 'C', 'D') NOT NULL,
#     UNIQUE (exam_id, question_number)
# );

# -- Bảng lưu câu trả lời của học sinh cho bài thi
# CREATE TABLE ExamAnswer (
#     answer_id INT PRIMARY KEY AUTO_INCREMENT,
#     exam_id INT NOT NULL,
#     student_id INT NOT NULL,
#     question_number INT NOT NULL,
#     answer ENUM('A', 'B', 'C', 'D') NOT NULL,
#     UNIQUE (exam_id, student_id, question_number)
# );

# -- Bảng lưu kết quả bài thi của học sinh
# CREATE TABLE ExamResult (
#     result_id INT PRIMARY KEY AUTO_INCREMENT,
#     exam_id INT NOT NULL,
#     student_id INT NOT NULL,
#     total_score DECIMAL(5, 2),
#     graded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     UNIQUE (exam_id, student_id)
# );