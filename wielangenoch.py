import datetime as dt	IF
import sys,getopt
#order will be respected by -a flag
timespans = [
    (9,15,11,45),
    (11,15,12,45),
    (14,15,15,45),
    (19,15,23,45),
    (0,00,23,59)
]
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

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\n"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    #print(percent)
    filledLength = int(length * iteration // total)
    #print(filledLength)
    bar = fill * filledLength + '-' * (length - filledLength)
    #print(bar)
    print('\r%s|%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
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

    printProgressBar(iteration=(100*(1-(deltaToEnd/slotDuration))), total = 100, suffix = "hast du schon überstanden!", prefix = 'Fortschritt')
else:
    print("[ERROR] Keine validen Zeitspannen gefunden")


