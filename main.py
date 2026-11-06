class Quiz: 
    def __init__(self, question, choices, answer):
        #init은 초기화를 의미
        self.question = question 
        self.choices = choices 
        self.answer = answer 
    def display(self):
        #display는 출력하는 기능
        print(f"[문제]{self.question}\n")
        for idx, choice in enumerate(self.choices,1):
            print(f"{idx}. {choice}")
            #선택지 4개를 1번부터 번호 붙인다는거

    def is_correct(self, user_answer):
        #is_correct는 답 확인하는 함수
        return user_answer == self.answer

#테스트용 퀴즈
if __name__ == "__main__":
    #main.py파일이 직접 실행되었을때만 아래코드 실행해라
    sample_quiz = Quiz(
        "Python의 창시자는 누구?",
        ["Guido van Rossum", "James Gosling", "Bjarne Stroustrup", "Dennis Ritchie"],
        1
    ) 

#퀴즈 출력 및 정답 확인 
sample_quiz.display()
print("정답확인(1입력시):",sample_quiz.is_correct(1))


