class Course:
    def __init__(self, name, code, meetings):
        self.name = name
        self.code = code
        self.meetings = meetings
    
    def print_course(self):
        for block in self.meetings:
            
            block.convert_days()

            for day in block.days:
                print(self.name + " (" + self.code + ") has a " + block.type + " from " + str(block.startTime) + " to " + str(block.endTime) + " on " + day)

class Block:
    def __init__(self, days, startTime, endTime, type):
        self.days = days
        self.startTime = startTime
        self.endTime = endTime
        self.type = type
    
    def convert_days(self):
       for i in range(len(self.days)):
        
        if self.days[i] == 'M':
            self.days[i] = 'Monday'
        elif self.days[i] == 'T':
            self.days[i] = 'Tuesday'
        elif self.days[i] == 'W':
            self.days[i] = 'Wednesday'
        elif self.days[i] == 'R':
            self.days[i] = 'Thursday'
        elif self.days[i] == 'F':
            self.days[i] = 'Friday'
    
    def convert_time(self, time):
        time_parts = time.split()
        hour_minute = time_parts[0]
        am_pm = time_parts[1]

        hour, minute = hour_minute.split(":")
        hour = int(hour)
        minute = int(minute)

        if am_pm == "PM" and hour != 12:
            hour += 12

        if am_pm == "AM" and hour == 12:
            hour = 0

        return hour * 60 + minute
    
    def time_to_minutes(self):
        self.startTime = self.convert_time(self.startTime)
        self.endTime = self.convert_time(self.endTime)

def time_conflicts(meeting_a, meeting_b):
    if len(meeting_a.days) == 0 or len(meeting_b.days) == 0:
        return False

    if meeting_a.startTime is None or meeting_a.endTime is None:
        return False

    if meeting_b.startTime is None or meeting_b.endTime is None:
        return False

    shared_day = False

    for day in meeting_a.days:
        if day in meeting_b.days:
            shared_day = True

    if shared_day == False:
        return False

    return meeting_a.startTime < meeting_b.endTime and meeting_b.startTime < meeting_a.endTime

def section_conflicts(section_a, section_b):
    for block_a in section_a:
        for block_b in section_b:
            if time_conflicts(block_a, block_b):
                return True

    return False

math4a_lecture = Block(["M", "W", "F"], "1:00 PM", "1:50 PM", "Lecture")
cmpsc16_lecture = Block(["M", "W"], "3:30 PM", "4:45 PM", "Lecture")
cmpsc16_section = Block(["R"], "2:00 PM", "2:50 PM", "Section")

math4a = Course("MATH 4A - Linear Algebra", "30189", [math4a_lecture])
cmpsc16 = Course("CMPSC 16 - Problem Solving I", "08128", [cmpsc16_lecture, cmpsc16_section])

math4a_lecture.time_to_minutes()
cmpsc16_lecture.time_to_minutes()
cmpsc16_section.time_to_minutes()

overlap_block = Block(["M"], "1:30 PM", "2:20 PM", "Lecture")
different_day_block = Block(["T"], "1:30 PM", "2:20 PM", "Lecture")
touching_block = Block(["M"], "1:50 PM", "2:40 PM", "Lecture")
same_time_block = Block(["W"], "1:00 PM", "1:50 PM", "Lecture")

overlap_block.time_to_minutes()
different_day_block.time_to_minutes()
touching_block.time_to_minutes()
same_time_block.time_to_minutes()

print(time_conflicts(math4a_lecture, overlap_block))        #true
print(time_conflicts(math4a_lecture, different_day_block))  #false
print(time_conflicts(math4a_lecture, touching_block))       #false
print(time_conflicts(math4a_lecture, same_time_block))      #true
print(time_conflicts(math4a_lecture, cmpsc16_lecture))      #false
print(time_conflicts(cmpsc16_lecture, cmpsc16_section))     #false

section_a = [math4a_lecture]
section_b = [cmpsc16_lecture, cmpsc16_section]
section_c = [overlap_block]
section_d = [different_day_block]
section_e = [same_time_block]

print(section_conflicts(section_a, section_b))  #false
print(section_conflicts(section_a, section_c))  #true
print(section_conflicts(section_a, section_d))  #false
print(section_conflicts(section_a, section_e))  #true