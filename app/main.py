from notifier import send_discord_message


def main():
    print("League Queue Notifier started.")

    test_message = "RUN BACK TEST — If you see this on your phone, the notifier works."
    success = send_discord_message(test_message)

    if success:
        print("Test message sent successfully.")
    else:
        print("Failed to send test message.")


if __name__ == "__main__":
    main()