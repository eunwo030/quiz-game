import sys


class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def display(self):
        print("\n-----------------------------")
        print(f"[문제] {self.question}")
        for idx, choice in enumerate(self.choices, 1):
            print(f"{idx}. {choice}")
        print("-----------------------------")

    def is_correct(self, user_answer):
        return user_answer == self.answer


class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.best_score = 0
        self.init_default_quizzes()

    def init_default_quizzes(self):
        # 기본 퀴즈 5개
        self.quizzes = [
            Quiz("배은우가 사는 지역은?", ["서울", "부산", "대전", "광주"], 4),
            Quiz("배은우의 나이는?", ["20살", "25살", "30살", "35살"], 1),
            Quiz("배은우의 MBTI는?", ["ENFJ", "ENTJ", "INFJ", "ESTJ"], 2),
            Quiz("배은우가 좋아하는 노래장르는?", ["발라드", "힙합", "트로트", "팝송"], 4),
            Quiz("배은우의 전공은?", ["컴퓨터공학", "경영학", "심리학", "산업공학"], 4),
        ]

    def display_menu(self):
        print("=============================")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 최고 점수 확인")
        print("5. 종료")
        print("=============================")

    def get_valid_input(self, prompt, min_val, max_val):
        """숫자 입력 예외 처리 공통 메서드"""
        while True:
            try:
                user_input = input(prompt).strip()
                if not user_input:
                    print(" 입력이 비어있습니다. 다시 입력해주세요.")
                    continue
                num = int(user_input)
                if min_val <= num <= max_val:
                    return num
                else:
                    print(f" {min_val}에서 {max_val} 사이의 숫자를 입력해주세요.")
            except ValueError:
                print(" 유효한 숫자를 입력해주세요.")

    def play_quiz(self):
        """1. 퀴즈 풀기 기능"""
        if not self.quizzes:
            print("\n 등록된 퀴즈가 없습니다! 퀴즈를 먼저 추가해 주세요.")
            return

        print(f"\n 퀴즈를 시작합니다! (총 {len(self.quizzes)}문제)")
        score = 0

        for idx, quiz in enumerate(self.quizzes, 1):
            print(f"\n[{idx}번 문제]")
            quiz.display()
            user_ans = self.get_valid_input("정답 입력 (1~4): ", 1, 4)

            if quiz.is_correct(user_ans):
                print(" 정답입니다!")
                score += 1
            else:
                print(f" 틀렸습니다. 정답은 {quiz.answer}번입니다.")

        print("\n=============================")
        print(f" 결과: {len(self.quizzes)}문제 중 {score}문제 정답!")

        if score > self.best_score:
            self.best_score = score
            print(" 축하합니다! 새로운 최고 점수를 기록했습니다!")
        print("=============================")

    def add_quiz(self):
        """2. 퀴즈 추가 기능"""
        print("\n 새로운 퀴즈를 추가합니다.")
        question = input("문제를 입력하세요: ").strip()
        while not question:
            print(" 문제는 빈 칸일 수 없습니다.")
            question = input("문제를 입력하세요: ").strip()

        choices = []
        for i in range(1, 5):
            choice = input(f"선택지 {i}: ").strip()
            while not choice:
                print(" 선택지는 빈 칸일 수 없습니다.")
                choice = input(f"선택지 {i}: ").strip()
            choices.append(choice)

        answer = self.get_valid_input("정답 번호 (1~4): ", 1, 4)

        new_quiz = Quiz(question, choices, answer)
        self.quizzes.append(new_quiz)
        print("\n 새로운 퀴즈가 성공적으로 추가되었습니다!")

    def show_quizzes(self):
        """3. 퀴즈 목록 기능"""
        if not self.quizzes:
            print("\n 등록된 퀴즈가 없습니다.")
            return

        print(f"\n 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        for idx, quiz in enumerate(self.quizzes, 1):
            print(f"[{idx}] {quiz.question}")

    def show_best_score(self):
        """4. 최고 점수 확인 기능"""
        print("\n=============================")
        print(f" 현재 최고 점수: {self.best_score}점")
        print("=============================")

    def run(self):
        while True:
            try:
                self.display_menu()
                choice = self.get_valid_input("선택: ", 1, 5)

                if choice == 1:
                    self.play_quiz()
                elif choice == 2:
                    self.add_quiz()
                elif choice == 3:
                    self.show_quizzes()
                elif choice == 4:
                    self.show_best_score()
                elif choice == 5:
                    print("\n 프로그램을 종료합니다.")
                    break
            except (KeyboardInterrupt, EOFError):
                print("\n\n 프로그램이 안전하게 종료되었습니다.")
                sys.exit(0)


if __name__ == "__main__":
    game = QuizGame()
    game.run()