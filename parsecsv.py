import csv
from datetime import datetime

def parse_days(day_str):
    mapping = {
        'M': 'Mon',
        'T': 'Tue',
        'W': 'Wed',
        'Th': 'Thu',
        'F': 'Fri',
        'S': 'Sat',
        'Su': 'Sun'
    }
    result = []
    i = 0
    while i < len(day_str):
        if day_str[i:i+2] == 'Th':
            result.append(mapping['Th'])
            i += 2
        elif day_str[i:i+2] == 'Su':
            result.append(mapping['Su'])
            i += 2
        elif day_str[i] in mapping:
            result.append(mapping[day_str[i]])
            i += 1
        else:
            i += 1  # skip unknown
    return result

class event():
    def __init__(self, coursedict: dict):
        if (coursedict):
            self.course = coursedict['Course Code']
            self.component = coursedict['Component']
            self.day = coursedict['Day']
            self.starttime = datetime.strptime(coursedict['Start Time'],"%I:%M %p")
            self.endtime = datetime.strptime(coursedict['End Time'],"%I:%M %p")
            self.room = coursedict['Room']
            self.extras = coursedict
        else:
            raise ValueError("provide 'coursedict'")
        
    def __str__(self):
        return (f"{self.course} ({self.component}) in {self.room} on {self.day} "
                f"from {self.starttime.strftime('%I:%M %p')} to {self.endtime.strftime('%I:%M %p')}")
    

class room():
    def __init__(self, room_name: str, events: list[event]):
        self.room_name = room_name
        self.events = events

    def __str__(self):
        events_str = "\n  ".join(str(e) for e in self.events)
        return f"Room {self.room_name}:\n  {events_str if events_str else 'No events scheduled.'}"

    def checkinstant(self, day: str, timestring: str) -> bool:
        """Check if the room is available at the specified time instant on the specified day."""
        try: check_time = datetime.strptime(timestring, "%I:%M %p").time()
        except: return False
        for e in self.events:
            if day in e.day:
                if e.starttime.time() <= check_time < e.endtime.time():
                    return False
        return True

    def checkinterval(self, day: str, start_time: str, end_time: str) -> bool:
        """Check if the room is free for the given interval on the specified day."""
        try:
            check_start = datetime.strptime(start_time, "%I:%M %p").time()
            check_end = datetime.strptime(end_time, "%I:%M %p").time()
        except: return False
        for e in self.events:
            if day in e.day:
                # Check for overlap
                event_start = e.starttime.time()
                event_end = e.endtime.time()
                if not (check_end <= event_start or check_start >= event_end):
                    return False
        return True
    def dict(self):
        return({"room_name": self.room_name, "events": [i.extras for i in self.events]})

def csvparse():
    with open("timetable.csv", "r") as csvfile:
        csvreader = csv.DictReader(csvfile)
        rows=[]
        for i in csvreader:
            rows.append(i)

    roomset = set()
    for i in rows:
        if i['Room'] != '': roomset.add(i['Room'])
    roomset = set([i for i in roomset if (i[0] in 'ABCD' and i[1:].isdigit() and len(i)==4)])
    
    roomset = sorted(roomset)

    events_list = []
    for i in rows:
        if i['Room'] in roomset:
            # i['Start Time'] = datetime.strptime(i['Start Time'],"%I:%M %p")
            # i['End Time'] = datetime.strptime(i['End Time'],"%I:%M %p")
            i['Day'] = parse_days(i['Day'])
            events_list.append(event(i))


    rooms_list = []

    for i in roomset:
        eventsinroom = []
        for j in events_list:
            if j.room == i: eventsinroom.append(j)
        rooms_list.append(room(i, eventsinroom))
    
    return {
        "rooms_list": rooms_list,
        "events_list": events_list,
        "roomset": roomset
    }
csv_result = csvparse()

def fetchroom(room_name: str):
    for r in csv_result['rooms_list']:
        if r.room_name == room_name:
            return r
    return None

# import json
# print(csv_result['roomset'])
# roomslist = csv_result['rooms_list']
# print(fetchroom('D217'))
# print(fetchroom('D217').checkinstant('Mon', '02:15 PM'))
# print(fetchroom('D217').checkinterval('Mon', '02:25 PM', '03:31 PM'))
# with open('room.json', 'w') as f:
#     f.write(json.dumps(fetchroom('D217').dict()))
