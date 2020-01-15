from datetime import datetime, time, timedelta

#Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
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
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()

times = [(time(a[0][0],a[0][1]),time(a[1][0],a[1][1])) for a in [((9,15),(10,45)),((11,15),(12,45)),((14,15),(15,45)),((0,0),(23,59))]]
now = datetime.now().time()
for t in times:
    if (t[0] < now < t[1]):
        slot = t
    else:
        slot=None
if slot:
    print("Wir befinden uns in Zeitslot {} bis {}".format(str(t[0]),str(t[1])))
    now = timedelta(hours=now.hour, minutes=now.minute, seconds=now.second)
    end = timedelta(hours=slot[1].hour, minutes=slot[1].minute, seconds=slot[1].second)
    dur = end - now
    print("Bis zum Ende dauert es noch {}".format(dur))
    printProgressBar(iteration=dur.minutes, total=90, prefix="Fortschritt", length=190)
else:
    print("Du bist nicht in einer Vorlesung")
