# A simple Album player
# After loading the directory of Album, it will display every photo for three seconds if there is no operation

import os
import sys
import glob
import pygame
import tkinter
import os.path
from button import Button
from tkinter import filedialog

# Initialization
pygame.init()

# set width, heigh and caption
WIDTH, HEIGHT = 1600, 900
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Album Player")


# Add font
def bold_font(size):
    os.chdir(sys.path[0])
    return pygame.font.Font("assets/simhei.ttf", size)


def regular_font(size):
    return pygame.font.SysFont("simhei", size)

# Set background
BASE_TEXT_COLOR = "#6fffe9"
BACKGROUND_IMAGE = pygame.image.load("assets/background.png")
SCREEN.blit(BACKGROUND_IMAGE, (0, 0))
# update
pygame.display.update()

# set icon
WINDOW_ICON = pygame.image.load("assets/window_icon.png")
pygame.display.set_icon(WINDOW_ICON)

# Set button background color, back button, pause button, play button, forward button, load new album button
MAIN_MENU_BUTTON_BACKGROUND = pygame.image.load("assets/main_menu_button_bg.png")
REWIND_ICON_SURFACE = pygame.image.load("assets/rewind_icon.png")
PAUSE_ICON_SURFACE = pygame.image.load("assets/pause_icon.png")
PLAY_ICON_SURFACE = pygame.image.load("assets/play_icon.png")
SEEK_ICON_SURFACE = pygame.image.load("assets/seek_icon.png")
LOAD_NEW_ALBUM_SURFACE = pygame.image.load("assets/load_new_album_icon.png")


# function for load botton
def load_button():    
    filedialogwindow = tkinter.Tk()
    filedialogwindow.withdraw()
    filepath = filedialog.askdirectory(title="Select Your Album")
    filedialogwindow.destroy()
    album_player(filepath)


# function for quit botton
def quit_button():
    pygame.quit()
    sys.exit()


# function for backward botton
def rewind_button(current_image_index):
    if current_image_index > 0:
        current_image_index -= 1
    rewind_button_pressed = True
    return rewind_button_pressed, current_image_index


# function for forward botton
def seek_button(current_image_index, image_names):
    if current_image_index+1 < len(image_names):
        current_image_index += 1
    seek_button_pressed = True
    return seek_button_pressed, current_image_index


# function for play botton
def play_button():
    paused = False
    unpaused = True
    return paused, unpaused


# function for pause botton
def pause_button():
    paused = True
    unpaused = False
    return paused, unpaused


# Main menu
def main_menu():
    TITLE_TEXT_SURFACE = bold_font(120).render("Album Player", True, BASE_TEXT_COLOR)
    TITLE_TEXT_RECT = TITLE_TEXT_SURFACE.get_rect(center=(WIDTH/2, 175))
    SCREEN.blit(TITLE_TEXT_SURFACE, TITLE_TEXT_RECT)
 
    LOAD_BUTTON = Button(
        surface=MAIN_MENU_BUTTON_BACKGROUND, pos=(WIDTH/2, 415), text_input="Load",
        font=bold_font(100), base_color=BASE_TEXT_COLOR, hovering_color="white"
    )

    QUIT_BUTTON = Button(
        surface=MAIN_MENU_BUTTON_BACKGROUND, pos=(WIDTH/2, 585), text_input="Close",
        font=bold_font(100), base_color=BASE_TEXT_COLOR, hovering_color="white"
    )
    while True:
        # Listen to cursor event
        current_mouse_pos = pygame.mouse.get_pos()
        LOAD_BUTTON.update(SCREEN)
        QUIT_BUTTON.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if LOAD_BUTTON.check_for_input(current_mouse_pos):
                    load_button()
                if QUIT_BUTTON.check_for_input(current_mouse_pos):
                    quit_button()

        LOAD_BUTTON.change_color(current_mouse_pos)
        QUIT_BUTTON.change_color(current_mouse_pos)
        pygame.display.update()


# function for album player
def album_player(folder_path):
    SCREEN.blit(BACKGROUND_IMAGE, (0, 0))

    image_file_paths = []
    image_names = []
    current_image_index = 0
    paused = False
    unpaused = False
    seek_button_pressed = False
    rewind_button_pressed = False
    
    os.chdir(folder_path)
    for file in glob.glob("*"):
        current_image_path = f"{folder_path}/{file}"
        # photo path list
        image_file_paths.append(current_image_path)
        # photo name list
        image_names.append(file)

    # backward botton
    REWIND_BUTTON = Button(
        surface=REWIND_ICON_SURFACE, pos=(WIDTH/2-100, HEIGHT-150), text_input="",
        font=bold_font(100), base_color=BASE_TEXT_COLOR, hovering_color="white"
    )
    # Pause botton
    PAUSE_BUTTON = Button(
        surface=PAUSE_ICON_SURFACE, pos=(WIDTH/2, HEIGHT-150), text_input="",
        font=bold_font(100), base_color=BASE_TEXT_COLOR, hovering_color="white"
    )
    # paly botton
    PLAY_BUTTON = Button(
        surface=PLAY_ICON_SURFACE, pos=(WIDTH/2, HEIGHT-150), text_input="",
        font=bold_font(100), base_color=BASE_TEXT_COLOR, hovering_color="white"
    )
    # forward botton
    SEEK_BUTTON = Button(
        surface=SEEK_ICON_SURFACE, pos=(WIDTH/2+100, HEIGHT-150), text_input="",
        font=bold_font(100), base_color=BASE_TEXT_COLOR, hovering_color="white"
    )
    # Load button
    LOAD_NEW_ALBUM_BUTTON = Button(
        surface=LOAD_NEW_ALBUM_SURFACE, pos=(WIDTH-325, HEIGHT-150), text_input="",
        font=bold_font(100), base_color=BASE_TEXT_COLOR, hovering_color="white"
    )

    # setting switch photo every 5 second automatically
    previous_time = pygame.time.get_ticks()
    COOLDOWN = 5000

    # set photo name attribute
    photo_title_text_surface = bold_font(90).render(image_names[current_image_index], True, BASE_TEXT_COLOR)
    photo_title_text_rect = photo_title_text_surface.get_rect(center=(WIDTH/2, 150))

    # photo display
    image_count_text_surface = regular_font(80).render(f"图片 {current_image_index+1}/{len(image_names)}", True, BASE_TEXT_COLOR)
    image_count_text_rect = image_count_text_surface.get_rect(center=(300, 755))

    # Read picture attribute to adjusting size of window
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

    # Listen to cursor click
    while True:
        for event in pygame.event.get():            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Forward, back, pause, start according to cursor click
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

        # Switch photo
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

# main entry
main_menu()