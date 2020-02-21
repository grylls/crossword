import crossword
import PySimpleGUI as sg
import ipuz

def generate_crossword():
    with open('puzzle.ipuz') as puzzle_file:
        ipuz_dict = ipuz.read(puzzle_file.read())  # may raise ipuz.IPUZException

    puzzle = crossword.from_ipuz(ipuz_dict)
    return puzzle
    
sg.ChangeLookAndFeel('GreenTan')     
BOX_SIZE = 25
column1 = []
column2 = []
across_arr = []
down_arr = []
             
column1 = [
        [
            sg.Listbox(values=across_arr,
            key="files_listbox_a",
            size=(35, 30))

        ]
    ]

column2 = [
        [
            sg.Listbox(values=down_arr,
            key="files_listbox_d",
            size=(35, 30)),
                       
        ]
    ]

layout = [  
        [sg.Frame('Crossword',[ 
                [sg.Button('Generate'),sg.Button('Show Solution'), sg.Button('Exit')], 
                [sg.Graph((400,500), (0,450), (350,0), background_color='grey', enable_events=True, key='_GRAPH_')
    ]]),sg.Frame('Clues',[
                [
                    sg.Text("Across", background_color='#F7F3EC', justification='center', size=(35, 0)),
                    sg.Text("Down", background_color='#F7F3EC', justification='center', size=(35, 0))
                ],
                [       
                    sg.Column(column1),
                    sg.Column(column2)
                ],
    ],size=(700,500))],
]

# Create the Window
window1 = sg.Window('CrossWord',size=(1100,500)).Layout(layout).Finalize()
g = window1.FindElement('_GRAPH_')
window1.FindElement('Show Solution').Update(disabled=True)
while True:
    event, values = window1.read()
    mouse = values['_GRAPH_']
    if event in ('Show Solution'):   # if user click on show button
       layout2 = [
            [sg.Text('Crossword Solution')], 
            [sg.Button('Exit')],
            [sg.Graph((500,500), (0,450), (430,0), background_color='grey', enable_events=True, key='_OGRAPH_')],
        ] 
       window2 = sg.Window('CrossWord Solution', size=(500,500)).Layout(layout2).Finalize()
       o = window2.FindElement('_OGRAPH_')
       puzzledata = generate_crossword()      
       for x, y in puzzledata.cells:
           if puzzledata[x, y].solution == "#":
               o.DrawRectangle((y*BOX_SIZE+5,x*BOX_SIZE+3), (y*BOX_SIZE+BOX_SIZE+5,x*BOX_SIZE+BOX_SIZE+3), line_color='black', fill_color='black')
           else:
               o.DrawRectangle((y*BOX_SIZE+5,x*BOX_SIZE+3), (y*BOX_SIZE+BOX_SIZE+5,x*BOX_SIZE+BOX_SIZE+3), line_color='black')
               o.DrawText('{}'.format(puzzledata[x, y].solution),(y*BOX_SIZE+10,x*BOX_SIZE+8))
       while True:
           event2, values2 = window2.read()
           if event2 is None or event2 == 'Exit':
               break
       window2.close()    
    elif event == "Generate":
       puzzledata = generate_crossword()
       across = puzzledata.clues.across
       for m in across:
            val = str(m)+" - "+across[m]
            across_arr.append(val)
            window1.Element('files_listbox_a').Update(values = across_arr)
        
       down = puzzledata.clues.down     
       for n in down:
           val2 = str(n)+" - "+down[n]
           down_arr.append(val2)
           window1.Element('files_listbox_d').Update(values = down_arr)
           
       for x, y in puzzledata.cells:
           if puzzledata[x, y].solution == "#":
               g.DrawRectangle((y*BOX_SIZE+5,x*BOX_SIZE+3), (y*BOX_SIZE+BOX_SIZE+5,x*BOX_SIZE+BOX_SIZE+3), line_color='black', fill_color='black')
           else:
               #g.DrawRectangle((y*BOX_SIZE+5,x*BOX_SIZE+3), (y*BOX_SIZE+BOX_SIZE+5,x*BOX_SIZE+BOX_SIZE+3), line_color='black')
               g.DrawRectangle((y*BOX_SIZE+5,x*BOX_SIZE+3), (y*BOX_SIZE+BOX_SIZE+5,x*BOX_SIZE+BOX_SIZE+3), line_color='black')
               if(puzzledata[x, y].puzzle == "#"):
                   pass
               elif isinstance(puzzledata[x, y].puzzle, int):
                   if puzzledata[x, y].puzzle != 0:
                       g.DrawText('{}'.format(puzzledata[x, y].puzzle),(x*BOX_SIZE+10,y*BOX_SIZE+8))
               else:
                   newdict = puzzledata[x, y].puzzle
                   if newdict['cell']!=0:
                       g.DrawText('{}'.format(newdict['cell']),(x*BOX_SIZE+10,y*BOX_SIZE+8))
       window1.FindElement('Show Solution').Update(disabled=False)
       window1.FindElement('Generate').Update(disabled=True)
       
    elif event == '_GRAPH_':
       if mouse == (None, None):
           continue
       box_x = mouse[0]//BOX_SIZE
       box_y = mouse[1]//BOX_SIZE
       #letter_location = (box_x * BOX_SIZE + 18, box_y * BOX_SIZE + 17)
       sg.PopupAutoClose("need to implement Input box") 
                   
    elif event is None or event == 'Exit':
        break
window1.close()