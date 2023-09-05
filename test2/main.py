import os
import sys
import glob
import pygame
import tkinter
import os.path
from button import Button
from tkinter import filedialog

# 初始化
pygame.init()

# 设置宽, 高, 标题栏
WIDTH, HEIGHT = 1600, 900
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("相册播放器 | 小F 2022")


# 添加中文字体
def bold_font(size):
    os.chdir(sys.path[0])
    return pygame.font.Font("assets/simhei.ttf", size)


def regular_font(size):
    return pygame.font.SysFont("simhei", size)

# 设置文字背景色, 背景图片
BASE_TEXT_COLOR = "#6fffe9"
BACKGROUND_IMAGE = pygame.image.load("assets/background.png")
SCREEN.blit(BACKGROUND_IMAGE, (0, 0))
# 更新
pygame.display.update()

# 设置标题栏图标
WINDOW_ICON = pygame.image.load("assets/window_icon.png")
pygame.display.set_icon(WINDOW_ICON)

# 设置按钮背景色, 向后按钮, 暂停按钮, 播放按钮, 向前按钮, 加载新相册按钮
MAIN_MENU_BUTTON_BACKGROUND = pygame.image.load("assets/main_menu_button_bg.png")
REWIND_ICON_SURFACE = pygame.image.load("assets/rewind_icon.png")
PAUSE_ICON_SURFACE = pygame.image.load("assets/pause_icon.png")
PLAY_ICON_SURFACE = pygame.image.load("assets/play_icon.png")
SEEK_ICON_SURFACE = pygame.image.load("assets/seek_icon.png")
LOAD_NEW_ALBUM_SURFACE = pygame.image.load("assets/load_new_album_icon.png")


# 加载按钮函数
def load_button():
    # 打开文件管理器, 选择文件夹
    filedialogwindow = tkinter.Tk()
    filedialogwindow.withdraw()
    filepath = filedialog.askdirectory(title="选择你的相册")
    filedialogwindow.destroy()
    album_player(filepath)


# 关闭按钮
def quit_button():
    pygame.quit()
    sys.exit()


# 向后按钮
def rewind_button(current_image_index):
    if current_image_index > 0:
        current_image_index -= 1
    rewind_button_pressed = True
    return rewind_button_pressed, current_image_index


# 向前按钮
def seek_button(current_image_index, image_names):
    if current_image_index+1 < len(image_names):
        current_image_index += 1
    seek_button_pressed = True
    return seek_button_pressed, current_image_index


# 播放按钮
def play_button():
    paused = False
    unpaused = True
    return paused, unpaused


# 暂停按钮
def pause_button():
    paused = True
    unpaused = False
    return paused, unpaused


# 主界面
def main_menu():
    # 主页标题栏
    TITLE_TEXT_SURFACE = bold_font(120).render("相册播放器", True, BASE_TEXT_COLOR)
    TITLE_TEXT_RECT = TITLE_TEXT_SURFACE.get_rect(center=(WIDTH/2, 175))
    SCREEN.blit(TITLE_TEXT_SURFACE, TITLE_TEXT_RECT)
    # 加载按钮
    LOAD_BUTTON = Button(
        surface=MAIN_MENU_BUTTON_BACKGROUND, pos=(WIDTH/2, 415), text_input="加载",
        font=bold_font(100), base_color=BASE_TEXT_COLOR, hovering_color="white"
    )
    # 关闭按钮
    QUIT_BUTTON = Button(
        surface=MAIN_MENU_BUTTON_BACKGROUND, pos=(WIDTH/2, 585), text_input="关闭",
        font=bold_font(100), base_color=BASE_TEXT_COLOR, hovering_color="white"
    )
    while True:
        # 监听鼠标点击事件
        current_mouse_pos = pygame.mouse.get_pos()
        LOAD_BUTTON.update(SCREEN)
        QUIT_BUTTON.update(SCREEN)
        # 根据鼠标点击情况, 是否点击右上角的关闭
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # 根据鼠标点击情况, 点击加载或关闭按钮
            if event.type == pygame.MOUSEBUTTONDOWN:
                if LOAD_BUTTON.check_for_input(current_mouse_pos):
                    load_button()
                if QUIT_BUTTON.check_for_input(current_mouse_pos):
                    quit_button()

        # 当鼠标放置在按钮上, 按钮颜色发生改变
        LOAD_BUTTON.change_color(current_mouse_pos)
        QUIT_BUTTON.change_color(current_mouse_pos)
        pygame.display.update()


