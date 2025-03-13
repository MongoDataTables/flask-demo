from pymongo import MongoClient
from datetime import datetime
import random
import uuid

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['myDatabase']
collection = db['dystopianNovels']

# Clear existing data
collection.delete_many({})

# Lists for generating dystopian novel data
titles_prefix = [
    "The Last", "Forgotten", "Shattered", "The Dark", "Silent", "Stolen",
    "Broken", "Toxic", "Digital", "Electric", "The Final", "Radioactive",
    "Mechanical", "Synthetic", "Hollow", "Chrome", "Lost", "Frozen", "Neon",
    "Encrypted", "Fractured", "Glitched", "Virtual", "Wasted", "Carbon"
]

titles_suffix = [
    "Sky", "Earth", "Memory", "City", "Dawn", "Echo", "Waters", "Sun", "Horizon",
    "Republic", "Eden", "Protocol", "Algorithm", "Society", "Regime", "Directive",
    "Future", "System", "Colony", "State", "Citizen", "Order", "Nation", "Domain"
]

authors_first = [
    "Alex", "Morgan", "Jordan", "Casey", "Riley", "Quinn", "Avery", "Taylor",
    "Cameron", "Dakota", "Harper", "Skyler", "Reese", "Ellis", "Rowan", "Phoenix",
    "Blake", "Hayden", "Parker", "Zion", "Emerson", "Nova", "Sage", "Winter"
]

authors_last = [
    "Zhang", "Patel", "Kim", "Singh", "Chen", "Nguyen", "Rodriguez", "Smith",
    "Ivanov", "Garcia", "Nakamura", "Jones", "Kowalski", "Müller", "Adeyemi",
    "Santos", "Dubois", "Wilson", "Ahmed", "Cohen", "Novak", "Diaz", "Jackson"
]

themes = [
    "Environmental collapse", "Surveillance state", "Artificial intelligence takeover",
    "Post-apocalyptic survival", "Totalitarian government", "Corporate control",
    "Biological warfare aftermath", "Digital consciousness", "Class warfare",
    "Genetic engineering", "Mind control", "Resource depletion", "Technological dependence",
    "Social media dystopia", "Reality manipulation", "Memory erasure", "Pandemic aftermath",
    "Climate disaster", "Robotic revolution", "Virtual reality imprisonment"
]

ratings = [2.5, 3.0, 3.5, 4.0, 4.5, 5.0]

# Generate novel data
novels = []
for i in range(2000000):
    # Create title and author
    title = f"{random.choice(titles_prefix)} {random.choice(titles_suffix)}"
    author = f"{random.choice(authors_first)} {random.choice(authors_last)}"

    # Generate random publication date between 1950 and 2024
    year = random.randint(1950, 2024)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    pub_date = datetime(year, month, day)

    # Generate page count
    pages = random.randint(180, 800)

    # Select themes - between 1 and 3 unique themes
    novel_themes = random.sample(themes, random.randint(1, 3))

    # Rating
    rating = random.choice(ratings)

    # Description - generated with some variation
    theme_text = " and ".join(novel_themes).lower()
    descriptions = [
        f"A haunting exploration of {theme_text} in a world where humanity's future hangs by a thread.",
        f"When society collapsed, the only thing left was {theme_text}. A stark warning of what might come.",
        f"Set in a future where {theme_text} has forever changed what it means to be human.",
        f"A chilling narrative exploring {theme_text} and the resilience of the human spirit.",
        f"In the aftermath of {theme_text}, one person's journey reveals the dark truth of our present."
    ]
    description = random.choice(descriptions)

    # Create a unique ID
    novel_id = f"DYST-{uuid.uuid4().hex[:8].upper()}"

    novels.append({
        'NovelId': novel_id,
        'Title': title,
        'Author': author,
        'PublishedDate': pub_date,
        'Pages': pages,
        'Themes': novel_themes,
        'Rating': rating,
        'Description': description
    })

# Insert into MongoDB
result = collection.insert_many(novels)
print(f"Inserted {len(result.inserted_ids)} dystopian novels into the database")

# Print a sample document for verification
print("\nSample document:")
print(collection.find_one())