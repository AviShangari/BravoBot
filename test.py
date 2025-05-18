from intent_classifier import IntentClassifier

intent_model = IntentClassifier()

print(intent_model.predict_intent("what's the weather like"))
print(intent_model.predict_intent("what is the time"))
print(intent_model.predict_intent("open youtube"))
