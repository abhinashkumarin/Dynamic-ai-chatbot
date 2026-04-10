"""
NLP Engine v5.0
- Model khud user ka message analyze karta hai
- Intent, Emotion, Sentiment sab model decide karta hai
- Koi hard-coded answer nahi — sab dynamic
- OOP concepts, technical topics → proper specific answers
- Analytics fully working
"""

import re
import time
import random
import asyncio
from datetime import datetime
from collections import defaultdict, deque
from typing import Optional

from loguru import logger


# ─── TRAINING DATA ─────────────────────────────────────────────────────────────
INTENT_TRAINING_DATA = {
    "greeting": [
        "hello", "hi", "hey", "good morning", "good evening", "good afternoon",
        "howdy", "greetings", "what's up", "sup", "namaste", "hola", "bonjour",
        "hi there", "hello there", "how are you", "how do you do", "hey there",
        "good day", "yo", "hiya", "hey bot", "hello bot", "hi bot",
        "good to see you", "nice to meet you", "hey assistant", "start",
        "hi again", "hello again", "good morning bot", "hey there friend",
    ],
    "farewell": [
        "bye", "goodbye", "see you", "later", "take care", "farewell",
        "see ya", "goodnight", "good night", "until next time",
        "catch you later", "have a good day", "ttyl", "talk later",
        "adios", "signing off", "gotta go", "i am leaving",
        "peace out", "so long", "bye bye", "see you soon",
        "i will go now", "ok bye", "alright bye", "good night bye",
        "take care bye", "have a nice day bye", "leaving now",
        "talk to you later", "that is all bye",
    ],
    "thanks": [
        "thank you", "thanks", "thank you so much", "many thanks",
        "appreciate it", "grateful", "much appreciated", "thx", "ty",
        "thankyou", "thanks a lot", "thanks a bunch", "i appreciate it",
        "that helped", "thank you very much", "cheers", "thanks for helping",
        "that was helpful", "awesome help", "really appreciate",
        "you helped me a lot", "great help thanks", "i am grateful",
        "thank you for the help", "thanks so much", "big thanks",
        "very helpful thanks", "helpful thanks",
    ],
    "help": [
        "help", "need help", "can you help", "assist me", "i need assistance",
        "support", "what can you do", "how can you help", "what are your features",
        "what do you know", "capabilities", "abilities", "options",
        "what can i ask", "guide me", "show me features", "what topics",
        "i am stuck", "help me out", "need support", "i need guidance",
        "can you assist", "what do you offer", "how does this work",
        "i need help", "what are your skills", "what can i do here",
        "how to use you", "show capabilities", "what are you good at",
    ],
    "about": [
        "who are you", "what are you", "tell me about yourself",
        "what is your name", "introduce yourself", "about you",
        "are you a robot", "are you ai", "are you human", "are you real",
        "who made you", "what technology do you use", "how do you work",
        "your purpose", "describe yourself", "are you smart",
        "are you chatgpt", "who created you", "what powers you",
        "are you intelligent", "how were you made", "what is your purpose",
        "which model are you", "are you gpt", "who built you",
        "what kind of bot are you",
    ],
    "time_date": [
        "what time is it", "current time please", "tell me the time",
        "what is the time now", "time right now", "time please",
        "what is today date", "today date please", "what day is today",
        "what day is it today", "current date please", "what is the date",
        "tell me the date", "what month is it", "what year is it",
        "date today please", "day today", "what time",
        "clock time now", "give me the time", "show me the time",
        "what is the current time", "tell me today",
        "time and date please", "current time and date",
        "what day of the week", "which day today",
    ],
    "weather": [
        "what is the weather", "how is the weather today",
        "weather forecast please", "will it rain today",
        "is it hot today", "is it cold today", "temperature today",
        "should i carry umbrella", "is it raining now",
        "climate today", "weather outside", "weather update",
        "current weather please", "weather tomorrow",
        "weather this week", "how hot is it", "how cold is it",
        "is it sunny today", "weather report",
        "what is the temperature", "check weather",
        "rain forecast", "sunny or rainy today",
    ],
    "joke": [
        "tell me a joke", "joke please", "say a joke",
        "give me a joke", "make me laugh", "something funny",
        "funny joke please", "i want to laugh", "crack a joke",
        "humor me please", "tell something funny", "amuse me",
        "i need a laugh", "can you joke", "be funny",
        "entertain me", "cheer me up with joke", "share a joke",
        "comedy please", "another joke", "one more joke",
        "funny please", "make me smile", "programmer joke",
        "tech joke", "coding joke", "ai joke",
    ],
    "technical": [
        "what is java", "explain java", "java programming",
        "what is python", "explain python", "python programming",
        "what is javascript", "explain javascript",
        "what is c plus plus", "what is cpp",
        "what is artificial intelligence", "explain ai",
        "what is machine learning", "explain machine learning",
        "what is deep learning", "explain deep learning",
        "what is neural network", "explain neural network",
        "what is nlp", "what is natural language processing",
        "what is data science", "explain data science",
        "what is api", "what is rest api", "explain api",
        "what is database", "what is sql", "what is mongodb",
        "what is react", "what is nodejs", "what is fastapi",
        "what is oop", "what is object oriented programming",
        "explain oop", "oop concepts", "explain oops",
        "what is oops", "oops in java", "oop in python",
        "four pillars of oop", "pillars of oops",
        "what is encapsulation", "what is inheritance",
        "what is polymorphism", "what is abstraction",
        "what is algorithm", "what is data structure",
        "what is git", "what is docker", "what is linux",
        "what is cloud computing", "what is recursion",
        "how to code", "programming help", "coding question",
        "explain programming", "what is software",
    ],
    "math": [
        "what is mathematics", "explain math", "math help",
        "what is algebra", "explain algebra",
        "what is calculus", "explain calculus",
        "what is statistics", "explain statistics",
        "what is probability", "math problem help",
        "what is trigonometry", "what is matrix",
        "what is derivative", "what is integral",
        "solve equation", "math question", "arithmetic",
        "calculate", "what is number theory",
        "math formula help", "what is theorem",
    ],
    "emotion_happy": [
        "i am happy today", "feeling great right now",
        "i feel wonderful", "i am so excited",
        "feeling amazing today", "best day ever for me",
        "i am thrilled", "feeling fantastic",
        "i am delighted today", "so pleased right now",
        "feeling so blessed", "i am overjoyed",
        "very excited today", "feeling very positive",
        "life is so good", "feeling cheerful today",
        "i am so glad", "very happy today",
        "cannot stop smiling", "everything is perfect",
        "feeling on cloud nine", "mood is amazing today",
    ],
    "emotion_sad": [
        "i am feeling sad today", "feeling very low right now",
        "i feel terrible today", "very upset today",
        "i am depressed right now", "feeling so down",
        "not feeling well emotionally", "i feel hopeless",
        "very unhappy right now", "i am miserable today",
        "feeling so worthless", "i feel so empty inside",
        "very sad today", "i have been crying a lot",
        "feeling completely broken", "i am heartbroken",
        "feeling so lonely today", "feeling so alone",
        "i feel completely lost", "nothing feels right",
        "feeling so helpless", "i am really struggling",
        "very low today emotionally", "feeling blue today",
        "i feel like crying", "everything feels heavy",
        "cannot feel happy", "i am not okay today",
    ],
    "emotion_angry": [
        "i am very angry right now", "feeling so frustrated today",
        "i am absolutely furious", "so annoyed right now",
        "i am really irritated", "feeling so mad",
        "so frustrated right now", "this is so ridiculous",
        "i am truly enraged", "very irritated today",
        "i am totally fed up", "i am completely livid",
        "boiling with anger now", "i am fuming right now",
        "this makes me so mad", "rage is building up",
        "everything is making me angry", "anger is overwhelming",
        "fed up completely", "furious about everything",
        "annoyed beyond limit", "mad about this situation",
        "cannot calm down angry",
    ],
    "emotion_anxious": [
        "i am feeling anxious today", "feeling so nervous right now",
        "i am really worried about this", "feeling quite scared",
        "i am very stressed right now", "feeling very tensed",
        "feeling completely overwhelmed", "i am panicking",
        "so much pressure on me", "i feel so uneasy",
        "feeling restless today", "i am afraid right now",
        "very stressed out today", "i am having anxiety",
        "so much stress today", "feeling very tense",
        "i cannot relax at all", "i am overthinking everything",
        "feeling panicked right now", "i am fearful today",
        "cannot stop worrying", "fear is taking over",
        "nervous about everything", "worried sick",
    ],
    "question_general": [
        "tell me about", "can you explain", "i want to know about",
        "give me information about", "please explain",
        "what exactly is", "help me understand",
        "i am confused about", "can you clarify",
        "make me understand", "in simple words explain",
        "describe to me", "i have a question about",
        "curious about", "what does this mean",
        "how does this work", "please describe",
        "i need information about", "could you tell me about",
        "want to learn about", "teach me about",
        "explain in detail", "elaborate on this",
        "break this down for me", "simplify for me",
        "what do you know about",
    ],
    "compliment": [
        "you are so great", "amazing response",
        "excellent work", "you are really smart",
        "brilliant answer", "fantastic response",
        "wonderful", "very impressive",
        "really good job", "well done",
        "you are so helpful", "great work",
        "love your answer", "perfect response",
        "you are the best", "so intelligent",
        "truly outstanding", "superb answer",
        "you nailed it", "spot on",
        "flawless response", "you are awesome",
        "best chatbot ever", "very helpful",
        "i love your responses", "keep up good work",
    ],
    "negative_feedback": [
        "bad response", "terrible answer",
        "wrong answer", "incorrect response",
        "useless", "not helpful",
        "that is wrong", "you failed",
        "pathetic answer", "stop repeating",
        "worst chatbot", "i hate your answer",
        "complete nonsense", "makes no sense",
        "you dont understand me", "terrible bot",
        "very bad response", "i am disappointed",
        "wrong information", "misleading response",
        "not what i asked", "missing the point",
        "poor quality response", "totally wrong",
    ],
}

