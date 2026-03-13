# Assignment: Chat Models & Basic Interactions

## Overview

Practice multi-turn conversations, streaming, parameters, and error handling to build robust AI applications.

---

## Challenge: Interactive Chatbot 

**Goal**: Build a chatbot that maintains conversation history across multiple exchanges.

**Tasks**:
1. Create `chatbot.py` in the `02-chat-models/code/` folder
2. Implement an interactive chatbot that:
   - Accepts user input in a loop
   - Maintains conversation history
   - Allows users to type "quit" to exit
   - Shows the conversation history length after each exchange
3. Use a SystemMessage to give the bot a personality (you choose!)

**Example Interaction**:
```
 Chatbot: Hello! I'm your helpful assistant. Ask me anything!

You: What is Python?
: Python is a versatile programming language...

You: Can you show me an example?
: Sure! Here's a simple Python example...

You: quit
 Goodbye! We had 5 messages in our conversation.
```

**Success Criteria**:
- Bot remembers previous messages
- Conversation history is maintained correctly
- User can exit gracefully

**Hints**:
```python
# 1. Import required modules
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv
import os

# 2. Load environment variables
load_dotenv()

# 3. Create the ChatOpenAI model
model = ChatOpenAI(model=os.environ.get("AI_MODEL", "gpt-5-mini"))

# 4. Initialize conversation history list with a SystemMessage for personality
messages = [
    SystemMessage(content="You are a helpful assistant.")
]

# 5. Create a loop that:
#    - Prompts for user input using input()
#    - Adds HumanMessage to messages list
#    - Invokes model with messages list
#    - Adds AIMessage to messages list
#    - Displays the response

# 6. Check for "quit" to exit the loop

# 7. Show conversation history length on exit
```

---

## Bonus Challenge: Temperature Experiment ️

**Goal**: Understand how temperature affects AI creativity and consistency.

**Tasks**:
1. Create `temperature_lab.py`
2. Test the same creative prompt with 5 different temperature values: 0, 0.5, 1, 1.5, 2
3. Run each temperature 3 times to see variability
4. Display results in a readable format
5. Add your analysis of which temperature works best for different use cases

**Creative Prompt Ideas**:
- "Write a tagline for a coffee shop"
- "Create a name for a tech startup"
- "Suggest a title for a mystery novel"

**Expected Output**:
```
️ Temperature: 0
─────────────────────────────────────
Try 1: "Brew Your Best Day"
Try 2: "Brew Your Best Day"
Try 3: "Brew Your Best Day"

️ Temperature: 2
─────────────────────────────────────
Try 1: "Caffeinated Dreams Await"
Try 2: "Sip the Extraordinary"
Try 3: "Where Magic Meets Mocha"

 Analysis:
- Temperature 0: Perfect for factual, consistent responses
- Temperature 2: Great for creative brainstorming
```

**Success Criteria**:
- Tests at least 5 temperature values
- Shows variability clearly
- Includes your analysis of results

**Hints**:
```python
# 1. Import required modules
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# 2. Load environment variables
load_dotenv()

# 3. Define a list of temperature values to test [0, 0.5, 1, 1.5, 2]

# 4. Define your creative prompt

# 5. Loop through each temperature value:
#    - Create a NEW model instance with that temperature
#    - Run 3 trials with the same prompt
#    - Display the results for each trial

# 6. Add your analysis comparing the different temperature results
```

---

## Solutions

Solutions for all challenges will be available in the [`solution/`](./solution/) folder. Try to complete the challenges on your own first!

**Additional Examples**: Check out the [`samples/`](./samples/) folder for more example solutions covering streaming, error handling, and token tracking!

---

## Need Help?

- **Code issues**: Review examples in [`code/`](./code/)
- **Errors**: Check the lab's error handling section
- **Concepts**: Re-read and study this [lab](./README.md)
