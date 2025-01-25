from datetime import datetime, timedelta

class Event:
    def __init__(self, name, start, end):
        self.name = name
        self.start = datetime.strptime(start, "%H:%M")
        self.end = datetime.strptime(end, "%H:%M")

    def __repr__(self):
        return f'"{self.name}", Start: "{self.start.strftime("%H:%M")}", End: "{self.end.strftime("%H:%M")}"'

class Schedule:
    def __init__(self, working_hours=("08:00", "18:00")):
        self.events = []
        self.working_hours = (
            datetime.strptime(working_hours[0], "%H:%M"),
            datetime.strptime(working_hours[1], "%H:%M"),
        )

    def add_event(self, name, start, end):
        new_event = Event(name, start, end)
        self.events.append(new_event)

    def sort_schedule(self):
        self.events.sort(key=lambda x: x.start)

    def detect_conflicts(self):
        self.sort_schedule()
        conflicts = []
        for i in range(len(self.events) - 1):
            current = self.events[i]
            next_event = self.events[i + 1]
            if current.end > next_event.start:
                conflicts.append((current, next_event))
        return conflicts

    def suggest_alternative(self, event):
        start, end = self.working_hours
        duration = event.end - event.start
        proposed_start = end

        for e in self.events:
            if e.end <= start:
                proposed_start = e.end
                break

        proposed_end = proposed_start + duration
        if proposed_end <= self.working_hours[1]:
            return proposed_start.strftime("%H:%M"), proposed_end.strftime("%H:%M")
        else:
            return None

# Sample usage
schedule = Schedule()
schedule.add_event("Meeting A", "09:00", "10:30")
schedule.add_event("Workshop B", "10:00", "11:30")
schedule.add_event("Lunch Break", "12:00", "13:00")
schedule.add_event("Presentation C", "10:30", "12:00")

schedule.sort_schedule()
conflicts = schedule.detect_conflicts()

print("Sorted Schedule:")
for event in schedule.events:
    print(event)

print("\nConflicting Events:")
for conflict in conflicts:
    print(f"{conflict[0].name} and {conflict[1].name}")

print("\nSuggested Resolutions:")
for conflict in conflicts:
    alternative = schedule.suggest_alternative(conflict[1])
    if alternative:
        print(f'Reschedule "{conflict[1].name}" to Start: "{alternative[0]}", End: "{alternative[1]}"')
    else:
        print(f'No alternative slot available for "{conflict[1].name}".')
