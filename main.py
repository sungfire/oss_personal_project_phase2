import pygame
import random
import time

# 게임 설정: 화면 크기, 격자 크기 및 지뢰 수 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
MINE_COUNT = 40  # 지뢰 총 개수 (default, HARD 기준)

# 게임 점수와 타이머를 구성하는 클래스
class Score:
    # 스코어 클래스 초기화, 점수와 타이머 시작 시간 설정
############################
#########PHASE2#############
############################
    def __init__(self, font, screen, mine_count, initial_score=0):
        self.score = initial_score
        self.start_time = time.time()
        self.font = font
        self.screen = screen
        self.opened_cells = 0
        self.remaining_mines = mine_count

    # 칸을 열 때마다 점수 증가
    def update_score_for_open_cell(self):
        self.opened_cells += 1
        self.score += 3

    # 깃발 우클릭시 점수 업데이트
    def update_score_for_flag(self, flag_set):
        self.score -= 1 if flag_set else 1
        self.remaining_mines -= 1 if flag_set else -1

    # 게임 오버시 점수 감소
    def apply_game_over_penalty(self):
        self.score -= 20

    # 난이도 별 클리어시 보너스 점수 차등적용
    def apply_victory_bonus(self, difficulty):
        bonus = {'easy': 50, 'medium': 100, 'hard': 200}
        self.score += bonus.get(difficulty, 0)

    # 화면에 현재 점수와 경과 시간 표시
    def display_score(self):
        elapsed_time = int(time.time() - self.start_time)
        score_time_text = f'Score: {self.score} | Time: {elapsed_time} sec | Mines: {self.remaining_mines}'
        display_text = self.font.render(score_time_text, True, (0, 0, 255))
        text_x = (self.screen.get_width() - display_text.get_width()) / 2
        self.screen.blit(display_text, (text_x, 10))

    # 게임 리셋시 점수와 타이머 초기화
    def reset(self, mine_count):
        self.start_time = time.time()
        self.score = 0
        self.opened_cells = 0
        self.remaining_mines = mine_count

    # 게임 종료시 최종 점수와 소요 시간 메시지 생성
    def final_message(self):
        elapsed_time = self.get_elapsed_time()
        return f"Final Score: {self.score}, Time Taken: {elapsed_time} sec"

    # 경과 시간 계산
    def get_elapsed_time(self):
        return int(time.time() - self.start_time)
############################
#########PHASE2#############
############################

# 지뢰찾기 보드판을 구성하는 클래스
class Minesweeper:
    # 게임 초기화, 화면 설정 및 게임 타이머 시작
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Minesweeper")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.choose_difficulty()
############################
#########PHASE2#############
############################
        self.scoreboard = Score(self.font, self.screen, self.mine_count)  # 스코어보드 초기화
############################
#########PHASE2#############
############################
        self.reset()

    # 난이도 선택 (easy, medium, hard)
    def choose_difficulty(self):
        print("Choose difficulty: Easy (1), Medium (2), Hard (3)")
        choice = input("Enter your choice (1, 2, 3): ")
        if choice == '1':
            self.grid_size = 8
            self.mine_count = 7
            self.screen_width = 400
            self.screen_height = 400
            self.current_difficulty = 'easy'
        elif choice == '2':
            self.grid_size = 10
            self.mine_count = 15
            self.screen_width = 500
            self.screen_height = 500
            self.current_difficulty = 'medium'
        else:
            self.grid_size = 20
            self.mine_count = 40
            self.screen_width = 800
            self.screen_height = 600
            self.current_difficulty = 'hard'
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

    # 모든 게임 필드 초기화
    def reset(self):
        self.mines = [[False] * self.grid_size for _ in range(self.grid_size)]
        self.adjacent = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.flags = [[False] * self.grid_size for _ in range(self.grid_size)]
        self.grid = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.game_over = False
        self.victory = False
        self.exploding_cells = []  # 폭발 애니메이션을 위한 칸 리스트
        self.explosion_start_time = None  # 폭발 시작 시간
        self.exploded_cells = []  # 폭발이 완료된 칸 리스트
        self.place_mines()
############################
#########PHASE2#############
############################
        self.scoreboard.reset(self.mine_count)
############################
#########PHASE2#############
############################

    # 게임 승리 조건을 확인하는 함수
    def check_victory(self):
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if (self.mines[x][y] and not self.flags[x][y]) or (not self.mines[x][y] and not self.grid[x][y]):
                    return False
        self.victory = True
        self.scoreboard.apply_victory_bonus(self.current_difficulty)  # 승리시 난이도별 보너스 점수 적용

        return True

    # 지뢰를 게임 보드에 무작위로 배치하는 함수
    def place_mines(self):
        placed = 0
        while placed < self.mine_count:
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            if not self.mines[x][y]:
                self.mines[x][y] = True
                self.increment_adjacent(x, y)  # 인접 칸 지뢰 수 증가
                placed += 1

    # 주어진 위치 주변의 지뢰 수를 증가시키는 함수
    def increment_adjacent(self, x, y):
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
                    self.adjacent[nx][ny] += 1

    # 마우스 입력 처리 함수
    def handle_mouse_input(self, event):
        x, y = event.pos[0] // (self.screen_width // self.grid_size), event.pos[1] // (self.screen_height // self.grid_size)
        if event.button == 1 and not self.flags[x][y]:  # 왼쪽 클릭 처리
            self.open_cell(x, y)
        elif event.button == 3 and not self.grid[x][y]:  # 오른쪽 클릭 처리
            self.toggle_flag(x, y)

    # 지정된 위치의 칸을 여는 함수
    def open_cell(self, x, y):
        if not self.grid[x][y]:
            self.grid[x][y] = 1
            if self.mines[x][y]:
                self.game_over = True