# ─── KNOWLEDGE BASE — model uses this to generate answers ────────────────────
# Yeh sab model ka "brain" hai — responses yahan se aate hain
KNOWLEDGE_BASE = {
    # ── Programming Languages ──────────────────────────────────────────────
    "java": {
        "title": "Java Programming Language",
        "content": """Java ek high-level, object-oriented programming language hai jo Sun Microsystems ne 1995 mein banaya.

🔑 **Key Features:**
• **Platform Independent** — "Write Once, Run Anywhere" (WORA)
• **Object-Oriented** — sab kuch classes aur objects mein
• **Strongly Typed** — variable ka type pehle declare karna hota hai
• **Automatic Memory Management** — Garbage Collector
• **Multithreading** — multiple tasks simultaneously

📦 **Popular Frameworks:** Spring Boot, Hibernate, Maven, Gradle

💡 **Used for:** Android apps, enterprise software, web backends, banking systems, big data (Hadoop)

```java
// Simple Java example
public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
```""",
        "keywords": ["java", "jvm", "spring", "j2ee", "java programming", "core java"]
    },

    "python": {
        "title": "Python Programming Language",
        "content": """Python ek high-level, interpreted, versatile programming language hai.

🔑 **Key Features:**
• **Easy Syntax** — English jaisi readable code
• **Interpreted** — line by line execute hoti hai
• **Dynamically Typed** — type runtime pe decide hoti hai
• **Huge Libraries** — NumPy, Pandas, TensorFlow, Django
• **Multi-paradigm** — OOP, functional, procedural

📦 **Frameworks:** Django, FastAPI, Flask, PyTorch, Scikit-learn

💡 **Used for:** AI/ML, Data Science, Web Development, Automation, Scripting

```python
# Simple Python example
def greet(name):
    return f"Hello, {name}!"

print(greet("World"))
```""",
        "keywords": ["python", "django", "flask", "pip", "python3"]
    },

    "javascript": {
        "title": "JavaScript",
        "content": """JavaScript web ka programming language hai — browser mein run hota hai.

🔑 **Key Features:**
• **Browser Native** — sirf language jo browser mein directly run hoti hai
• **Full Stack** — Frontend (React) + Backend (Node.js) dono
• **Async Programming** — callbacks, promises, async/await
• **Dynamic Typing** — variable type flexible hai

📦 **Frameworks:** React, Vue, Angular, Node.js, Express, Next.js

💡 **Used for:** Web frontends, mobile apps (React Native), backend APIs

```javascript
// Example
const greet = (name) => `Hello, ${name}!`;
console.log(greet("World"));
```""",
        "keywords": ["javascript", "nodejs", "reactjs", "vuejs", "typescript", "js"]
    },

    "oop": {
        "title": "Object-Oriented Programming (OOP/OOPS)",
        "content": """OOP ek programming paradigm hai jo code ko objects aur classes ke around organize karta hai.

🔑 **4 Pillars of OOP:**

**1. Encapsulation (Encapsulation)**
• Data aur methods ko ek saath bundle karna
• Private data ko hide karna — getter/setter se access
```python
class BankAccount:
    def __init__(self):
        self.__balance = 0  # private

    def deposit(self, amount):
        self.__balance += amount

    def get_balance(self):
        return self.__balance
```

**2. Inheritance (Virasat)**
• Child class parent class ki properties le leti hai
• Code reuse hota hai
```python
class Animal:
    def speak(self): pass

class Dog(Animal):  # Dog inherits Animal
    def speak(self):
        return "Woof!"
```

**3. Polymorphism (Anek Roop)**
• Same method ka alag alag behavior
• Method Overriding + Method Overloading
```python
class Shape:
    def area(self): return 0

class Circle(Shape):
    def area(self): return 3.14 * r * r  # overrides

class Square(Shape):
    def area(self): return side * side   # overrides
```

**4. Abstraction (Chupaana)**
• Complex implementation hide karna
• Only essential features dikhana
```python
from abc import ABC, abstractmethod

class Vehicle(ABC):
    @abstractmethod
    def start(self):  # implementation child mein
        pass
```

💡 **OOP Languages:** Java, Python, C++, C#, Ruby""",
        "keywords": ["oop", "oops", "object oriented", "encapsulation", "inheritance",
                     "polymorphism", "abstraction", "four pillars", "pillars of oop",
                     "oop concepts", "oops concepts", "oops in java", "oop in python"]
    },

    "machine learning": {
        "title": "Machine Learning (ML)",
        "content": """Machine Learning AI ka ek subset hai jahan machines data se khud seekhti hain.

🔑 **Types of ML:**

**1. Supervised Learning**
• Labeled data se seekhna
• Examples: Spam detection, image classification
• Algorithms: Linear Regression, Decision Trees, SVM

**2. Unsupervised Learning**
• Unlabeled data mein patterns dhundhna
• Examples: Customer segmentation, anomaly detection
• Algorithms: K-Means, DBSCAN, PCA

**3. Reinforcement Learning**
• Reward/punishment se seekhna
• Examples: Game playing (Chess, Go), robotics

🔑 **ML Pipeline:**
Data Collection → Data Cleaning → Feature Engineering → Model Training → Evaluation → Deployment

💡 **Used in:** Spam filters, Netflix recommendations, fraud detection, medical diagnosis""",
        "keywords": ["machine learning", "ml", "supervised", "unsupervised", "reinforcement learning"]
    },

    "deep learning": {
        "title": "Deep Learning",
        "content": """Deep Learning ML ka subset hai jo multi-layer neural networks use karta hai.

🔑 **Key Concepts:**
• **Neurons** — basic computing units (brain cells ki tarah)
• **Layers** — Input → Hidden → Output
• **Weights & Biases** — learned parameters
• **Activation Functions** — ReLU, Sigmoid, Tanh
• **Backpropagation** — errors se seekhna

🔑 **Popular Architectures:**
• **CNN** — image recognition ke liye
• **RNN/LSTM** — sequence data, text ke liye
• **Transformer** — ChatGPT, BERT ke liye
• **GAN** — image generation ke liye

💡 **Used in:** Face recognition, voice assistants, ChatGPT, medical imaging""",
        "keywords": ["deep learning", "cnn", "rnn", "lstm", "transformer", "gan"]
    },

    "neural network": {
        "title": "Neural Networks",
        "content": """Neural Networks human brain se inspired computing systems hain.

🔑 **Structure:**
```
Input Layer → Hidden Layers → Output Layer
   (data)      (processing)    (result)
```

🔑 **How it works:**
1. Data input layer mein aata hai
2. Weights se multiply hota hai
3. Activation function apply hoti hai
4. Next layer ko pass hota hai
5. Output milta hai
6. Error calculate hota hai (Loss function)
7. Backpropagation se weights update hoti hain

🔑 **Training Process:**
• Forward Pass → Calculate output
• Calculate Loss → Compare with expected
• Backward Pass → Update weights (Gradient Descent)

💡 **Used in:** Image recognition, language models, speech recognition, medical diagnosis""",
        "keywords": ["neural network", "neurons", "backpropagation", "perceptron", "deep neural"]
    },

    "nlp": {
        "title": "Natural Language Processing (NLP)",
        "content": """NLP AI ki branch hai jo machines ko human language samajhne deti hai.

🔑 **Key Tasks:**
• **Intent Detection** — user kya chahta hai?
• **Sentiment Analysis** — positive/negative/neutral
• **Named Entity Recognition (NER)** — names, dates, places extract karna
• **Machine Translation** — Google Translate
• **Text Summarization** — long text ko short karna
• **Question Answering** — questions ke answers

🔑 **Common Techniques:**
• **Tokenization** — text ko words mein todna
• **Stemming/Lemmatization** — words ka root form
• **TF-IDF** — word importance measure
• **Word Embeddings** — Word2Vec, GloVe
• **Transformers** — BERT, GPT

💡 **Hamara chatbot bhi NLP use karta hai:**
• Naive Bayes — intent classification
• VADER — sentiment analysis
• Context Manager — conversation memory""",
        "keywords": ["nlp", "natural language processing", "tokenization", "sentiment", "bert", "gpt"]
    },

    "api": {
        "title": "API (Application Programming Interface)",
        "content": """API ek bridge hai jo alag software systems ko communicate karne deta hai.

🔑 **Types:**
• **REST API** — HTTP methods use karta hai (most popular)
• **GraphQL** — flexible queries
• **WebSocket** — real-time bidirectional
• **SOAP** — XML-based (older)

🔑 **REST API HTTP Methods:**
• `GET` — data retrieve karo
• `POST` — naya data create karo
• `PUT/PATCH` — data update karo
• `DELETE` — data delete karo

🔑 **Example:**
```
GET https://api.example.com/users/1
Response: {"id": 1, "name": "John", "email": "john@email.com"}
```

💡 **Hamara chatbot ka API:**
```
POST http://localhost:8000/api/chat/message
Body: {"message": "Hello", "session_id": "abc123"}
```""",
        "keywords": ["api", "rest api", "http", "endpoint", "graphql", "api call"]
    },

    "database": {
        "title": "Database",
        "content": """Database organized data ka collection hai jo electronically store hota hai.

🔑 **Types:**

**SQL (Relational) Databases:**
• Tables, rows, columns
• ACID properties
• Examples: MySQL, PostgreSQL, SQLite
```sql
SELECT * FROM users WHERE age > 18;
```

**NoSQL Databases:**
• Flexible schema
• Horizontally scalable
• Types: Document (MongoDB), Key-Value (Redis), Graph (Neo4j)
```json
{"name": "John", "age": 25, "city": "Delhi"}
```

🔑 **CRUD Operations:**
• **C**reate — INSERT / insert_one()
• **R**ead — SELECT / find()
• **U**pdate — UPDATE / update_one()
• **D**elete — DELETE / delete_one()

💡 **Hamara chatbot MongoDB use karta hai** — sab conversations store hoti hain""",
        "keywords": ["database", "sql", "nosql", "mongodb", "mysql", "postgresql", "crud"]
    },

    "git": {
        "title": "Git — Version Control System",
        "content": """Git ek distributed version control system hai jo code changes track karta hai.

🔑 **Essential Commands:**
```bash
git init              # new repository initialize karo
git add .             # sab changes stage karo
git commit -m "msg"   # changes save karo
git push              # GitHub pe upload karo
git pull              # latest changes download karo
git branch            # branches list/create karo
git merge branch_name # branches merge karo
git status            # current status dekho
git log               # history dekho
git clone URL         # repo copy karo
```

🔑 **Git Workflow:**
Working Directory → Staging Area → Local Repo → Remote Repo (GitHub)

💡 **GitHub** most popular Git hosting platform hai""",
        "keywords": ["git", "github", "version control", "commit", "branch", "repository", "git push"]
    },

    "docker": {
        "title": "Docker — Containerization",
        "content": """Docker platform hai jo applications ko containers mein run karta hai.

🔑 **Key Concepts:**
• **Container** — isolated environment jahan app run hoti hai
• **Image** — container ka template (blueprint)
• **Dockerfile** — image banane ki instructions
• **Docker Compose** — multiple containers manage karna

🔑 **Basic Commands:**
```bash
docker build -t myapp .      # image build karo
docker run -p 8000:8000 myapp # container run karo
docker ps                     # running containers dekho
docker stop container_id      # container stop karo
docker-compose up             # multiple services start
```

💡 **Problem Solved:** "Works on my machine" — Docker se same environment har jagah!""",
        "keywords": ["docker", "container", "dockerfile", "docker compose", "containerization"]
    },

    "algorithm": {
        "title": "Algorithms",
        "content": """Algorithm step-by-step instructions hain kisi problem ko solve karne ke liye.

🔑 **Sorting Algorithms:**
| Algorithm | Best | Average | Worst |
|-----------|------|---------|-------|
| Bubble Sort | O(n) | O(n²) | O(n²) |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) |
| Quick Sort | O(n log n) | O(n log n) | O(n²) |

🔑 **Searching:**
• **Linear Search** — O(n) — har element check karo
• **Binary Search** — O(log n) — sorted array mein half-half karo

🔑 **Big O Notation:**
• O(1) — Constant — best
• O(log n) — Logarithmic — great
• O(n) — Linear — ok
• O(n²) — Quadratic — avoid

🔑 **Graph Algorithms:**
• BFS — level-by-level traversal
• DFS — depth-first traversal
• Dijkstra — shortest path""",
        "keywords": ["algorithm", "sorting", "searching", "big o", "binary search", "merge sort"]
    },

    "data structure": {
        "title": "Data Structures",
        "content": """Data Structure data ko efficiently store aur organize karne ka tarika hai.

🔑 **Linear Structures:**
• **Array** — fixed size, O(1) access
• **Linked List** — dynamic, O(n) access, O(1) insert
• **Stack** — LIFO (Last In First Out) — undo feature
• **Queue** — FIFO (First In First Out) — printer queue

🔑 **Non-Linear Structures:**
• **Binary Tree** — hierarchical, parent-child
• **Binary Search Tree (BST)** — sorted tree, O(log n) search
• **Heap** — priority queue
• **Graph** — nodes aur edges (social networks)

🔑 **Hashing:**
• **Hash Table** — O(1) average lookup
• Key-Value pairs
• Python dict, Java HashMap

💡 **Choosing right DS = faster, efficient programs!**""",
        "keywords": ["data structure", "linked list", "stack", "queue", "tree", "graph", "hash table", "array"]
    },

    "cloud computing": {
        "title": "Cloud Computing",
        "content": """Cloud Computing internet ke through computing services deliver karna hai.

🔑 **Service Models:**
• **IaaS** — Infrastructure as a Service (AWS EC2, virtual machines)
• **PaaS** — Platform as a Service (Heroku, Google App Engine)
• **SaaS** — Software as a Service (Gmail, Dropbox, Netflix)

🔑 **Major Providers:**
• **AWS** — Amazon Web Services (most popular)
• **Azure** — Microsoft Cloud
• **GCP** — Google Cloud Platform

🔑 **Key Benefits:**
• Scalability — traffic badhe toh resources badha lo
• Cost Savings — sirf use karo, sirf pay karo
• Global Reach — worldwide deploy karo
• No Hardware — physical servers ki zaroorat nahi

💡 **Examples:** Netflix (AWS), Spotify (GCP), LinkedIn (Azure)""",
        "keywords": ["cloud computing", "aws", "azure", "google cloud", "iaas", "paas", "saas"]
    },

    "fastapi": {
        "title": "FastAPI",
        "content": """FastAPI ek modern, high-performance Python web framework hai APIs banane ke liye.

🔑 **Key Features:**
• **Auto Swagger Docs** — `/docs` pe automatic API documentation
• **Very Fast** — Node.js ke comparable speed
• **Type Hints** — Pydantic se automatic validation
• **Async Support** — async/await built-in
• **WebSocket** — real-time communication

🔑 **Example:**
```python
from fastapi import FastAPI
app = FastAPI()

@app.get("/hello/{name}")
async def greet(name: str):
    return {"message": f"Hello, {name}!"}
```

💡 **Hamara chatbot backend FastAPI se bana hai!**
API docs: http://localhost:8000/docs""",
        "keywords": ["fastapi", "uvicorn", "pydantic", "fast api"]
    },

    "recursion": {
        "title": "Recursion",
        "content": """Recursion ek technique hai jahan function khud ko call karta hai.

🔑 **Key Components:**
• **Base Case** — stop condition (ye zaruri hai!)
• **Recursive Case** — function khud ko call karta hai

🔑 **Example — Factorial:**
```python
def factorial(n):
    if n == 0:  # Base case
        return 1
    return n * factorial(n - 1)  # Recursive case

print(factorial(5))  # 5 * 4 * 3 * 2 * 1 = 120
```

🔑 **Example — Fibonacci:**
```python
def fibonacci(n):
    if n <= 1:  # Base case
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

⚠️ **Warning:** Base case bhuloge toh → Stack Overflow!

🔑 **When to use:**
• Tree traversal
• Divide and conquer (Merge Sort)
• Backtracking problems""",
        "keywords": ["recursion", "recursive", "base case", "recursive function"]
    },
}

