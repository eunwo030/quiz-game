import json
import os
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

    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["question"], data["choices"], data["answer"])


class QuizGame:
    def __init__(self, data_file="state.json"):
        self.data_file = data_file
        self.quizzes = []
        self.best_score = 0
        self.load_data()

    def init_default_quizzes(self):
        self.quizzes = [
            Quiz("배은우가 사는 지역은?", ["서울", "부산", "대전", "광주"], 3),
            Quiz("배은우의 나이는?", ["20살", "25살", "30살", "35살"], 1),
            Quiz("배은우의 MBTI는?", ["ENFJ", "ENTJ", "INFJ", "ESTJ"], 2),
            Quiz("배은우가 좋아하는 노래장르는?", ["발라드", "힙합", "트로트", "팝송"], 4),
            Quiz("배은우의 전공은?", ["컴퓨터공학", "경영학", "심리학", "산업공학"], 4),
        ]
        self.best_score = 0

    def save_data(self):
        """state.json 파일로 데이터 저장 (UTF-8)"""
        try:
            data = {
                "quizzes": [q.to_dict() for q in self.quizzes],
                "best_score": self.best_score,
            }
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"⚠️ 데이터 저장 실패: {e}")

    def load_data(self):
        """state.json 파일에서 데이터 불러오기 (예외 처리 포함)"""
        if not os.path.exists(self.data_file):
            print("📂 저장된 데이터가 없습니다. 기본 데이터를 사용합니다.")
            self.init_default_quizzes()
            self.save_data()
            return

        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.quizzes = [Quiz.from_dict(q) for q in data.get("quizzes", [])]
                self.best_score = data.get("best_score", 0)
            print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개, 최고점수 {self.best_score}점)")
        except (json.JSONDecodeError, KeyError, Exception) as e:
            print(f"⚠️ 파일 손상 또는 읽기 오류 발생! 기본 데이터로 복구합니다. ({e})")
            self.init_default_quizzes()
            self.save_data()

    def display_menu(self):
        print("\n=============================")
        print("        🎯 나만의 퀴즈 게임 🎯        ")
        print("=============================")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 최고 점수 확인")
        print("5. 종료")
        print("=============================")

    def get_valid_input(self, prompt, min_val, max_val):
        while True:
            try:
                user_input = input(prompt).strip()
                if not user_input:
                    print("⚠️ 입력이 비어있습니다. 다시 입력해주세요.")
                    continue
                num = int(user_input)
                if min_val <= num <= max_val:
                    return num
                else:
                    print(f"⚠️ {min_val}에서 {max_val} 사이의 숫자를 입력해주세요.")
            except ValueError:
                print("⚠️ 유효한 숫자를 입력해주세요.")

    def play_quiz(self):
        if not self.quizzes:
            print("\n⚠️ 등록된 퀴즈가 없습니다!")
            return

        print(f"\n📝 퀴즈를 시작합니다! (총 {len(self.quizzes)}문제)")
        score = 0

        for idx, quiz in enumerate(self.quizzes, 1):
            print(f"\n[{idx}번 문제]")
            quiz.display()
            user_ans = self.get_valid_input("정답 입력 (1~4): ", 1, 4)

            if quiz.is_correct(user_ans):
                print("✅ 정답입니다!")
                score += 1
            else:
                print(f"❌ 틀렸습니다. 정답은 {quiz.answer}번입니다.")

        print("\n=============================")
        print(f"🏆 결과: {len(self.quizzes)}문제 중 {score}문제 정답!")

        if score > self.best_score:
            self.best_score = score
            print("🎉 축하합니다! 새로운 최고 점수를 기록했습니다!")
            self.save_data()
        print("=============================")

    def add_quiz(self):
        print("\n📌 새로운 퀴즈를 추가합니다.")
        question = input("문제를 입력하세요: ").strip()
        while not question:
            print("⚠️ 문제는 빈 칸일 수 없습니다.")
            question = input("문제를 입력하세요: ").strip()

        choices = []
        for i in range(1, 5):
            choice = input(f"선택지 {i}: ").strip()
            while not choice:
                print("⚠️ 선택지는 빈 칸일 수 없습니다.")
                choice = input(f"선택지 {i}: ").strip()
            choices.append(choice)

        answer = self.get_valid_input("정답 번호 (1~4): ", 1, 4)

        new_quiz = Quiz(question, choices, answer)
        self.quizzes.append(new_quiz)
        self.save_data()
        print("\n✅ 새로운 퀴즈가 성공적으로 추가되었으며 state.json에 저장되었습니다!")

    def show_quizzes(self):
        if not self.quizzes:
            print("\n📋 등록된 퀴즈가 없습니다.")
            return

        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        for idx, quiz in enumerate(self.quizzes, 1):
            print(f"[{idx}] {quiz.question}")

    def show_best_score(self):
        print("\n=============================")
        print(f"🏆 현재 최고 점수: {self.best_score}점")
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
                    print("\n👋 프로그램을 종료합니다.")
                    break
            except (KeyboardInterrupt, EOFError):
                print("\n\n⚠️ 프로그램이 안전하게 종료되었습니다.")
                self.save_data()
                sys.exit(0)


if __name__ == "__main__":
    game = QuizGame()
    game.run()