############################
#########PHASE2#############
############################
                self.start_explosion(x, y)
############################
#########PHASE2#############
############################
                self.scoreboard.apply_game_over_penalty()
            else:
                self.scoreboard.update_score_for_open_cell()
                if self.adjacent[x][y] == 0:
                    self.open_adjacent_cells(x, y)  # 인접한 칸 자동으로 열기
                self.check_victory()  # 승리 조건 확인

    # 지정된 위치의 인접 칸을 자동으로 여는 함수
    def open_adjacent_cells(self, x, y):
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size and not self.grid[nx][ny]:
                    self.open_cell(nx, ny)

    # 깃발 상태를 토글하는 함수
    def toggle_flag(self, x, y):
        if not self.grid[x][y]:
            self.flags[x][y] = not self.flags[x][y]
############################
#########PHASE2#############
############################
            self.scoreboard.update_score_for_flag(self.flags[x][y])  # 우클릭 사용시 점수 업데이트
            self.check_victory()  # 승리 조건 확인
############################
#########PHASE2#############
############################


############################
#########PHASE2#############
############################
    def start_explosion(self, x, y):
        self.exploding_cells = [(x, y)] # exploding_cells 에 현재 cell 추가.
        self.explosion_start_time = time.time() # exploding_start_time 설정.

    def update_explosion(self):
        if self.explosion_start_time:
            self.exploded_cells.extend(self.exploding_cells) # exploging 을 완료할 cell로 exploded_cells 업데이트
            new_cells = []
            for cell in self.exploding_cells: # exploded_cells 주변으로 exploding 전개
                cx, cy = cell
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        nx, ny = cx + dx, cy + dy
                        if (0 <= nx < self.grid_size and 0 <= ny < self.grid_size and 
                            (nx, ny) not in self.exploded_cells and (nx, ny) not in new_cells):
                            new_cells.append((nx, ny))
               
            self.exploding_cells = new_cells # exploding_cell 업데이트
            pygame.time.wait(200) # 0.2 초 간격으로 반복
            if not new_cells:
                self.explosion_start_time = None
############################
#########PHASE2#############
############################

    # 게임 보드 그리기 함수
    def draw_board(self):
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                rect = pygame.Rect(x * (self.screen_width // self.grid_size), y * (self.screen_height // self.grid_size),
                                   self.screen_width // self.grid_size, self.screen_height // self.grid_size)
                if self.grid[x][y] == 1:
                    if self.mines[x][y]:
                        pygame.draw.rect(self.screen, (255, 0, 0), rect)
                    else:
                        pygame.draw.rect(self.screen, (255, 255, 255), rect)
                        if self.adjacent[x][y] > 0:
                            label = self.font.render(str(self.adjacent[x][y]), True, (0, 0, 0))
                            self.screen.blit(label, rect.topleft)
                else:
                    pygame.draw.rect(self.screen, (160, 160, 160), rect)
                    if self.flags[x][y]:
                        pygame.draw.circle(self.screen, (0, 0, 255), (rect.centerx, rect.centery), 10)
############################
#########PHASE2#############
############################
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)  # 검은색 테두리 그리기
############################
#########PHASE2#############
############################

############################
#########PHASE2#############
############################

        for cell in self.exploding_cells:
            rect = pygame.Rect(cell[0] * (self.screen_width // self.grid_size), cell[1] * (self.screen_height // self.grid_size),
                               self.screen_width // self.grid_size, self.screen_height // self.grid_size)
            pygame.draw.rect(self.screen, (255, 0, 0), rect)
            pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)  # 검은색 테두리 그리기

        for cell in self.exploded_cells:
            rect = pygame.Rect(cell[0] * (self.screen_width // self.grid_size), cell[1] * (self.screen_height // self.grid_size),
                               self.screen_width // self.grid_size, self.screen_height // self.grid_size)
            pygame.draw.rect(self.screen, (0, 0, 0), rect)
        
############################
#########PHASE2#############
############################

        self.scoreboard.display_score()  # 실시간 점수 & 타이머 표시


        if self.game_over and not self.explosion_start_time:
            message = self.font.render("Game Over! Press Any Key To Restart.", True, (255, 255, 255))
            self.screen.blit(message, (self.screen_width / 2 - message.get_width() / 2, self.screen_height / 2))

        if self.victory:
            message = self.font.render("You Won! " + self.scoreboard.final_message(), True, (0, 255, 0))
            self.screen.blit(message, (self.screen_width / 2 - message.get_width() / 2, self.screen_height / 2))

    # 게임 실행 함수
    def run(self):
        while True:
            while not self.game_over and not self.victory:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        self.handle_mouse_input(event)
                self.screen.fill((0, 0, 0))
                self.draw_board()
                pygame.display.flip()
                self.clock.tick(30)

            ############################
            #########PHASE2#############
            ############################
            if self.game_over:
                while self.explosion_start_time is not None:
                    self.screen.fill((0, 0, 0))
                    self.update_explosion()
                    self.draw_board()
                    pygame.display.flip()
                    self.clock.tick(30)

                self.draw_board()
                pygame.display.flip()
                self.wait_for_key_press() # key 입력할 때까지 대기
                self.reset()
            ############################
            #########PHASE2#############
            ############################

            if self.victory:
                self.scoreboard.apply_victory_bonus(self.current_difficulty)  # 승리시 난이도별 보너스 점수 적용
                pygame.time.wait(5000)  # 승리시 5초 대기
                self.reset()  # 게임판 리셋

    
############################
#########PHASE2#############
############################
    def wait_for_key_press(self): # 키 입력 대기 함수
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    waiting = False
############################
#########PHASE2#############
############################

if __name__ == "__main__":
    game = Minesweeper()
    game.run()