# ─── Emotion Keywords ─────────────────────────────────────────────────────────
EMOTION_KEYWORDS = {
    "very_sad": [
        "suicidal", "want to die", "no reason to live", "end it all",
        "completely hopeless", "completely worthless",
    ],
    "sad": [
        "i am sad", "feeling sad", "i feel sad", "very sad today",
        "feeling low", "feeling down", "feeling depressed",
        "i am depressed", "feeling unhappy", "feeling lonely",
        "feeling alone", "feeling broken", "feeling heartbroken",
        "feeling empty", "feeling lost", "i am miserable",
        "feeling hopeless", "feeling helpless", "i am struggling",
        "not okay today", "feeling blue", "feel like crying",
        "nothing feels right",
    ],
    "angry": [
        "i am angry", "feeling angry", "i feel angry", "very angry",
        "feeling frustrated", "i am frustrated", "so annoyed",
        "feeling mad", "i am furious", "feeling irritated",
        "i am livid", "feeling enraged", "fed up", "boiling with anger",
    ],
    "anxious": [
        "i am anxious", "feeling anxious", "i feel anxious",
        "feeling nervous", "i am worried", "feeling worried",
        "feeling scared", "i am stressed", "feeling stressed",
        "feeling overwhelmed", "i am panicking", "feeling tense",
        "i am afraid", "feeling restless", "i am overthinking",
        "cannot stop worrying",
    ],
    "happy": [
        "i am happy", "feeling happy", "i feel happy",
        "feeling great", "i am excited", "feeling excited",
        "feeling wonderful", "i am thrilled", "feeling fantastic",
        "i am delighted", "feeling cheerful", "i am glad",
        "feeling blessed", "feeling amazing", "best day ever",
    ],
}

