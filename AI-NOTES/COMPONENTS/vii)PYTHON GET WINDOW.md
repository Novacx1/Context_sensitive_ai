WE do import pygetwindow as gw "where gw is a alias"

It is used to give us the current window

def get_active_window():

    window=gw.getActiveWindow()
    if window:

        return window.title

    return "No active window found"