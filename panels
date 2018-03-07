import sys, os, json, time, datetime, math, curses, thread

COUNTER = 0

def my_raw_input(window, r, c, prompt_string):
    curses.echo()
    window.addstr(r, c, prompt_string)
    window.refresh()
    input = window.getstr(r + 1, c)
    return input

def count(window):
    global COUNTER
    while True:
        window.addstr(3, 0, '%d'%(COUNTER))
        if COUNTER >= 1000:
            COUNTER = 0
        COUNTER += 1
        window.refresh()

def main(args):
    # create stdscr
    stdscr = curses.initscr()
    stdscr.clear()

    # allow echo, set colors
    curses.echo()
    curses.start_color()
    curses.use_default_colors()

    # define 2 windows
    command_window = curses.newwin(3, 30, 0, 0)
    display_window = curses.newwin(6, 30, 5, 0)
    command_window.border()
    display_window.border()

    # thread to refresh display_window
    thread.start_new_thread(count, (display_window,))

    # main thread, waiting for user's command.
    while True:
        command = my_raw_input(command_window, 0, 0, 'Enter your command :')
        if command == 'quit':
            break
        else:
            command_window.addstr(1, 0, ' '*len(command))

    curses.endwin()
    curses.wrapper(main)
