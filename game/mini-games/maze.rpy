init python:
    import pygame_sdl2 as pygame
    import random

    MAZE_BGM_PATH = "audio/zoumigong.mp3"
    SUCCESS_SFX_PATH = "audio/success.mp3"
    FAILURE_SFX_PATH = "audio/failure.mp3"

    def _maze_play_sfx_if_exists(path):
        if renpy.loadable(path):
            renpy.sound.play(path)

    def _maze_music_enter():
        """进入迷宫小游戏时切换 BGM，并记录进入前音乐。"""
        try:
            store._maze_prev_bgm = renpy.music.get_playing(channel="music")
        except Exception:
            store._maze_prev_bgm = None

        if renpy.loadable(MAZE_BGM_PATH):
            renpy.music.play(MAZE_BGM_PATH, channel="music", loop=True, fadein=0.5)

    def _maze_music_exit():
        """离开迷宫小游戏时恢复进入前 BGM（若无则停止 music）。"""
        prev = getattr(store, "_maze_prev_bgm", None)
        if prev:
            renpy.music.play(prev, channel="music", loop=True, fadein=0.5)
        else:
            renpy.music.stop(channel="music", fadeout=0.5)
    
    class MazeGame(renpy.Displayable):
        def __init__(self, cols=15, rows=10, cell_size=40, wall_thickness=4, **kwargs):
            super(MazeGame, self).__init__(**kwargs)
            self.cols = cols
            self.rows = rows
            self.cell_size = cell_size
            self.wall_thickness = wall_thickness
            
            # 记录画布大小
            self.width = cols * cell_size
            self.height = rows * cell_size
            
            self.init_maze()

        def init_maze(self):
            # 起点和终点坐标 (列, 行)
            self.start_cell = (0, 0)
            self.end_cell = (self.cols-1, self.rows-1)
            
            # 生成迷宫地图
            self.grid = self.generate_maze(self.cols, self.rows)
            
            # 找出死胡同 (只有一条路，即3面墙的格子)
            dead_ends = []
            for y in range(self.rows):
                for x in range(self.cols):
                    if sum(self.grid[y][x]) == 3:
                        if (x, y) != self.start_cell and (x, y) != self.end_cell:
                            dead_ends.append((x, y))
            
            # 在死胡同中随机放置家丁 (最多放6个)
            num_enemies = min(len(dead_ends), 6)
            self.enemies = random.sample(dead_ends, num_enemies)
            
            # 路径
            self.path = [self.start_cell]
            self.drawing = False

        def generate_maze(self, cols, rows):
            # 每个格子的墙：[上, 右, 下, 左], True 表示有墙
            grid = [[[True, True, True, True] for _ in range(cols)] for _ in range(rows)]
            visited = [[False for _ in range(cols)] for _ in range(rows)]
            
            # 深度优先搜索回溯算法生成随机迷宫
            stack = [(0, 0)]
            visited[0][0] = True
            
            dirs = [
                (0, -1, 0, 2), # 上 (dx=0, dy=-1，自身上墙壁下标0，对方下墙壁下标2)
                (1, 0, 1, 3),  # 右
                (0, 1, 2, 0),  # 下
                (-1, 0, 3, 1)  # 左
            ]
            
            while stack:
                curr_x, curr_y = stack[-1]
                unvisited_neighbors = []
                for dx, dy, w1, w2 in dirs:
                    nx, ny = curr_x + dx, curr_y + dy
                    if 0 <= nx < cols and 0 <= ny < rows and not visited[ny][nx]:
                        unvisited_neighbors.append((nx, ny, w1, w2))
                        
                if unvisited_neighbors:
                    nx, ny, w1, w2 = random.choice(unvisited_neighbors)
                    
                    # 打通墙壁
                    grid[curr_y][curr_x][w1] = False
                    grid[ny][nx][w2] = False
                    
                    visited[ny][nx] = True
                    stack.append((nx, ny))
                else:
                    stack.pop()
                    
            return grid

        def render(self, width, height, st, at):
            render = renpy.Render(self.width, self.height)
            canvas = render.canvas()
            
            # 画背景底色
            canvas.rect("#222222", (0, 0, self.width, self.height))
            
            # 画起点 (绿色) 和终点 (红色)
            sx, sy = self.start_cell
            canvas.rect("#4CAF50", (sx * self.cell_size, sy * self.cell_size, self.cell_size, self.cell_size))
            ex, ey = self.end_cell
            canvas.rect("#F44336", (ex * self.cell_size, ey * self.cell_size, self.cell_size, self.cell_size))
            
            # 画家丁敌人 (紫色方块)
            for ex, ey in self.enemies:
                e_size = self.cell_size // 2
                offset = self.cell_size // 4
                canvas.rect("#9C27B0", (ex * self.cell_size + offset, ey * self.cell_size + offset, e_size, e_size))
            
            # 画玩家的寻路路径 ("一笔画" 轨迹)
            cs = self.cell_size
            path_color = "#FFC107"
            
            if len(self.path) > 0:
                for x, y in self.path:
                    cx = x * cs + cs // 2
                    cy = y * cs + cs // 2
                    canvas.circle(path_color, (cx, cy), cs // 4)
                
                # 连接路径线段
                if len(self.path) > 1:
                    for i in range(len(self.path) - 1):
                        p1 = (self.path[i][0] * cs + cs // 2, self.path[i][1] * cs + cs // 2)
                        p2 = (self.path[i+1][0] * cs + cs // 2, self.path[i+1][1] * cs + cs // 2)
                        # 为了安全，这里调用参数传递最少的画线方法
                        canvas.line(path_color, p1, p2, max(2, cs // 5))

            # 画墙壁
            wall_color = "#FFFFFF"
            wt = self.wall_thickness
            for y in range(self.rows):
                for x in range(self.cols):
                    walls = self.grid[y][x]
                    px = x * cs
                    py = y * cs
                    if walls[0]: # Top
                        canvas.rect(wall_color, (px, py, cs, wt))
                    if walls[1]: # Right
                        canvas.rect(wall_color, (px + cs - wt, py, wt, cs))
                    if walls[2]: # Bottom
                        canvas.rect(wall_color, (px, py + cs - wt, cs, wt))
                    if walls[3]: # Left
                        canvas.rect(wall_color, (px, py, wt, cs))
                        
            return render

        def event(self, ev, x, y, st):
            # 将鼠标坐标映射到网格上
            grid_x = int(x // self.cell_size)
            grid_y = int(y // self.cell_size)
            
            # 判断是否移出迷宫范围
            if x < 0 or x >= self.width or y < 0 or y >= self.height:
                if self.drawing:
                    self.drawing = False
                return None
            
            # Ren'Py 鼠标事件，1代表左键
            if getattr(ev, 'type', None) == pygame.MOUSEBUTTONDOWN and getattr(ev, 'button', 0) == 1:
                # 只有点击当前的所在位置才能继续画
                if self.path and grid_x == self.path[-1][0] and grid_y == self.path[-1][1]:
                    self.drawing = True
                # 或者点击起点可以重新清空开始
                elif grid_x == self.start_cell[0] and grid_y == self.start_cell[1]:
                    self.path = [self.start_cell]
                    self.drawing = True
                    renpy.redraw(self, 0)
                    
            elif getattr(ev, 'type', None) == pygame.MOUSEBUTTONUP and getattr(ev, 'button', 0) == 1:
                self.drawing = False
                
            elif getattr(ev, 'type', None) == pygame.MOUSEMOTION:
                if self.drawing and self.path:
                    last_x, last_y = self.path[-1]
                    
                    # 鼠标移入了新的格子
                    if grid_x != last_x or grid_y != last_y:
                        # 检查是否是退后（回到上一个格子）
                        if len(self.path) >= 2 and grid_x == self.path[-2][0] and grid_y == self.path[-2][1]:
                            self.path.pop()
                            renpy.redraw(self, 0)
                        else:
                            # 检查是否严格相邻，且两者之间没有墙壁
                            dx = grid_x - last_x
                            dy = grid_y - last_y
                            if abs(dx) + abs(dy) == 1:
                                wall_index = -1
                                if dy == -1: wall_index = 0 # 向上走，要检查上面的墙
                                elif dx == 1: wall_index = 1 # 向右走，检查右边的墙
                                elif dy == 1: wall_index = 2 # 向下走，检查下面的墙
                                elif dx == -1: wall_index = 3 # 向左走，检查左边的墙
                                
                                # 如果墙是被打通的 (False)
                                if wall_index != -1 and not self.grid[last_y][last_x][wall_index]:
                                    self.path.append((grid_x, grid_y))
                                    
                                    # 检查是否撞到家丁敌人
                                    if (grid_x, grid_y) in self.enemies:
                                        _maze_play_sfx_if_exists(FAILURE_SFX_PATH)
                                        # 加 10 点 OOC 并通过 notify 提示玩家
                                        store.add_ooc(10)
                                        renpy.notify("撞见家丁了！OOC +10，迷宫已重置！")
                                        # 撞到敌人后重置迷宫并中断当前画线
                                        self.init_maze()
                                        renpy.redraw(self, 0)
                                        return None
                                        
                                    renpy.redraw(self, 0) # 触发重绘
                                    
                                    # 到达终点，返回 True
                                    if (grid_x, grid_y) == self.end_cell:
                                        self.drawing = False
                                        _maze_play_sfx_if_exists(SUCCESS_SFX_PATH)
                                        return True
            return None


screen maze_game():
    modal True
    zorder 100

    on "show" action Function(_maze_music_enter)
    on "hide" action Function(_maze_music_exit)
    
    # 遮罩背景
    add Solid("#000000CC")
    
    # 定义迷宫实例。15列 x 10行，每个格子50像素
    default maze = MazeGame(cols=15, rows=10, cell_size=50)
    
    # 迷宫显示区域
    frame:
        align (0.5, 0.5)
        padding (10, 10)
        background Solid("#333333")
        add maze
        
    text "从洪府（绿色块）开始按左键前行 (不能穿墙)\n到达红块（知府）。注意避开紫色块（家丁）！" align (0.5, 0.1) color "#FFF" text_align 0.5
        
    textbutton "重启并生成新迷宫":
        align (0.8, 0.9)
        # 用新对象覆盖以重置和刷新迷宫
        action SetScreenVariable("maze", MazeGame(cols=15, rows=10, cell_size=50))
        
    textbutton "跳过":
        align (0.95, 0.95)
        action Return(False)