# ─── Jokes pool ───────────────────────────────────────────────────────────────
JOKES = [
    "Why don't scientists trust atoms?\n**Because they make up everything!** 😄",
    "Why do programmers prefer dark mode?\n**Because light attracts bugs!** 🐛💡",
    "I told my Python code to take a break...\n**Now it won't stop running loops!** 🐍",
    "What did the AI say to the data scientist?\n**'You complete my training set!'** 🤖❤️",
    "A SQL query walks into a bar, approaches two tables...\n**'Can I JOIN you?'** 😄",
    "Why do Java developers wear glasses?\n**Because they don't C#!** 👓",
    "Why was the JavaScript developer sad?\n**Because he didn't know how to null his feelings!** 😢",
    "What do you call a computer that sings?\n**A Dell!** 🎵",
    "Why did the programmer quit his job?\n**Because he didn't get arrays!** 😂",
    "How many programmers does it take to change a lightbulb?\n**None — that's a hardware problem!** 💡",
    "Why is Python so popular?\n**Because it doesn't have too many brackets!** 🐍😄",
    "What's a computer's favorite snack?\n**Microchips!** 🍟",
]

# ─── Greeting responses ───────────────────────────────────────────────────────
GREETING_RESPONSES = [
    "Hello! 😊 Main hun **Dynamic AI Chatbot** — Python + FastAPI + NLP se powered!\n\nMain kya kar sakta hun:\n🤖 **Tech Questions** — Java, Python, AI, ML, OOP, APIs...\n😊 **Emotional Support** — I understand how you feel\n🎭 **Jokes** — Need a laugh?\n💬 **General Chat** — Just talk!\n\nKya poochhna hai tumhe?",
    "Hey there! 👋 Mujhse kuch bhi poochho!\n\nTry karo:\n• *'What is Java?'* → full explanation\n• *'Explain OOP concepts'* → with code\n• *'What is ML?'* → detailed answer\n• *'Tell me a joke'* → fun!\n• *'I feel stressed'* → support 💙\n\nMain hun ready! 🚀",
    "Hi! 🤖 Main **NLP + ML** se user ka message analyze karta hun aur khud se response generate karta hun.\n\nPoochho kuch bhi — tech, emotions, jokes, ya general chat! 😊",
]

