import spacy

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

# Define some example rules
rules = {
    "greetings": ["Hi there!", "Hello!", "Hey!", "Hi!", "Howdy!"],
    "how_are_you": ["I'm doing well, thanks!", "I'm good. How about you?", "I'm just a chatbot, but I'm here to help!"],
    "goodbye": ["Goodbye!", "See you later!", "Have a great day!"],
    "ask_name": ["I'm just a chatbot, but you can call me ChatGPT.", "I don't have a name, but you can call me Chatbot."],
}

# Define a function to handle user input
def respond_to_input(input_text):
    # Tokenize the input text
    doc = nlp(input_text.lower())

    # Check for greetings
    for token in doc:
        if token.text in ["hello", "hi", "hey", "howdy"]:
            return rules["greetings"]

    # Check for how are you
    if "how are you" in input_text.lower():
        return rules["how_are_you"]
 # Check for goodbye
    if "bye" in input_text.lower():
        return rules["goodbye"]

    # Check for asking the chatbot's name
    if "name" in input_text.lower():
        return rules["ask_name"]

    # If no matching rules, return a default response
    return ["I'm sorry, I don't understand that."]

# Main loop
first_greeting = True
while True:
    if first_greeting:
        print("Chatbot: Hi there! How can I assist you today?")
        print("Chatbot: You can ask me about my name, or just say hello.")
        first_greeting = False
    else:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Chatbot: Goodbye!")
            break
        response = respond_to_input(user_input)
        print("Chatbot:",response[0])