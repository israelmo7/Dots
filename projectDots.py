"""
Project    | Dots
Written by | Israel Moshe
Date       | 5.11.26
Framework  | Data science course, Analiza campus
"""
import sys #argv, exit
import random #random, choice
######
"""---------------------------    Globals   ---------------------------"""
######
BOARD_SIZE = 8
EXIT_CODE = 999
game_state = {'current_color': None, 'dots': 0, 'dots_temp':0}
colors = {'B': [], 'P': []}
colors_pos = {'B': [], 'P': []}
GREEN_A = "\033[92m"
BLUE_A = "\033[94m"
RESET_A = "\033[0m"
debug_mode = False
######
"""---------------------------    PyGame Globals  ---------------------------"""
to_keep_going = False
DOT_SIZE = 50
# גודל קבוע ונוח למסכי הפתיחה והסיום (למשל 450x450)
MENU_WINDOW_SIZE = 450 
WINDOW_SIZE = DOT_SIZE * BOARD_SIZE
NUMBER_OF_COLORS = 1

colors_p = {'B': (0, 0, 255), 'R': (231, 76, 60), 'P': (128, 0, 128), 'Y':(255, 255, 0)}
colors_p |= {'b': (200, 220, 255), 'r': (255, 200, 200), 'p': (230, 210, 250), 'y':(255, 255, 220)}
WHITE_R = (255, 255, 255)
GRAY_R = (200, 200, 200)
BLACK_R = (0, 0, 0)
######
"""---------------------------    Lambdas   ---------------------------"""
######
#IN: dict   OUT: bool
is_valid_type = lambda i, t: bool(i is not None and type(i) == t and len(i) > 0)
#IN: list, list   OUT: bool
is_it_in_range = lambda val, sizes: bool(sizes[0] > val[0] >= 0 and sizes[1] > val[1] >= 0)
#IN: tuple(int,int), tuple(int,int)   OUT: bool
is_they_touch = lambda a, b: bool((abs(a[0] - b[0]) == 1)) ^ bool(abs(a[1] - b[1]) == 1)
######

"""---------------------------    Functions   ---------------------------"""
"""
Print Debug: prints only when 'debug_mode' is TRUE.
   INPUT:
       msg - the string to print
   OUTPUT:
       NONE
"""
def printd(msg):
    if debug_mode:
        print(msg)

