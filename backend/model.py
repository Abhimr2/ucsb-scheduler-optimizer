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
        self.s = self.convert_time(self.s)
        self.e = self.convert_time(self.e)

math4a_lecture = Block(["M", "W", "F"], "1:00 PM", "1:50 PM", "Lecture")
cmpsc16_lecture = Block(["M", "W"], "3:30 PM", "4:45 PM", "Lecture")
cmpsc16_section = Block(["R"], "2:00 PM", "2:50 PM", "Section")

math4a = Course("MATH 4A - Linear Algebra", "30189", [math4a_lecture])
cmpsc16 = Course("CMPSC 16 - Problem Solving I", "08128", [cmpsc16_lecture, cmpsc16_section])

math4a.print_course()
cmpsc16.print_course()