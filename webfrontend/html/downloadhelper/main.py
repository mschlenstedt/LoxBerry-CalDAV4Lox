import caldav
from icalendar import Calendar, Event
#from dotenv import load_dotenv
import os
import sys
#from ftplib import FTP
import datetime

def create_folder_if_missing(folder_name):
    """
    Creates a folder if it doesn't exist
    :param folder_name: Folder name without leading or trailing slash
    :return: None
    """
    if not os.path.exists(f'{folder_name}/'):
        os.mkdir(f'{folder_name}/')


def export_calendar():
    export_cal = Calendar()
    export_cal.add('prodid', '-//Mozilla.org/NONSGML Mozilla Calendar V1.1//EN')
    export_cal.add('version', '2.0')

    # Use a breakpoint in the code line below to debug your script.
    client = caldav.DAVClient(sys.argv[1],
                              username=sys.argv[2],
                              password=sys.argv[3])
    principal = client.principal()
    import_calendar = principal.calendars()[0]
    #events = import_calendar.events()
    ustart = datetime.datetime.fromtimestamp(int(sys.argv[5]))
    uend = datetime.datetime.fromtimestamp(int(sys.argv[6]))
    events = import_calendar.search(
        start=ustart,
        end=uend,
        event=True,
        expand=True,
    )
    #print(f'Found {len(events)} calendar events.')
    for import_event in import_calendar.events():
        export_event = Event()
        for subcomponent in import_event.icalendar_instance.subcomponents:
            export_cal.add_component(subcomponent)

    #create_folder_if_missing('out')
    f = open(os.path.join(sys.argv[4]), 'wb')
    f.write(export_cal.to_ical())
    f.close()
    #print(f'Exported calendar events.')
    pass


#def upload_calendar_file():
#    ftp = FTP(os.getenv('FTP_URI'))
#    ftp.login(os.getenv('FTP_USR'), os.getenv('FTP_PWD'))
#    print(f'Uploading to server...')
#    with open('out/calendar.ics', 'rb') as f:
#        ftp.storbinary(f'STOR {os.getenv("FTP_PATH")}', f)


if __name__ == '__main__':
    #load_dotenv()
    export_calendar()
    #upload_calendar_file()