"""
Set Board Auto: set colors points on board auto.
    INPUT:
        board - the board; 2d list
    OUTPUT:
        board - the new.

"""
def set_board_ready_adv(board):
    """
    Always works: snake covers every cell, then split into NUMBER_OF_COLORS paths.
    Only endpoints are placed on the board.
    """
    global game_state, colors, colors_pos

    n = NUMBER_OF_COLORS
    total = BOARD_SIZE * BOARD_SIZE
    base_colors = [c for c in colors_p if c.isupper()]

    # random colors from the real (uppercase) list
    palette = random.sample(base_colors, n)

    # --- full snake path (every cell once, each step orthogonal) ---
    path = []
    for r in range(BOARD_SIZE):
        if r % 2 == 0:
            cols = range(BOARD_SIZE)
        else:
            cols = range(BOARD_SIZE - 1, -1, -1)
        for c in cols:
            path.append((r, c))

    if random.random() < 0.5:
        path.reverse()

    # --- split into exactly n segments (1 color = whole path, easiest) ---
    sizes = [total // n] * n
    for i in range(total % n):
        sizes[i] += 1

    segments = []
    idx = 0
    for sz in sizes:
        segments.append(path[idx:idx + sz])
        idx += sz

    # --- reset state & place only endpoints ---
    game_state = {'current_color': None, 'dots': 0, 'dots_temp': 0}
    colors = {color: [] for color in palette}
    colors_pos = {}

    for color, seg in zip(palette, segments):
        start, end = seg[0], seg[-1]
        colors_pos[color] = [start, end]
        board[start[0]][start[1]] = color
        board[end[0]][end[1]] = color
        game_state['dots'] += 2

    return board
"""
Init Pygame: screen, settings and enviroment.
   INPUT:
       initial_size - int; the dimension for the window width and height
   OUTPUT:
       screen - pygame object for the program screen.
       clock - pygame object for timing.
"""
def init_pygame(initial_size):
    # אתחול הספרייה
    pygame.init()

    # הגדרת מאפייני החלון לפי הגודל שקיבלנו
    screen = pygame.display.set_mode((initial_size, initial_size))
    pygame.display.set_caption("Dots")

    # שעון לשליטה בקצב הפריימים (FPS)
    clock = pygame.time.Clock()

    return screen, clock
"""
Get New Board: returns totally empty board. clean old data.
   INPUT:
       int - the size of the ROWS & COLUMNS
   OUTPUT:
       board - 2d list size of <int>
"""
def get_new_board(board_size):
    global game_state, colors
    game_state = {'current_color': None, 'dots': 0, 'dots_temp':0}
    for i in colors.keys():
        colors[i] = [] 
    board = []

    for i in range(board_size):
        board.append([' '] * board_size)
    return board
"""
Show Board: prints the current table to screen.
   INPUT:
       board - 2d list<str>
   OUTPUT:
       None
"""
def show_board(board):
    print("-" * BOARD_SIZE * 4)

    for i in board:
        print('|', end=' ')
        for j in i:
           if j[0].lower() == 'b': print(BLUE_A, end='')
           print(j + RESET_A, end=' | ')
        print("\n" + "-" * BOARD_SIZE * 4)
"""
Set Board: set board's starting values.
   INPUT:
       board - 2d list<str>
   OUTPUT:
        board - the new board.
"""      
def set_board_ready(board):
    global game_state, colors_pos
#########
    game_state['dots'] += 2

    board[0][1] = list(colors.keys())[0]
    board[-1][-1] = list(colors.keys())[0]
    colors_pos[list(colors.keys())[0]] = [(0, 1), (BOARD_SIZE - 1, BOARD_SIZE - 1)]
#########
    game_state['dots'] += 2
    
    board[0][0] = list(colors.keys())[1]
    board[-1][-2] = list(colors.keys())[1]
    colors_pos[list(colors.keys())[1]] = [(0, 0), (BOARD_SIZE - 1, BOARD_SIZE - 2)]
#########

    return board
"""
Get Current Dot: returns the color of the current building line.
   INPUT:
       board - 2d list<str>
   OUTPUT:
       str - the color; None if nothing.
"""   
def get_current_dot(board):

    result = bool(game_state['current_color'] is not None)
    result = result and is_valid_type(colors[game_state['current_color']], list)

    return game_state['current_color'] if result else None 
"""
The Function checks if the next move ove the player is valid, by rules:

    INPUT:
        board - the board itself; 2d list
        next_move - tuple of 2 INT; the [i][j] on board
    OUTPUT:
        int - [1: first dot |2: regular movement |3: finishing move |0: fail]

"""
#STATUS CODES for the movement actions#
ERROR = 0
FIRST = 1
MID = 2
LAST = 3
REPEAT = 4
CLEAR = 5
LOOPED = 6
def is_valid_move(board, next_move):

    #Check for same position
    if is_valid_type(game_state['current_color'], str) and \
        next_move == colors[game_state['current_color']][-1]:
        return REPEAT
    #Global Validation
    if not is_valid_type(board, list): 
        printd(f"Error: Problems with <board>")
        return ERROR
    #Out of range Validation
    printd(type(next_move))
    if not is_it_in_range(next_move, [len(board), len(board[0])]):
        printd(f"Error: {next_move} is out of range ({len(board)},{len(board[0])})")
        return ERROR

    #Check for current position existence.
    next_value = board[next_move[0]][next_move[1]]
    current_value = get_current_dot(board)
    if current_value != None:
        #Touching squares Validation
        if not is_they_touch(next_move, colors[game_state['current_color']][-1]):
            printd(f"Error: {next_move} isnt touching {colors[game_state['current_color']][-1]}")
            return ERROR
        elif current_value.lower() == next_value:
            return LOOPED
    #Here it means or 1) they touching 2) first dot.
    elif next_value in colors.keys():
        return FIRST if colors[next_value] == [] else CLEAR
    else:
        printd(get_current_dot(board))
        return ERROR                    #random touch
    
    ######################__Touching and not first time__######################
    
    if next_value in colors.keys():
        if current_value != next_value:
            printd("Error: different base colors")
            return ERROR
        elif colors[next_value][0] == next_move:
            printd("Error: tried to loop into same root")
            return ERROR
    elif len(next_value) == 2:
        printd("Error: tried to pass through finished line")
        return REPEAT
    
    return LAST if next_value in colors.keys() else MID
"""
The Function checks if all the dots are filled

    INPUT:
        NONE
    OUTPUT:
        bool - True for win.

"""
def check_for_win():
    result = False
    if game_state['dots'] == BOARD_SIZE ** 2:
        for color, pos in colors.items():
            if colors_pos[color][0] not in pos or colors_pos[color][1] not in pos:
                return False
        result = True
    return result
"""
The Function removes sapareted dots by color base/trail.

    INPUT:
        board - the board itself; 2d list
        color - str; to remove.
    OUTPUT:
        board - the new board.

"""
def remove_cutted_dots(board, color):
    is_cut = False
    color = color[0].lower()
    pos = colors[color.upper()]

    pos = pos[1:-1:] if pos[-1] in colors_pos[color.upper()] and pos[0] in colors_pos[color.upper()] else pos[1::]

    for i, j in pos:
        if is_cut:
            if len(board[i][j]) == 2: game_state['dots'] -= 1
            else: game_state['dots_temp'] -= 1
            board[i][j] = ' '
        elif board[i][j][0] != color:
            if len(board[i][j]) == 2: game_state['dots'] -= 1
            else: game_state['dots_temp'] -= 1
            is_cut = True
    return board
"""
The Function Makes a move over the board.
    INPUT:
        board - the board itself; 2d list
        dest - tuple of 2 ints; the move to do.
    OUTPUT:
        board - the new board.

"""
def make_a_move(board, dest):

    global game_state, colors, to_keep_going

    answer = is_valid_move(board, dest)
    to_keep_going = False

    if answer == FIRST: #first dot
        game_state['current_color'] = board[dest[0]][dest[1]]
        colors[game_state['current_color']] = [(dest[0], dest[1])]#
        to_keep_going = True
    elif answer == MID: # second dot
        to_keep_going = True
        old = board[dest[0]][dest[1]]
        game_state['dots_temp'] += 1
        board[dest[0]][dest[1]] = get_current_dot(board).lower()
        colors[game_state['current_color']].append(tuple(dest))
        printd(f"$ {colors[game_state['current_color']]}")
        if old != ' ': board = remove_cutted_dots(board, old)

    elif answer == LAST: # last dot
        board, _ = change_color(board, get_current_dot(board).lower())
        colors[get_current_dot(board)].append(dest)
        game_state['dots'] += game_state['dots_temp']
        game_state['dots_temp'] = 0
        game_state['current_color'] = None

    elif answer == REPEAT: #same position
        to_keep_going = True
        board = board

    elif answer == CLEAR:
        sign = board[dest[0]][dest[1]]
        cnt = 0
        board, cnt = change_color(board, sign.lower() * 2, ' ')
        game_state['dots'] -= cnt
        colors[sign] = [(dest[0], dest[1])]
        game_state['current_color'] = sign
        to_keep_going = True
    elif answer == LOOPED:
        cut_index = list(colors[get_current_dot(board)]).index(dest) + 1
        to_cut = colors[get_current_dot(board)][cut_index]
        board[to_cut[0]][to_cut[1]] = ' '
        board = remove_cutted_dots(board, board[dest[0]][dest[1]])
        colors[get_current_dot(board)] = colors[get_current_dot(board)][:cut_index:1]
        to_keep_going = True
    elif game_state['dots_temp'] > 0: #Mismatch
        board, _ = change_color(board, get_current_dot(board).lower(), ' ')
        colors[game_state['current_color']] = []
        game_state['dots_temp'] = 0
        game_state['current_color'] = None


    return board
"""
The Function deleted full color.
    INPUT:
        board - the board itself; 2d list
        from_c - old color to change.
        to_c - new color to set.
    OUTPUT:
        board - the new board.

"""
def change_color(board, from_c, to_c = True):

    to_c = str(from_c * 2 if type(to_c) == bool else to_c)
    cnt = 0
    pos = colors[from_c[0].upper()]
    printd(pos[1::])
    for i,j in pos[1::]:
        if from_c == board[i][j]:
            board[i][j] = to_c
            cnt += 1

    printd(f"Deleted {cnt} Dots")
    return board, cnt     
"""
The Function Starts loop game.
    INPUT:
        board - the board itself; 2d list
    OUTPUT:
        bool - True for Win;

"""
def gameplay(board):

    while board and not check_for_win():
        show_board(board)
        to_move = (int(input("I: ")), int(input("J: ")))

        board = None if (-1 in to_move) else make_a_move(board, to_move)

    return True if board else False
"""
The Function converts 2d array coordinates to screen coordinates.
    INPUT:
        pos - tuple of 2
    OUTPUT:
        pos - tuple of 2
"""
def index_to_screen(pos):
    final = [0, 0]

    if pos[0] > 0:
        final[0] = (pos[0] - 1) * DOT_SIZE + DOT_SIZE

    if pos[1] > 0:
        final[1] = (pos[1] - 1) * DOT_SIZE + DOT_SIZE

    return (final[0] + DOT_SIZE// 2, final[1] + DOT_SIZE // 2)
"""
The Function shows the starting window for pygame.
    INPUT:
        screen - pygame object for the game window.
    OUTPUT:
        NONE
"""
def starting_screen(screen):

    def show_help_screen(screen):
        title_font = pygame.font.SysFont("Arial", 40, bold=True)
        text_font = pygame.font.SysFont("Arial", 22, bold= True)
        rules = [
            "רבסה",
            "",
            "עבצה ותואב תודוקנ יתש ןיב וק חותמל",
            "ךסמה לכ תא אלמל",
            "",
            "הרזחל םוקמ לכב ץחל",
        ]

        waiting = True
        while waiting:
            screen.fill(WHITE_R)
            y = MENU_WINDOW_SIZE // 4
            for i, line in enumerate(rules):
                font = title_font if i == 0 else text_font
                color = (50, 50, 50) if i == 0 else (90, 90, 90)
                surf = font.render(line, True, color)
                screen.blit(surf, (MENU_WINDOW_SIZE // 2 - surf.get_width() // 2, y))
                y += 45
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                    waiting = False

    global BOARD_SIZE, NUMBER_OF_COLORS  # הוסף כאן את המשתנה החדש אם הוא גלובלי
    title_font = pygame.font.SysFont("Arial", 50, bold=True)
    text_font = pygame.font.SysFont("Arial", 22)
    btn_font = pygame.font.SysFont("Arial", 36, bold=True)
    
    waiting = True
    while waiting:
        screen.fill(WHITE_R)
        
        center = MENU_WINDOW_SIZE // 2
        
        # כותרת למעלה
        title_surf = title_font.render("תודוקנ", True, (50, 50, 50))
        screen.blit(title_surf, (center - title_surf.get_width() // 2, MENU_WINDOW_SIZE // 6))

        # --- שורה ראשונה: בחירת גודל לוח (Board Size) ---
        y1 = MENU_WINDOW_SIZE // 2 - 50
        left_btn_1 = pygame.Rect(center - 110, y1, 40, 40)
        box_rect_1 = pygame.Rect(center - 65, y1, 130, 40)
        right_btn_1 = pygame.Rect(center + 70, y1, 40, 40)

        pygame.draw.rect(screen, (220, 220, 220), left_btn_1, border_radius=6)
        pygame.draw.rect(screen, (240, 240, 240), box_rect_1, border_radius=6)
        pygame.draw.rect(screen, (220, 220, 220), right_btn_1, border_radius=6)
        
        left_text_1 = btn_font.render("<", True, (50, 50, 50))
        val_text_1 = text_font.render(f"לדוג: {BOARD_SIZE}x{BOARD_SIZE}", True, (50, 50, 50))
        right_text_1 = btn_font.render(">", True, (50, 50, 50))
        
        screen.blit(left_text_1, (left_btn_1.centerx - left_text_1.get_width() // 2, left_btn_1.centery - left_text_1.get_height() // 2))
        screen.blit(val_text_1, (box_rect_1.centerx - val_text_1.get_width() // 2, box_rect_1.centery - val_text_1.get_height() // 2))
        screen.blit(right_text_1, (right_btn_1.centerx - right_text_1.get_width() // 2, right_btn_1.centery - right_text_1.get_height() // 2))

        # --- שורה שנייה: משתנה נוסף (למשל Difficulty / Mode) ---
        y2 = MENU_WINDOW_SIZE // 2 + 10
        left_btn_2 = pygame.Rect(center - 110, y2, 40, 40)
        box_rect_2 = pygame.Rect(center - 65, y2, 130, 40)
        right_btn_2 = pygame.Rect(center + 70, y2, 40, 40)

        pygame.draw.rect(screen, (220, 220, 220), left_btn_2, border_radius=6)
        pygame.draw.rect(screen, (240, 240, 240), box_rect_2, border_radius=6)
        pygame.draw.rect(screen, (220, 220, 220), right_btn_2, border_radius=6)
        
        left_text_2 = btn_font.render("<", True, (50, 50, 50))
        val_text_2 = text_font.render(f"םיעבצ: {NUMBER_OF_COLORS}", True, (50, 50, 50))
        right_text_2 = btn_font.render(">", True, (50, 50, 50))
        
        screen.blit(left_text_2, (left_btn_2.centerx - left_text_2.get_width() // 2, left_btn_2.centery - left_text_2.get_height() // 2))
        screen.blit(val_text_2, (box_rect_2.centerx - val_text_2.get_width() // 2, box_rect_2.centery - val_text_2.get_height() // 2))
        screen.blit(right_text_2, (right_btn_2.centerx - right_text_2.get_width() // 2, right_btn_2.centery - right_text_2.get_height() // 2))

        # --- כפתור התחלה בתחתית ---
        start_btn_rect = pygame.Rect(center - 100, MENU_WINDOW_SIZE // 2 + 75, 200, 45)
        pygame.draw.rect(screen, (46, 204, 113), start_btn_rect, border_radius=8)
        start_text = text_font.render("קחשמ לחתה", True, (255, 255, 255))
        screen.blit(start_text, (start_btn_rect.centerx - start_text.get_width() // 2, start_btn_rect.centery - start_text.get_height() // 2))

        # after start button draw:
        help_btn_rect = pygame.Rect(center - 100, MENU_WINDOW_SIZE // 2 + 130, 200, 40)
        pygame.draw.rect(screen, (52, 152, 219), help_btn_rect, border_radius=8)
        help_text = text_font.render("הרזע", True, (255, 255, 255))
        screen.blit(help_text, (help_btn_rect.centerx - help_text.get_width() // 2,
        help_btn_rect.centery - help_text.get_height() // 2))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                if left_btn_1.collidepoint(mouse_pos):
                    if BOARD_SIZE > 5:
                        BOARD_SIZE -= 1
                elif right_btn_1.collidepoint(mouse_pos):
                    if BOARD_SIZE < 10:
                        BOARD_SIZE += 1
                        
                elif left_btn_2.collidepoint(mouse_pos):
                    if NUMBER_OF_COLORS > 1:
                        NUMBER_OF_COLORS -= 1
                elif right_btn_2.collidepoint(mouse_pos):
                    if NUMBER_OF_COLORS < 4: 
                        NUMBER_OF_COLORS += 1

                elif help_btn_rect.collidepoint(mouse_pos):
                    show_help_screen(screen)        
                elif start_btn_rect.collidepoint(mouse_pos):
                    waiting = False
                
"""
The Function shows the ending window for pygame.
    INPUT:
        screen - pygame object for the game window.
        won - bool; if win or not.
    OUTPUT:
        NONE
"""
def ending_screen(screen, won):
    title_font = pygame.font.SysFont("Arial", 50, bold=True)
    instruction_font = pygame.font.SysFont("Arial", 22)
    small_font = pygame.font.SysFont("Arial", 13)

    waiting = True
    while waiting:
        screen.fill(WHITE_R)
        
        if won:
            msg = "ןוחצינ"
            msg_color = (46, 204, 113)
        else:
            msg = "רמגנ קחשמ"
            msg_color = (231, 76, 60)
            
        title_surf = title_font.render(msg, True, msg_color)
        inst_surf = instruction_font.render("תאצל ידכ ץחל", True, (100, 100, 100))
        git_surf = small_font.render("github.com/israelmo7", True, (120, 120, 120))

        # שימוש ב-MENU_WINDOW_SIZE כדי שהטקסט ימורכז יפה גם במסך הסיום הקבוע
        screen.blit(title_surf, (MENU_WINDOW_SIZE // 2 - title_surf.get_width() // 2, MENU_WINDOW_SIZE // 3))
        screen.blit(inst_surf, (MENU_WINDOW_SIZE // 2 - inst_surf.get_width() // 2, MENU_WINDOW_SIZE // 2))
        screen.blit(git_surf, (MENU_WINDOW_SIZE // 2 - git_surf.get_width() // 2, MENU_WINDOW_SIZE // 2 + 50))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False

"""
The Function Starts loop game with pygame.
    INPUT:
        board - the board itself; 2d list
    OUTPUT:
        bool - True for Win;
"""
def run_with_pygame(board, clock, screen):

    is_dragging = False
    while board and not check_for_win():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                board = None

            elif event.type == pygame.MOUSEBUTTONDOWN:
                is_dragging = True
            elif event.type == pygame.MOUSEMOTION and is_dragging:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                mouse_x //= DOT_SIZE
                mouse_y //= DOT_SIZE
                board = make_a_move(board, (mouse_x, mouse_y))
                is_dragging = to_keep_going

            elif event.type == pygame.MOUSEBUTTONUP:
                is_dragging = False

        screen.fill(WHITE_R) # Background
        for i in range(BOARD_SIZE):
            dot_size = DOT_SIZE * i
            pygame.draw.line(screen, GRAY_R, (dot_size, 0), (dot_size, WINDOW_SIZE), 5)
            pygame.draw.line(screen, GRAY_R, (0, dot_size), (WINDOW_SIZE, dot_size), 5)

        if board:
            for color, (i, j) in colors_pos.items():
                pygame.draw.circle(screen, colors_p[color], index_to_screen(i), (DOT_SIZE // 2) - 5)
                pygame.draw.circle(screen, colors_p[color], index_to_screen(j), (DOT_SIZE // 2) - 5)
                
        for i in colors.keys():
            if is_valid_type(colors[i], list) and len(colors[i]) > 1:
                for x in range(1, len(colors[i])): 
                    pygame.draw.line(screen, colors_p[i], index_to_screen((colors[i][x - 1][0], colors[i][x - 1][1])), \
                                     index_to_screen((colors[i][x][0], colors[i][x][1])), DOT_SIZE // 2)

        pygame.display.flip()
        clock.tick(60)

    return board != None
"""----------------------------------------    MAIN   ----------------------------------------"""
def main(mode = ''):
    global BOARD_SIZE, WINDOW_SIZE
    screen, clock = None, None
    
    if mode == 'G':
        screen, clock = init_pygame(MENU_WINDOW_SIZE)
        starting_screen(screen)

        WINDOW_SIZE = DOT_SIZE * BOARD_SIZE
        screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))

        board = get_new_board(BOARD_SIZE)
        board = set_board_ready_adv(board)

        won = run_with_pygame(board, clock, screen)   # play on game-sized window

        screen = pygame.display.set_mode((MENU_WINDOW_SIZE, MENU_WINDOW_SIZE))
        ending_screen(screen, won)
        pygame.quit()

    else:
        board = get_new_board(BOARD_SIZE)
        board = set_board_ready(board)
        print("The Player " + "Won!" if gameplay(board) else 'Stopped the game!')

if __name__ == '__main__':
    args = sys.argv
    if len(args) == 1:
        import pygame; main('G')
    elif len(args) == 2 :
        if args[1] == 'G': import pygame; main(args[1])
        elif args[1] == 'd': debug_mode = True; main(args[1])
        else: print(f"Usage: Python3 {args[0]} (Opotional: d => for debug mode; G => for pygame mode)")
    else: print(f"Usage: Python3 {args[0]} (Opotional: d => for debug mode; G => for pygame mode)")