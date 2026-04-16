# League Queue Notifier

A local desktop utility that watches for League of Legends queue events and sends Discord notifications to my phone.

## MVP goals
- Send a Discord notification when a match is found
- Later: detect queue start
- Later: estimate safe time to leave desk
- Later: add funny custom messages

## Tech stack
- Python
- Discord webhook
- Local-only app (no server required)

## Run
```bash
python app/main.py