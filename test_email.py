from email_sender import send_email

receiver = input("Enter receiver email: ")

send_email(
    receiver,
    "AI Customer Support Bot",
    "Congratulations! Your email automation is working successfully."
)