import sqlite3
import os

DB_NAME = "database.db"


def get_db_connection():
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), DB_NAME))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()

    # Enable Foreign Keys
    c.execute("PRAGMA foreign_keys = ON;")

    # Users Table
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    # User Stats Table (Profile)
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS user_stats (
            user_id TEXT PRIMARY KEY,
            height REAL,
            weight REAL,
            goal TEXT,
            gender TEXT,
            bmi REAL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """
    )

    # Diet Plans Table
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS diet_plans (
            id TEXT PRIMARY KEY, -- e.g., 'balanced', 'keto'
            name TEXT NOT NULL,
            description TEXT
        )
    """
    )

    # Meals Table
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS meals (
            id TEXT PRIMARY KEY, -- e.g., 'oatmeal'
            diet_plan_id TEXT,
            day_type TEXT, -- 'weekday' or 'weekend'
            name TEXT NOT NULL,
            calories INTEGER,
            time TEXT,
            image_url TEXT,
            FOREIGN KEY (diet_plan_id) REFERENCES diet_plans (id)
        )
    """
    )

    # Meal Ingredients Table (One-to-Many for meals)
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS meal_ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meal_id TEXT,
            name TEXT,
            amount TEXT,
            FOREIGN KEY (meal_id) REFERENCES meals (id)
        )
    """
    )

    # User Logs (Water & Meals)
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS daily_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            date DATE,
            water_intake INTEGER DEFAULT 0,
            calories_consumed INTEGER DEFAULT 0,
            UNIQUE(user_id, date),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """
    )

    # Seed Initial Diet Data if empty
    c.execute("SELECT count(*) FROM diet_plans")
    if c.fetchone()[0] == 0:
        print("Seeding database...")

        # 1. Diet Plans
        diets = [
            ("balanced", "Balanced", "Mix of everything"),
            ("keto", "Keto / Low Carb", "High fat, low carb"),
            ("mediterranean", "Mediterranean", "Heart-healthy, plant-focused"),
            ("pescatarian", "Pescatarian", "Plant-based with seafood"),
            ("vegetarian", "Vegetarian", "Plant-based"),
            ("vegan", "Vegan", "Strictly plant-based"),
        ]
        c.executemany(
            "INSERT INTO diet_plans (id, name, description) VALUES (?, ?, ?)", diets
        )

        # 2. Meals (Balanced) - Weekdays
        balanced_weekdays = [
            (
                "oatmeal",
                "balanced",
                "weekdays",
                "Oatmeal with Berries",
                350,
                "08:00 AM Breakfast",
                "https://images.unsplash.com/photo-1517673132405-a56a62b18caf?q=80&w=800&auto=format&fit=crop",
            ),
            (
                "chicken_salad",
                "balanced",
                "weekdays",
                "Grilled Chicken Salad",
                450,
                "01:00 PM Lunch",
                "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?q=80&w=800&auto=format&fit=crop",
            ),
            (
                "steak",
                "balanced",
                "weekdays",
                "Steak and Veggies",
                600,
                "08:00 PM Dinner",
                "https://images.unsplash.com/photo-1600891964092-4316c288032e?q=80&w=800&auto=format&fit=crop",
            ),
            (
                "yogurt",
                "balanced",
                "weekdays",
                "Greek Yogurt & Granola",
                300,
                "08:00 AM Breakfast",
                "https://images.unsplash.com/photo-1488477181946-6428a0291777?q=80&w=800&auto=format&fit=crop",
            ),
            (
                "quinoa",
                "balanced",
                "weekdays",
                "Quinoa Bowl",
                500,
                "01:00 PM Lunch",
                "https://images.unsplash.com/photo-1546548970-71785318a17b?q=80&w=800&auto=format&fit=crop",
            ),
            (
                "salmon",
                "balanced",
                "weekdays",
                "Baked Salmon",
                550,
                "08:00 PM Dinner",
                "https://images.unsplash.com/photo-1467003909585-2f8a7270028d?q=80&w=800&auto=format&fit=crop",
            ),
        ]
        c.executemany(
            "INSERT INTO meals (id, diet_plan_id, day_type, name, calories, time, image_url) VALUES (?, ?, ?, ?, ?, ?, ?)",
            balanced_weekdays,
        )

        # 3. Meals (Balanced) - Weekend
        balanced_weekend = [
            (
                "pancakes",
                "balanced",
                "weekend",
                "Protein Pancakes",
                500,
                "09:00 AM Brunch",
                "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?q=80&w=800&auto=format&fit=crop",
            ),
            (
                "burger",
                "balanced",
                "weekend",
                "Cheat Day Burger",
                850,
                "02:00 PM Lunch",
                "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?q=80&w=800&auto=format&fit=crop",
            ),
            (
                "pizza",
                "balanced",
                "weekend",
                "Homemade Pizza",
                900,
                "08:00 PM Dinner",
                "https://images.unsplash.com/photo-1513104890138-7c749659a591?q=80&w=800&auto=format&fit=crop",
            ),
        ]
        c.executemany(
            "INSERT INTO meals (id, diet_plan_id, day_type, name, calories, time, image_url) VALUES (?, ?, ?, ?, ?, ?, ?)",
            balanced_weekend,
        )

        # 4. Ingredients
        ingredients = [
            ("oatmeal", "Oats", "1 cup"),
            ("oatmeal", "Fresh Berries", "1/2 cup"),
            ("oatmeal", "Honey", "1 tbsp"),
            ("oatmeal", "Almond Milk", "1 cup"),
            ("chicken_salad", "Grilled Chicken", "150g"),
            ("chicken_salad", "Romaine Lettuce", "2 cups"),
            ("chicken_salad", "Cherry Tomatoes", "1/2 cup"),
            ("chicken_salad", "Olive Oil", "1 tbsp"),
            ("steak", "Sirloin Steak", "200g"),
            ("steak", "Asparagus", "100g"),
            ("steak", "Baby Potatoes", "150g"),
            ("steak", "Garlic Butter", "1 tbsp"),
            ("yogurt", "Greek Yogurt", "1 cup"),
            ("yogurt", "Granola", "1/2 cup"),
            ("yogurt", "Honey", "1 tsp"),
            ("quinoa", "Quinoa", "1 cup"),
            ("quinoa", "Chickpeas", "1/2 cup"),
            ("quinoa", "Avocado", "1/2"),
            ("quinoa", "Tahini Dressing", "2 tbsp"),
            ("salmon", "Salmon Fillet", "150g"),
            ("salmon", "Broccoli", "100g"),
            ("salmon", "Lemon", "1 wedge"),
            ("salmon", "Brown Rice", "1/2 cup"),
            ("pancakes", "Protein Powder", "1 scoop"),
            ("pancakes", "Oats", "1/2 cup"),
            ("pancakes", "Egg", "1"),
            ("pancakes", "Banana", "1"),
            ("burger", "Beef Patty", "150g"),
            ("burger", "Cheese", "1 slice"),
            ("burger", "Bun", "1"),
            ("burger", "Fries", "100g"),
            ("pizza", "Dough", "200g"),
            ("pizza", "Tomato Sauce", "1/2 cup"),
            ("pizza", "Mozzarella", "100g"),
            ("pizza", "Basil", "Fresh"),
        ]
        c.executemany(
            "INSERT INTO meal_ingredients (meal_id, name, amount) VALUES (?, ?, ?)",
            ingredients,
        )

    # GYM TABLES
    c.execute(
        """
    CREATE TABLE IF NOT EXISTS workouts (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        type TEXT NOT NULL,
        duration_min INTEGER,
        calories_burn INTEGER,
        image_url TEXT
    )
    """
    )

    c.execute(
        """
    CREATE TABLE IF NOT EXISTS user_workouts (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        workout_id TEXT NOT NULL,
        date TEXT NOT NULL,
        status TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (workout_id) REFERENCES workouts (id)
    )
    """
    )

    conn.commit()
    conn.close()
    print("Database initialized successfully.")


if __name__ == "__main__":
    init_db()
