import PySimpleGUI as sg
import playlist
import textwrap

def makeWindow():
    sg.theme('Dark Teal 2')



    selection_column = [[sg.Text('Select activity type: ', font=('Futura', 20), key = 'text1', size = 250)], 
            [sg.Combo(['Bike', 'Walk', 'Run'], font = 'Futura 20', size = (15, 1), enable_events=True,  readonly=True, key='-COMBO1-')],
            [sg.Text('Enter desired intensity: ', font=('Futura', 20), key = 'text2')],
            [sg.Combo(['Leisurely', 'Normal', 'High'], font = 'Futura 20', size = (15, 1), enable_events=True,  readonly=True, key='-COMBO2-')],
            [sg.Text('Enter distance (miles): ', font=('Futura', 20), key = 'text3')],
            [sg.InputText(font=('Futura 20'), size = (16, 1), key = 'DST')],
            [sg.Text('Enter music genre: ', font=('Futura', 20), key = 'text4')],
            [sg.Combo(['Happy', 'Moody', 'Calm'], font = 'Futura 20', size = (15, 1), enable_events=True,  readonly=True, key='-COMBO3-')],
            [sg.Button('Generate Playlist', font = 'Futura 20', key = 'GEN'), sg.Button('Clear', font = 'Futura 20', key = 'CLR')],
            [sg.Text(font = ('Futura 20'), key = 'INFO')],
            [sg.Button('Give me a shower song!', font = ('Futura 20'), key = 'SHWR')]]

    playlist_column = [[sg.Text(font=('Futura 20'), key = 'TITLE')],
                       [sg.Multiline(size = (70, 57), key = 'LST', enable_events = True, horizontal_scroll=True, autoscroll = True)],
                       [sg.Text(font=('Futura 20'), size = (16, None), key = 'DUR')],
                       [sg.Button('Add playlist to Spotify', key = 'IMP', font = 'Futura 20', button_color='green', visible = False)]]

    layout = [
            [sg.Column(selection_column, size = (300, 800)),
             sg.VSeperator(pad = (0,0)),
             sg.Column(playlist_column, size = (700, 800))],
        ]

    # Create the Window
    window = sg.Window('Sustainify', layout, size = (800, 800))
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break

        if event == 'SHWR':
            window['TITLE'].update('Get Scrubbing!')
            window['LST'].update('')
            window['INFO'].update('')
            song = playlist.makeShower()
            artists = song['track']['artists']
            artistStr = ""
            for a in artists:
                artistStr += a['name'] + ", "
            artistStr = artistStr[:len(artistStr) - 2]
            name = "\"" + song['track']['name'] + "\""
            toPrintSong = name + " - " + artistStr + '\n'
            infoT = "Duration: " + msToTF(song['track']['duration_ms'])
            window['DUR'].update(infoT)
            window['LST'].print(toPrintSong, font = 'Futura 16', text_color = 'black')
            window['INFO'].print("Showers should be < 4 minutes")


        if event == 'GEN':
            if(values['-COMBO1-'] == '' or values['-COMBO2-'] == '' or values['DST'] == '' or values['-COMBO3-'] == ''):
                window['LST'].print("Insufficient data!", font = 'Futura 16', text_color = 'black')
            else:
                window['IMP'].update(visible = True)
                window['LST'].update('')
                window['INFO'].update('')
                songs, time, timeO = playlist.makePlaylist(values['-COMBO1-'], values['-COMBO2-'], values['DST'], values['-COMBO3-'])
                title = values['-COMBO3-'] + " Playlist to " + values['-COMBO1-'] + " to"
                window['TITLE'].update(title)

                toPrint = ""
                for song in songs:
                    artists = song['track']['artists']
                    artistStr = ""
                    for a in artists:
                        artistStr += a['name'] + ", "
                    artistStr = artistStr[:len(artistStr) - 2]
                    name = "\"" + song['track']['name'] + "\""
                    toPrintSong = name + " - " + artistStr + '\n'
                    toPrint += toPrintSong
                
                infoT = "Duration: " + msToTF(time)
                window['DUR'].update(infoT)
                window['LST'].print(toPrint, font = 'Futura 16', text_color = 'black')
                infoP = "You want to " + values['-COMBO1-'].lower() + " for " + values['DST'] + " miles at a " + values['-COMBO2-'].lower() + " pace. " + "This should take you " \
                        + str(round(timeO//3600000)) + " hour(s) and " + str(round(((timeO%3600000)//60000))) + " minute(s).";
                infoo = textwrap.wrap(infoP, 30)
                for s in infoo:
                    window['INFO'].print(s)
                
        if event == 'IMP':
            importToSpotify()

        if event == 'CLR':
            window['IMP'].update(visible = False)
            window['LST'].update('')
            window['TITLE'].update('')
            window['-COMBO1-'].update('')
            window['-COMBO2-'].update('')
            window['-COMBO3-'].update('')
            window['DST'].update('')
            window['DUR'].update('')
            window['INFO'].update('')

    window.close()

def msToTF(time):
    min = str(round(((time%3600000)//60000)))
    if(len(min) == 1):
        min = "0" + min
    
    sec = str(round((time%60000)/1000))
    if(len(sec) == 1):
        sec = "0" + sec
        
    timeFormatted = str(round(time//3600000)) + ':' + min + ':' + sec
    return timeFormatted

def importToSpotify():
    layout = [[sg.InputText('Enter Playlist Name', font=('Futura 15'), size = (16, 1), key = 'DST')]]
    window = sg.Window('Import', layout, size = (200, 200))
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break




def main():
    makeWindow()

if __name__ == "__main__":
    main()