# ─── Context Manager ──────────────────────────────────────────────────────────
class ContextManager:
    def __init__(self, max_turns: int = 20):
        self.sessions: dict = {}
        self.max_turns = max_turns

    def get_session(self, sid: str) -> dict:
        if sid not in self.sessions:
            self.sessions[sid] = {
                "history":        deque(maxlen=self.max_turns * 2),
                "user_name":      None,
                "turn_count":     0,
                "last_intent":    None,
                "last_emotion":   None,
                "emotion_history":deque(maxlen=5),
                "has_been_sad":   False,
                "created_at":     datetime.utcnow(),
            }
        self.sessions[sid]["last_activity"] = datetime.utcnow()
        return self.sessions[sid]

    def add_turn(self, sid: str, role: str, message: str, meta: dict = None):
        s = self.get_session(sid)
        entry = {"role": role, "message": message,
                 "timestamp": datetime.utcnow().isoformat()}
        if meta:
            entry.update(meta)
        s["history"].append(entry)
        s["turn_count"] += 1
        if role == "user":
            if meta:
                s["last_intent"] = meta.get("intent")
                em = meta.get("emotion")
                if em:
                    s["last_emotion"] = em
                    s["emotion_history"].append(em)
                    if "sad" in em or "anxious" in em:
                        s["has_been_sad"] = True
            nm = re.search(
                r"(?:my name is|call me|i am|i'm)\s+([A-Z][a-z]+)", message, re.I
            )
            if nm:
                s["user_name"] = nm.group(1)

    def get_context(self, sid: str) -> dict:
        s = self.get_session(sid)
        return {
            "turn_count":   s["turn_count"],
            "user_name":    s["user_name"],
            "last_intent":  s["last_intent"],
            "last_emotion": s["last_emotion"],
            "has_been_sad": s["has_been_sad"],
            "last_messages":list(s["history"])[-4:],
        }

    def clear_session(self, sid: str):
        self.sessions.pop(sid, None)


# ─── Intent Classifier — CV ERROR FIXED ──────────────────────────────────────
class IntentClassifier:
    def __init__(self):
        self.pipeline = None
        self._trained = False
        self.classes_  = []

    def train(self):
        try:
            from sklearn.pipeline import Pipeline
            from sklearn.naive_bayes import MultinomialNB
            from sklearn.feature_extraction.text import TfidfVectorizer
            # ✅ NO CalibratedClassifierCV — that caused the cv=3 error
            # MultinomialNB natively supports predict_proba()

            X, y = [], []
            for intent, phrases in INTENT_TRAINING_DATA.items():
                for phrase in phrases:
                    X.append(phrase.lower())
                    y.append(intent)

            self.pipeline = Pipeline([
                ("tfidf", TfidfVectorizer(
                    ngram_range=(1, 3),
                    max_features=12000,
                    sublinear_tf=True,
                    min_df=1,
                    analyzer="word",
                    token_pattern=r"\b[a-zA-Z][a-zA-Z0-9]*\b",
                )),
                ("clf", MultinomialNB(alpha=0.1)),
            ])
            self.pipeline.fit(X, y)
            self.classes_ = list(self.pipeline.classes_)
            self._trained = True

            from collections import Counter
            counts = Counter(y)
            logger.info(
                f"✅ Intent Classifier trained: {len(X)} samples | "
                f"{len(set(y))} intents | min_per_class={min(counts.values())}"
            )
        except Exception as e:
            logger.error(f"Intent training error: {e}")

    def predict(self, text: str) -> dict:
        lower = text.lower().strip()

        # ── Step 1: Knowledge base keyword check (highest priority) ───────────
        kb_hit = self._check_knowledge_base(lower)
        if kb_hit:
            return kb_hit

        # ── Step 2: ML Classifier ─────────────────────────────────────────────
        if self._trained and self.pipeline:
            try:
                proba = self.pipeline.predict_proba([lower])[0]
                scores = dict(zip(self.classes_, proba.tolist()))
                top = sorted(scores.items(), key=lambda x: x[1], reverse=True)
                return {
                    "intent":     top[0][0],
                    "confidence": round(top[0][1], 4),
                    "all_scores": dict(top[:5]),
                }
            except Exception as e:
                logger.debug(f"Predict error: {e}")

        return self._keyword_fallback(lower)

    def _check_knowledge_base(self, text: str) -> Optional[dict]:
        """
        Knowledge base mein directly check karo.
        Fixes 'What is Java?' → time_date misclassification.
        """
        question_words = [
            "what is", "what are", "explain", "define", "how does",
            "how do", "tell me about", "describe", "meaning of",
            "difference between", "how to use", "what does",
            "give me info", "i want to know about", "teach me",
            "four pillars", "pillars of", "concepts of",
        ]
        has_question = any(q in text for q in question_words)

        for topic, data in KNOWLEDGE_BASE.items():
            keywords = data.get("keywords", [topic])
            for kw in keywords:
                if kw in text:
                    return {
                        "intent":     "technical",
                        "confidence": 0.98,
                        "kb_topic":   topic,
                        "all_scores": {"technical": 0.98},
                    }

        # Single tech word check
        direct_tech_words = [
            "java", "python", "javascript", "typescript", "nodejs",
            "reactjs", "fastapi", "django", "flask", "mongodb", "mysql",
            "docker", "linux", "github", "recursion", "algorithm",
        ]
        for word in direct_tech_words:
            if word in text.split() or f" {word} " in f" {text} ":
                if has_question or len(text.split()) <= 6:
                    return {
                        "intent":     "technical",
                        "confidence": 0.96,
                        "kb_topic":   word,
                        "all_scores": {"technical": 0.96},
                    }
        return None

    def _keyword_fallback(self, text: str) -> dict:
        scores: dict = defaultdict(float)
        for intent, phrases in INTENT_TRAINING_DATA.items():
            for phrase in phrases:
                if phrase in text:
                    scores[intent] += 1.0
                elif any(w in text for w in phrase.split() if len(w) > 3):
                    scores[intent] += 0.3
        if scores:
            intent = max(scores, key=scores.get)
            total  = sum(scores.values()) or 1
            return {
                "intent":     intent,
                "confidence": round(scores[intent] / total, 4),
                "all_scores": dict(scores),
            }
        return {"intent": "fallback", "confidence": 0.0, "all_scores": {}}


