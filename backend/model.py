from itertools import product

class Scheduler:
    def __init__(self, courses):
        self.courses = courses
    
    def generate_schedules(self):
        allOptions = []
        
        for course in self.courses:
            allOptions.append(course.create_options())
        
        allSchedules = []
        allSchedules = list(product(*allOptions))

        expected = 2 * 2 * 1 * 1
        actual = len(allSchedules)

        validSchedules = []

        for schedule in allSchedules:
            val = self.schedule_is_valid(schedule)

            if val == True:
                validSchedules.append(schedule)
        
        correct = len(validSchedules)

        print("Expected raw schedules:", expected)
        print("Actual raw schedules:", actual)
        print("Valid schedules:", correct)
    
    def schedule_is_valid(self, schedule):
        for i in range(len(schedule)):
            for j in range(i + 1, len(schedule)):
                if option_conflicts(schedule[i], schedule[j]):
                    return False

        return True
    
    def get_allScheduleBlocks(self, schedule):
        allBlocks = []
        
        for course_option in schedule:
            for block in course_option:
                allBlocks.append(block)
        
        return allBlocks
    
    def sort_by_days(self, schedule):
        days = [[], [], [], [], []]
        daysOfTheWeek = ["M", "T", "W", "R", "F"]

        allBlocks = self.get_allScheduleBlocks(schedule)

        for i in range(len(daysOfTheWeek)):
            day = daysOfTheWeek[i]

            for block in allBlocks:
                if day in block.days:
                    days[i].append(block)

        for day_blocks in days:
            day_blocks.sort(key=lambda item: (item.startTime, item.endTime))

        return days
    
    def score_days(self, schedule, preferredDays):
        day_score = 0
        total_score = 0

        for course_option in schedule:
            for block in course_option:
                total_score += len(block.days)

                for preferred_day in preferredDays:
                    if preferred_day in block.days:
                        day_score += 1

        return day_score / total_score
    
    def score_timeRange(self, schedule, preferredStart, preferredEnd):
        time_score = 0
        total_score = 0

        for course_option in schedule:
            for block in course_option:
                total_score += len(block.days)

                if block.startTime >= preferredStart and block.endTime <= preferredEnd:
                    time_score += len(block.days)
        
        return time_score / total_score
    
    def score_gap(self, schedule, preferredGap):
        sortedSched = self.sort_by_days(schedule)

        successful_gaps = 0
        total_gaps = 0

        for sorted_dayBlocks in sortedSched:
            for i in range(len(sorted_dayBlocks) - 1):
                current_block = sorted_dayBlocks[i]
                next_block = sorted_dayBlocks[i + 1]

                gap = next_block.startTime - current_block.endTime
                total_gaps += 1

                if gap <= preferredGap:
                    successful_gaps += 1

        if total_gaps == 0:
            return 1.0

        return successful_gaps / total_gaps
    
    def score_schedule(self, schedule, preferences):        
        gapScore = self.score_gap(schedule, preferences["preferredGap"])
        timeScore = self.score_timeRange(schedule, preferences["preferredStart"], preferences["preferredEnd"])
        dayScore = self.score_days(schedule, preferences["preferredDays"])

        dayScore *= preferences["dayWeight"]
        timeScore *= preferences["timeWeight"]
        gapScore *= preferences["gapWeight"]

        totalWeight = preferences["dayWeight"] + preferences["timeWeight"] + preferences["gapWeight"]

        weightedScore = dayScore + timeScore + gapScore

        return weightedScore / totalWeight * 100

class Course:
    def __init__(self, name, code, lectures, sections):
        self.name = name
        self.code = code
        self.lectures = lectures
        self.sections = sections
    
    def create_options(self):
        options = []

        if len(self.lectures) == 0 and len(self.sections) == 0:
            return options

        if len(self.sections) == 0:
            for lecture in self.lectures:
                options.append([lecture])

            return options

        if len(self.lectures) == 0:
            for section in self.sections:
                options.append([section])

            return options

        for lecture in self.lectures:
            for section in self.sections:
                options.append([lecture, section])

        return options


    def print_course(self):
        all_blocks = self.lectures + self.sections

        day_names = {
            "M": "Monday",
            "T": "Tuesday",
            "W": "Wednesday",
            "R": "Thursday",
            "F": "Friday",
        }

        for block in all_blocks:
            for day in block.days:
                displayed_day = day_names.get(day, day)

                print(
                    self.name
                    + " ("
                    + self.code
                    + ") has a "
                    + block.type
                    + " from "
                    + str(block.startTime)
                    + " to "
                    + str(block.endTime)
                    + " on "
                    + displayed_day
                )

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

def option_conflicts(option_a, option_b):
    for block_a in option_a:
        for block_b in option_b:
            if time_conflicts(block_a, block_b):
                return True

    return False