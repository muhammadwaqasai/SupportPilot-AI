from intent_detector import detect_intent

message = "I received a damaged product and I want a refund."

result = detect_intent(message)

print(result)