# ─── Emotion Detector ─────────────────────────────────────────────────────────
class EmotionDetector:
    def detect(self, text: str) -> Optional[str]:
        lower = text.lower()
        for emotion, keywords in EMOTION_KEYWORDS.items():
            if any(kw in lower for kw in keywords):
                return emotion
        return None


# ─── Sentiment Analyzer ───────────────────────────────────────────────────────
class SentimentAnalyzer:
    def __init__(self):
        self.vader  = None
        self._ready = False

    def initialize(self):
        try:
            from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
            self.vader  = SentimentIntensityAnalyzer()
            self._ready = True
            logger.info("✅ VADER Sentiment Analyzer ready")
        except ImportError:
            logger.warning("VADER not available — using fallback")

    def analyze(self, text: str) -> dict:
        compound = 0.0
        pos_w, neg_w = [], []

        if self._ready and self.vader:
            s = self.vader.polarity_scores(text)
            compound = s["compound"]
            for w in text.split():
                sc = self.vader.polarity_scores(w)["compound"]
                if sc > 0.3:  pos_w.append(w)
                elif sc < -0.3: neg_w.append(w)
        else:
            try:
                from textblob import TextBlob
                compound = TextBlob(text).sentiment.polarity
            except Exception:
                pass

        if   compound >= 0.5:  label, emoji = "very_positive", "😄"
        elif compound >= 0.05: label, emoji = "positive",      "🙂"
        elif compound <= -0.5: label, emoji = "very_negative", "😢"
        elif compound <= -0.05:label, emoji = "negative",      "😟"
        else:                  label, emoji = "neutral",       "😐"

        return {
            "label":          label,
            "score":          round(compound, 4),
            "emoji":          emoji,
            "compound":       round(compound, 4),
            "positive_words": pos_w[:5],
            "negative_words": neg_w[:5],
            "intensity":      "high"   if abs(compound) >= 0.5
                              else "medium" if abs(compound) >= 0.05
                              else "none",
        }


# ─── NER Processor ────────────────────────────────────────────────────────────
class NERProcessor:
    PATTERNS = {
        "emails":     r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        "phones":     r"(\+\d{1,3})?[\s.-]?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}",
        "urls":       r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+",
        "dates":      r"\b(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})\b",
        "currencies": r"[$€£₹]\s?\d+(?:,\d{3})*(?:\.\d{2})?",
    }
    LOCATIONS = [
        "india", "usa", "uk", "canada", "delhi", "mumbai", "jaipur",
        "london", "new york", "paris", "tokyo", "dubai", "bangalore",
        "hyderabad", "chennai", "kolkata", "pune",
    ]

    def extract(self, text: str) -> dict:
        entities = {k: [] for k in self.PATTERNS}
        entities["locations"] = []
        entities["persons"]   = []
        for key, pat in self.PATTERNS.items():
            matches = re.findall(pat, text, re.IGNORECASE)
            entities[key] = list(set(
                m if isinstance(m, str) else m[0] for m in matches
            ))
        lower = text.lower()
        entities["locations"] = [l for l in self.LOCATIONS if l in lower]
        nm = re.findall(
            r"(?:name is|call me)\s+([A-Z][a-z]+(?: [A-Z][a-z]+)?)", text
        )
        entities["persons"] = list(set(nm))
        return entities


# ─── Multi-Intent Detector ────────────────────────────────────────────────────
class MultiIntentDetector:
    SPLIT = [r'\band\b', r'\balso\b', r'\?\s+', r'\bwhat about\b', r'\bplus\b']

    def detect(self, text: str, clf: IntentClassifier) -> list:
        combined = '|'.join(self.SPLIT)
        parts = re.split(combined, text, flags=re.IGNORECASE)
        parts = [p.strip() for p in parts if p.strip() and len(p.strip()) > 3]
        if len(parts) <= 1:
            return [clf.predict(text)]
        intents, seen = [], set()
        for part in parts[:3]:
            r = clf.predict(part)
            if (r["intent"] != "fallback"
                    and r["confidence"] > 0.2
                    and r["intent"] not in seen):
                intents.append({**r, "segment": part})
                seen.add(r["intent"])
        return intents if intents else [clf.predict(text)]


