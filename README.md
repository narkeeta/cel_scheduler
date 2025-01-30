# Scheduler

Hey there CEL team! This is my task scheduler. I build this as a containerized docker application
with the backend being done in basic python and the frontend built out in vue.js since that's what
I'm most familiar with.

## Assumptions

some of the assumptions I made for this project where as follows
- A user didn't need to be able to see a continuous feed of the next upcoming event by date time,
but only a sorted list of the events that have been made
- A user would want to be able to add and delete the dates they add
- This would be a single use application for an individual user and therefor not require user login
and separate event storage for specific users
- A event would be invalid if any of it's days of the week and time pairings matched
a previously entered event, but not the duration
- A user would only need to enter an hour & minute value for the duration of the event

## Building and running the application

a pre-requisite for building this application is having docker installed
and not having any other service running on the localhost ports 8000 and 8080

```
docker compose build
docker compose up -d
```
