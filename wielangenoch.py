import datetime as dt
import shutil
import json
import sys,getopt

try:
    with open("config.json", "r") as f:
        print("in open")
        config = json.load(f)
        timetable = config.get("timetable")
except:
    print("[ERROR] Fehler beim Importieren der Config")
    timetable = []

try:
    opts, args = getopt.getopt(sys.argv[1:], "a")
except getopt.GetoptError as e:
    print("[ERROR]"+ str(e))
    opts = []

#commandline flags
automatic = False
for o,a in opts:
    if o == "-a":
        #automatic mode doesnt give you a choice if there are multiple timeslots and instead defaults to 0
        automatic = True

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', autosize = False):
    """
    utilizes this gist: https://gist.github.com/greenstick/b23e475d2bfdc3a82e34eaa1f6781ee4
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    styling = '%s |%s| %s%% %s' % (prefix, fill, percent, suffix)
    if autosize:
        cols, _ = shutil.get_terminal_size(fallback = (length, 1))
        length = cols - len(styling)
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s' % styling.replace(fill, bar), end = '\r\n')
    # Print New Line on Complete
    if iteration == total:
        print()

timeslots = []
#generate time object pairs if valid timespan was given
for h1,m1,h2,m2 in timespans:
    if (h1,m1)<(h2,m2):
        start = dt.time(h1,m1)
        end = dt.time(h2,m2)
        timeslots.append((start, end))
if timeslots:
    now = dt.datetime.now()
    possibleSlots = list(filter(lambda t: t[0]<=now.time()<=t[1], timeslots))
    #print(possibleSlots)
    if not possibleSlots:
        print("Derzeit läuft keine Vorlesung")
    else:
        if len(possibleSlots)>1 and not automatic:
            try:
                for i,v in enumerate(possibleSlots):
                    print("{}: {} - {}".format(i,v[0], v[1]))
                prompt = input("Mehrere mögliche Zeitslots gefunden, wähle einen davon aus (Default=0)\n")
                index = int(prompt) if prompt else 0
                currentSlot = possibleSlots[index]
                print("{}: {} - {} wurde ausgewählt".format(index, *currentSlot))
            except (IndexError, ValueError):
                currentSlot = possibleSlots[0]
                print("[ERROR] Aufgrund eines Fehlers wurde 0: {} - {} standardmäßig ausgewählt".format(*currentSlot))
        else: currentSlot = possibleSlots[0]
    slotDuration = dt.datetime.combine(dt.date.today(),currentSlot[1]) - dt.datetime.combine(dt.date.today(),currentSlot[0])
    deltaToEnd = dt.datetime.combine(dt.date.today(), currentSlot[1]) - now

    print("Du befindest dich im Zeitslot {} - {}".format(*currentSlot))
    print("Bis zum Ende des derzeitigen Zeitslots dauert es noch {}".format(str(deltaToEnd).split(".")[0]))

    printProgressBar(iteration=(100*(1-(deltaToEnd/slotDuration))), total = 100, suffix = "hast du schon überstanden!", prefix = 'Fortschritt', autosize=True)
else:
    print("[ERROR] Keine validen Zeitspannen gefunden")