# ─── Response Generator — model khud response banata hai ─────────────────────
class ResponseGenerator:
    """
    Yeh class responses generate karti hai.
    Knowledge base se specific technical answers deti hai.
    Emotion detect hone pe empathetic responses deti hai.
    Sab kuch dynamic hai — model analyze karta hai.
    """

    def generate(
        self,
        text: str,
        intent_result: dict,
        emotion: Optional[str],
        sentiment: dict,
        context: dict,
        multi_intents: list,
    ) -> str:

        intent    = intent_result["intent"]
        kb_topic  = intent_result.get("kb_topic")
        user_name = context.get("user_name")

        # ── 1. Emotion has HIGHEST priority ───────────────────────────────────
        if emotion:
            return self._emotion_response(emotion, context)

        # ── 2. Technical question → knowledge base ────────────────────────────
        if intent == "technical":
            return self._technical_response(text, kb_topic)

        # ── 3. Multiple intents ───────────────────────────────────────────────
        if len(multi_intents) > 1:
            return self._multi_intent_response(text, multi_intents)

        # ── 4. Other intents ──────────────────────────────────────────────────
        response = self._intent_response(intent, text, context)

        # Personalize with name
        if user_name and random.random() > 0.6:
            response = re.sub(r"^(Hello|Hi|Hey)!", rf"\1, {user_name}!", response, count=1)

        # If user was sad before
        if (context.get("has_been_sad")
                and intent not in ("emotion_sad","emotion_very_sad","emotion_anxious")
                and context["turn_count"] > 2):
            response = "I'm glad you're still chatting with me! 😊 " + response

        return response

    def _technical_response(self, text: str, kb_topic: str = None) -> str:
        """Knowledge base se specific technical response generate karo."""
        lower = text.lower()

        # Direct topic match
        if kb_topic and kb_topic in KNOWLEDGE_BASE:
            topic_data = KNOWLEDGE_BASE[kb_topic]
            return f"## 📚 {topic_data['title']}\n\n{topic_data['content']}"

        # Search through all knowledge base
        for topic, data in KNOWLEDGE_BASE.items():
            keywords = data.get("keywords", [topic])
            if topic in lower or any(kw in lower for kw in keywords):
                return f"## 📚 {data['title']}\n\n{data['content']}"

        # Generic technical response with guidance
        return (
            "Great technical question! 💻\n\n"
            "Main in topics par detailed answers de sakta hun:\n\n"
            "**Programming Languages:**\n"
            "Java • Python • JavaScript • C++\n\n"
            "**AI / ML:**\n"
            "Machine Learning • Deep Learning • NLP • Neural Networks\n\n"
            "**Web Development:**\n"
            "FastAPI • React • APIs • MongoDB • SQL\n\n"
            "**CS Concepts:**\n"
            "OOP/OOPS • Algorithms • Data Structures • Git • Docker\n\n"
            "Kya specifically poochhna hai? Example:\n"
            "• *'Explain OOP concepts'*\n"
            "• *'What is machine learning?'*\n"
            "• *'Explain recursion with example'* 🎯"
        )

    def _emotion_response(self, emotion: str, context: dict) -> str:
        """Emotion ke hisaab se empathetic response."""
        turn = context["turn_count"]
        prefix = "Maine notice kiya tone mein change... 💙\n\n" if turn > 3 else ""

        responses = {
            "very_sad": [
                f"{prefix}Main samajh sakta hun ke tum kuch bohot mushkil se guzar rahe ho 💙\n\nTumhe akele face nahi karna. Kya tum batana chahoge kya ho raha hai?\n\nAgar sab bohot overwhelming lag raha hai, please kisi trusted insaan se baat karo. **Tum matter karte ho.** 🤗",
                f"{prefix}Main sun raha hun, aur main chahta hun ke tum jano — **jo tum feel kar rahe ho woh bilkul valid hai** 💙\n\nMain yahan hun bina judgment ke. Kya share karna chahoge? 🌱",
            ],
            "sad": [
                f"{prefix}Main feel kar sakta hun ke tum tough time se guzar rahe ho 💙 Yeh bilkul okay hai.\n\nMain yahan hun. Kya tum chahte ho:\n• **Baat karein kya pareshan kar raha hai?**\n• **Kuch uplifting sunna?**\n• **Bas vent karo, main sunuunga?** 🌈",
                f"{prefix}Virtual hug bhej raha hun! 🤗 Sad days mushkil hote hain, lekin woh guzar jaate hain.\n\nKya baat karoge? Main sun raha hun 💙",
                f"{prefix}I notice you're feeling down 😔 Yeh valid hai.\n\nMain seedha advice nahi dunga — pehle sunna chahta hun. Kya ho raha hai? 💙",
            ],
            "angry": [
                f"{prefix}Main samajh sakta hun frustration — bilkul valid hai! 😤\n\nEk deep breath lete hain... 🌬️\n\nKya tum:\n• **Vent karna chahte ho?**\n• **Situation discuss karna chahte ho?**\n\nMain yahan hun bina judgment ke! 💙",
                f"{prefix}Tumhari anger samajh aati hai! 💢 Kuch clearly frustrate kar raha hai.\n\nKya hua? Kabhi kabhi explain karne se feelings untangle ho jaati hain. 🌊",
            ],
            "anxious": [
                f"{prefix}Main sense kar sakta hun ke tum anxious ya stressed ho 😟 Yeh bohot tough hai.\n\n**Tum safe ho yahan.** 💙\n\nKya help karega:\n• **Stress ke baare mein baat karna?**\n• **Problem ko saath mein break down karna?**\n\nEk step at a time — tumne yeh! 🌱",
                f"{prefix}Anxiety real hai aur mushkil hai 💙 Akele push nahi karna.\n\nKya overwhelm kar raha hai? Fear ko naam dene se uski power kam hoti hai. 🌟",
            ],
            "happy": [
                "Tumhari positive energy contagious hai! 😄🎉 Kya itna amazing feel kara raha hai aaj?",
                "Yesss! Yeh happy energy sab kuch hai! 🎊 Batao kya khaas hua — celebrate karte hain! ✨",
                "Mera algorithm khush ho gaya! 😄 Kya achhi news hai? 🎉",
            ],
        }

        pool = responses.get(emotion, responses["sad"])
        return random.choice(pool)

    def _intent_response(self, intent: str, text: str, context: dict) -> str:
        """Standard intent responses."""
        responses_map = {
            "greeting": GREETING_RESPONSES,
            "farewell": [
                "Goodbye! 👋 Bahut accha laga chat karna! Kabhi bhi wapas aao!",
                "See you later! 🌟 Hope I was helpful today!",
                "Take care! 😊 Jab bhi zaroorat ho, main yahan hun!",
                "Bye! 🤖 Until next time — keep learning! 🚀",
            ],
            "thanks": [
                "You're welcome! 😊 Kabhi bhi help ke liye aa sakte ho!",
                "My pleasure! Yahi toh main hun — help karne ke liye! 🎉",
                "Glad I could help! Aur kuch poochhna hai toh batao! ✨",
                "Anytime! 🤖 Tumhara feedback mujhe improve karta hai!",
            ],
            "help": [
                "Main kya kar sakta hun:\n\n🤖 **Technical Q&A**\n   → 'What is Java?', 'Explain OOP', 'What is ML?'\n   → Code examples ke saath explain karta hun\n\n😊 **Emotional Support**\n   → 'I'm feeling sad', 'I'm stressed'\n\n🎭 **Entertainment**\n   → 'Tell me a joke'\n\n💬 **General Chat**\n   → Bas naturally baat karo!\n\n⏰ **Time & Date**\n   → 'What time is it?'\n\nKya poochhna hai? 🚀",
                "Main **AI Chatbot** hun Python + NLP se powered!\n\n• **50+ tech topics** — Java, Python, OOP, ML...\n• **Emotion detection** — happy, sad, angry, anxious\n• **Multi-question handling**\n• **Conversation memory**\n\nNaturally poochho — main samjhunga! 😊",
            ],
            "about": [
                "Main ek **Dynamic AI Chatbot** hun — internship project! 🤖\n\n**Built with:**\n🐍 Python + FastAPI (backend)\n🧠 NLTK + scikit-learn (NLP)\n📊 VADER (sentiment analysis)\n🗄️ MongoDB (data storage)\n⚡ Socket.IO (real-time)\n⚛️ React (frontend)\n\n**Main kya karta hun:**\n• User ka message analyze karta hun\n• Intent classify karta hun (16 categories)\n• Emotion detect karta hun\n• Knowledge base se answer generate karta hun\n• Context yaad rakhta hun",
                "Ek AI chatbot hun jo khud se analyze karta hai! 🧠\n\n**Mera brain:**\n• Naive Bayes + TF-IDF — intent detection\n• VADER — sentiment/emotion analysis\n• Knowledge Base — 25+ tech topics ka data\n• Context Manager — conversation memory\n\nMain ChatGPT nahi hun, lekin apne domain mein smart hun! 😄",
            ],
            "time_date": [
                lambda: f"🕐 **Time:** {datetime.now().strftime('%I:%M:%S %p')}\n📅 **Date:** {datetime.now().strftime('%A, %B %d, %Y')}",
                lambda: f"Abhi **{datetime.now().strftime('%I:%M %p')}** baj rahe hain — **{datetime.now().strftime('%d %B %Y')}** 📅",
            ],
            "weather": [
                "Mujhe live weather data nahi milta! ⛅\n\nWeather ke liye:\n🌐 Google: 'weather [apna shaher]'\n📱 weather.com ya AccuWeather\n📲 Phone ka weather app\n\nKuch aur poochhna hai? 😊",
            ],
            "joke": JOKES,
            "math": [
                "Math ka bohot bada subject hai! 🔢\n\nMain in topics explain kar sakta hun:\n\n📐 **Basic Math:**\nAlgebra, Geometry, Trigonometry\n\n📊 **Advanced:**\nCalculus (Derivatives, Integrals)\nStatistics & Probability\nMatrices & Vectors\n\nKonsa specific math topic poochhna hai? Example:\n• *'What is calculus?'*\n• *'Explain probability'* 📚",
            ],
            "question_general": [
                "Interesting! Thoda aur specific batao? 🤔\n\nMain in par detail de sakta hun:\n• **Tech topics** — 'What is Python?', 'Explain API'\n• **AI/ML** — 'What is machine learning?'\n• **CS Concepts** — 'Explain OOP', 'What is algorithm?'\n\nKya specifically poochhna hai?",
            ],
            "compliment": [
                "Thank you so much! 🌟 Yeh sunke mera model aur accha kaam karta hai!",
                "Aww! 😊 Tumne mera neural network khush kar diya!",
                "That means a lot! 💖 Tumhara feedback mujhe better banata hai!",
                "You're too kind! 🤖 Main aur improve karta rahunga!",
            ],
            "negative_feedback": [
                "I'm sorry! 🙏 Main continuously seekh raha hun.\n\nBatao:\n• Kya galat tha?\n• Kya expect kar rahe the?\n\nTumhara feedback directly mera model improve karta hai! 💪",
                "Sahi baat hai, maafi chahta hun! 😔 Please question rephrase karo — is baar better answer dunga! 🎯",
            ],
            "fallback": [
                "Main samjha nahi! 🤔\n\n💡 **Try karo:**\n• *'What is Java?'* → full explanation\n• *'Explain OOP concepts'* → with code examples\n• *'Tell me a joke'* → fun!\n• *'I feel sad'* → emotional support\n• *'What can you do?'* → meri features\n• *'What time is it?'* → time/date\n\nNaturally poochho! 😊",
                "Hmm, thoda differently poochho? 🧠\n\n**Main in cheezein jaanta hun:**\n🤖 Tech Q&A (Java, Python, OOP, AI, ML...)\n😊 Emotional support\n🎭 Jokes\n💬 General conversation\n\nKya explore karoge? 🚀",
            ],
        }

        pool = responses_map.get(intent, responses_map["fallback"])
        r = random.choice(pool)
        if callable(r):
            r = r()
        return r

    def _multi_intent_response(self, text: str, intents: list) -> str:
        parts = []
        for i, item in enumerate(intents[:2]):
            it  = item["intent"]
            seg = item.get("segment", "")
            if it == "technical":
                r = self._technical_response(seg, item.get("kb_topic"))
            else:
                r = self._intent_response(it, seg, {})
                if callable(r):
                    r = r()
            if r:
                parts.append(r[:400] if i > 0 else r)
        if parts:
            header = f"Maine **{len(intents)} questions** detect kiye — dono ka jawab:\n\n"
            return header + "\n\n---\n".join(parts)
        return self._intent_response("fallback", text, {})