# 相册播放器功能函数
def album_player(folder_path):
    SCREEN.blit(BACKGROUND_IMAGE, (0, 0))

    image_file_paths = []
    image_names = []
    current_image_index = 0
    paused = False
    unpaused = False
    seek_button_pressed = False
    rewind_button_pressed = False

    # 添加加载按钮后, 得到的图片文件夹路径
    os.chdir(folder_path)
    for file in glob.glob("*"):
        current_image_path = f"{folder_path}/{file}"
        # 图片路径列表
        image_file_paths.append(current_image_path)
        # 图片名称列表
        image_names.append(file)

    # 向后按钮
    REWIND_BUTTON = Button(
        surface=REWIND_ICON_SURFACE, pos=(WIDTH/2-100, HEIGHT-150), text_input="",
        font=bold_font(100), base_color=BASE_TEXT_COLOR, hovering_color="white"
    )
    # 暂停按钮
    PAUSE_BUTTON = Button(
        surface=PAUSE_ICON_SURFACE, pos=(WIDTH/2, HEIGHT-150), text_input="",
        font=bold_font(100), base_color=BASE_TEXT_COLOR, hovering_color="white"
    )
    # 播放按钮
    PLAY_BUTTON = Button(
        surface=PLAY_ICON_SURFACE, pos=(WIDTH/2, HEIGHT-150), text_input="",
        font=bold_font(100), base_color=BASE_TEXT_COLOR, hovering_color="white"
    )
    # 向前按钮
    SEEK_BUTTON = Button(
        surface=SEEK_ICON_SURFACE, pos=(WIDTH/2+100, HEIGHT-150), text_input="",
        font=bold_font(100), base_color=BASE_TEXT_COLOR, hovering_color="white"
    )
    # 加载新相册按钮
    LOAD_NEW_ALBUM_BUTTON = Button(
        surface=LOAD_NEW_ALBUM_SURFACE, pos=(WIDTH-325, HEIGHT-150), text_input="",
        font=bold_font(100), base_color=BASE_TEXT_COLOR, hovering_color="white"
    )

    # 获取时间, 设置每5s切换一张图片
    previous_time = pygame.time.get_ticks()
    COOLDOWN = 5000

    # 设置图片名称文字属性
    photo_title_text_surface = bold_font(90).render(image_names[current_image_index], True, BASE_TEXT_COLOR)
    photo_title_text_rect = photo_title_text_surface.get_rect(center=(WIDTH/2, 150))

    # 图片张图显示
    image_count_text_surface = regular_font(80).render(f"图片 {current_image_index+1}/{len(image_names)}", True, BASE_TEXT_COLOR)
    image_count_text_rect = image_count_text_surface.get_rect(center=(300, 755))

    # 获取图片宽高属性, 窗口显示不合适, 调整大小
    new_image_surface = pygame.image.load(image_file_paths[current_image_index])
    if new_image_surface.get_height() > 500:
        new_image_surface = pygame.transform.scale(new_image_surface, (new_image_surface.get_width() * (500/new_image_surface.get_height()), 500))
    elif new_image_surface.get_width() > 800:
        new_image_surface = pygame.transform.scale(new_image_surface, (800, new_image_surface.get_height() * (800/new_image_surface.get_width())))
    new_image_rect = new_image_surface.get_rect(center=(WIDTH/2, HEIGHT/2))

    SCREEN.blit(new_image_surface, new_image_rect)
    SCREEN.blit(photo_title_text_surface, photo_title_text_rect)
    SCREEN.blit(image_count_text_surface, image_count_text_rect)

    REWIND_BUTTON.update(SCREEN)
    PAUSE_BUTTON.update(SCREEN)
    SEEK_BUTTON.update(SCREEN)
    LOAD_NEW_ALBUM_BUTTON.update(SCREEN)

    pygame.display.update()

    # 监听鼠标点击事件
    while True:
        for event in pygame.event.get():
            # 根据鼠标点击情况, 是否点击右上角的关闭
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 根据鼠标点击情况, 做向前, 向后, 暂停, 开始等切换图片操作
                current_mouse_pos = pygame.mouse.get_pos()
                if REWIND_BUTTON.check_for_input(current_mouse_pos):
                    rewind_button_pressed, current_image_index = rewind_button(current_image_index)
                if SEEK_BUTTON.check_for_input(current_mouse_pos):
                    seek_button_pressed, current_image_index = seek_button(current_image_index, image_names)
                if paused:
                    if PLAY_BUTTON.check_for_input(current_mouse_pos):
                        paused, unpaused = play_button()
                else:
                    if PAUSE_BUTTON.check_for_input(current_mouse_pos):
                        paused, unpaused = pause_button()
                if LOAD_NEW_ALBUM_BUTTON.check_for_input(current_mouse_pos):
                    load_button()

        current_time = pygame.time.get_ticks()

        # 切换图片, 一定时间、点击向后按钮、点击向前按钮、点击开始按钮
        if current_time - previous_time >= COOLDOWN or rewind_button_pressed or seek_button_pressed or paused or unpaused:
            unpaused = False
            if current_image_index < len(image_file_paths)-1 and not seek_button_pressed and not rewind_button_pressed and not paused:
                current_image_index += 1

            SCREEN.blit(BACKGROUND_IMAGE, (0, 0))
            REWIND_BUTTON.update(SCREEN)
            if paused:
                PLAY_BUTTON.update(SCREEN)
            else:
                PAUSE_BUTTON.update(SCREEN)
            SEEK_BUTTON.update(SCREEN)
            LOAD_NEW_ALBUM_BUTTON.update(SCREEN)

            new_image_surface = pygame.image.load(image_file_paths[current_image_index])
            if new_image_surface.get_height() > 500:
                new_image_surface = pygame.transform.scale(new_image_surface, (new_image_surface.get_width() * (500/new_image_surface.get_height()), 500))
            elif new_image_surface.get_width() > 800:
                new_image_surface = pygame.transform.scale(new_image_surface, (800, new_image_surface.get_height() * (800/new_image_surface.get_width())))
            new_image_rect = new_image_surface.get_rect(center=(WIDTH/2, HEIGHT/2))

            SCREEN.blit(new_image_surface, new_image_rect)

            photo_title_text_surface = bold_font(90).render(image_names[current_image_index], True, BASE_TEXT_COLOR)
            photo_title_text_rect = photo_title_text_surface.get_rect(center=(WIDTH/2, 150))

            SCREEN.blit(photo_title_text_surface, photo_title_text_rect)

            image_count_text_surface = regular_font(80).render(f"图片 {current_image_index+1}/{len(image_names)}", True, BASE_TEXT_COLOR)
            image_count_text_rect = image_count_text_surface.get_rect(center=(300, 755))

            SCREEN.blit(image_count_text_surface, image_count_text_rect)

            pygame.display.update()
            previous_time = pygame.time.get_ticks()
            seek_button_pressed = False
            rewind_button_pressed = False

# 主程序
main_menu()