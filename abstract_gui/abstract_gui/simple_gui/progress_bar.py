"""
    Demo Graph Custom Progress Meter

    The "Graph Element" is a "Gateway Element"
    Looking to create your own custom elements?  Then the Graph Element is an excellent
    place to start.

    This short demo implements a Circular Progress Meter

    The event loop has a little trick some may like....
        Rather than adding a sleep instead use window.read with a timeout
        This has a dual purpose. You get the delay you're after AND your GUI is refreshed

    Copyright 2022 PySimpleGUI
"""
import PySimpleGUI as sg
# Settings for you to modify are the size of the element, the circle width & color and the font for the % complete
GRAPH_SIZE = (300 , 300)          # this one setting drives the other settings
CIRCLE_LINE_WIDTH, LINE_COLOR = 20, 'yellow'
TEXT_FONT = 'Courier'

# Computations based on your settings above
TEXT_HEIGHT = GRAPH_SIZE[0]//4
TEXT_LOCATION = (GRAPH_SIZE[0]//2, GRAPH_SIZE[1]//2)
TEXT_COLOR = LINE_COLOR
def update_meter(graph_elem, percent_complete):
    """
    Update a circular progress meter
    :param graph_elem:              The Graph element being drawn in
    :type graph_elem:               sg.Graph
    :param percent_complete:        Percentage to show complete from 0 to 100
    :type percent_complete:         float | int
    """
    graph_elem.erase()
    arc_length = percent_complete/100*360+.9
    if arc_length >= 360:
        arc_length = 359.9
    graph_elem.draw_arc((CIRCLE_LINE_WIDTH, GRAPH_SIZE[1] - CIRCLE_LINE_WIDTH), (GRAPH_SIZE[0] - CIRCLE_LINE_WIDTH, CIRCLE_LINE_WIDTH),
                   arc_length, 0, 'arc', arc_color=LINE_COLOR, line_width=CIRCLE_LINE_WIDTH)
    percent = percent_complete
    graph_elem.draw_text(f'{percent:.0f}%', TEXT_LOCATION, font=(TEXT_FONT, -TEXT_HEIGHT), color=TEXT_COLOR)
def main():
    for i in range(10000):
        if not sg.one_line_progress_meter('My 1-line progress meter',
                                          i+1, 10000,
                                          'meter key',
                                          'MY MESSAGE1',
                                          'MY MESSAGE 2',
                                          orientation='v'):
            print('Hit the break')
            break
  
      

main()