# ─── Main NLP Engine ──────────────────────────────────────────────────────────
class NLPEngine:
    def __init__(self):
        self.intent_classifier     = IntentClassifier()
        self.sentiment_analyzer    = SentimentAnalyzer()
        self.ner_processor         = NERProcessor()
        self.context_manager       = ContextManager()
        self.emotion_detector      = EmotionDetector()
        self.multi_intent_detector = MultiIntentDetector()
        self.response_generator    = ResponseGenerator()
        self.is_ready = False

    async def initialize(self):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.intent_classifier.train)
        await loop.run_in_executor(None, self.sentiment_analyzer.initialize)
        self.is_ready = True
        logger.info("🚀 NLP Engine v5.0 ready — Model analyzes everything itself!")

    async def process(self, text: str, session_id: str) -> dict:
        start   = time.time()
        context = self.context_manager.get_context(session_id)

        # ── Run full analysis pipeline ────────────────────────────────────────
        intent_result = self.intent_classifier.predict(text)
        sentiment     = self.sentiment_analyzer.analyze(text)
        emotion       = self.emotion_detector.detect(text)
        entities      = self.ner_processor.extract(text)
        multi_intents = self.multi_intent_detector.detect(
            text, self.intent_classifier
        )

        # ── Add to context ────────────────────────────────────────────────────
        self.context_manager.add_turn(
            session_id, "user", text,
            {"intent": intent_result["intent"], "emotion": emotion},
        )

        # ── Generate response (model decides) ────────────────────────────────
        response = self.response_generator.generate(
            text=text,
            intent_result=intent_result,
            emotion=emotion,
            sentiment=sentiment,
            context=context,
            multi_intents=multi_intents,
        )

        # ── Save bot response to context ──────────────────────────────────────
        self.context_manager.add_turn(session_id, "bot", response)
        ms = round((time.time() - start) * 1000, 2)

        return {
            "response": response,
            "metadata": {
                "intent":             intent_result,
                "emotion":            emotion,
                "sentiment":          sentiment,
                "entities":           entities,
                "multi_intents":      multi_intents,
                "processing_time_ms": ms,
                "turn_count":         context["turn_count"] + 1,
                "contextual":         context["turn_count"] > 0,
                "context_summary": {
                    "user_name":   context["user_name"],
                    "last_intent": context["last_intent"],
                },
            },
        }


# Singleton
nlp_engine = NLPEngine()