import datetime
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
import uuid
from Backend.database import init_db, get_db_connection

app = Flask(__name__, static_folder="../")
CORS(app)

# Initialize Database on Startup
if not os.path.exists("database.db"):
    init_db()


@app.route("/")
def index():
    return send_from_directory(directory="../Frontend", path="index.html")


# ----------------------------------------------------------------------
# API ENDPOINTS
# ----------------------------------------------------------------------


# 1. AUTHENTICATION
@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Check if user already exists
        existing_user = cursor.execute(
            "SELECT id, name FROM users WHERE email = ?", (data["email"],)
        ).fetchone()

        if existing_user:
            # Return existing user details if email matches
            conn.close()
            return (
                jsonify(
                    {
                        "message": "User already exists. Logging in.",
                        "user_id": existing_user["id"],
                        "name": existing_user["name"],
                    }
                ),
                200,
            )

        # Create new user with UUID
        user_id = str(uuid.uuid4())
        cursor.execute(
            "INSERT INTO users (id, name, email, password) VALUES (?, ?, ?, ?)",
            (user_id, data["name"], data["email"], data["password"]),
        )

        # Initialize stats
        cursor.execute("INSERT INTO user_stats (user_id) VALUES (?)", (user_id,))
        conn.commit()
        return (
            jsonify(
                {"message": "User created", "user_id": user_id, "name": data["name"]}
            ),
            201,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()


@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    conn = get_db_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE email = ? AND password = ?",
        (data["email"], data["password"]),
    ).fetchone()
    conn.close()

    if user:
        return (
            jsonify(
                {
                    "message": "Login successful",
                    "user_id": user["id"],
                    "name": user["name"],
                }
            ),
            200,
        )
    else:
        return jsonify({"error": "Invalid credentials"}), 401


@app.route("/api/forgot-password", methods=["POST"])
def forgot_password():
    data = request.json
    email = data.get("email")

    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()

    if not user:
        # Security: Don't reveal if user exists or not, but for this app we'll be helpful
        return (
            jsonify(
                {
                    "message": "If this email is registered, you will receive password reset instructions."
                }
            ),
            200,
        )

    # Mock Email Sending
    try:
        import smtplib
        from email.mime.text import MIMEText

        # Check for Environment Variables (for real sending)
        smtp_server = os.environ.get("MAIL_SERVER")
        smtp_port = os.environ.get("MAIL_PORT")
        smtp_user = os.environ.get("MAIL_USERNAME")
        smtp_password = os.environ.get("MAIL_PASSWORD")

        if smtp_server and smtp_user and smtp_password:
            msg = MIMEText(
                "This is a password reset request for your FitHub account.\n\n(This is a generic message as reset token flow is complex)."
            )
            msg["Subject"] = "FitHub Password Reset"
            msg["From"] = smtp_user
            msg["To"] = email

            with smtplib.SMTP(
                smtp_server, int(smtp_port) if smtp_port else 587
            ) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.send_message(msg)
            print(f"Email sent to {email}")
        else:
            print(
                f"SIMULATED EMAIL to {email}: 'Password Reset Request Received. Please contact admin to reset.'"
            )

    except Exception as e:
        print(f"Failed to send email: {e}")
        # Return success regardless to user

    return (
        jsonify(
            {
                "message": "If this email is registered, you will receive password reset instructions."
            }
        ),
        200,
    )


# 2. USER PROFILE & STATS
@app.route("/api/user/<user_id>/profile", methods=["GET", "POST"])
def profile(user_id):
    conn = get_db_connection()
    if request.method == "POST":
        data = request.json
        conn.execute(
            """
            UPDATE user_stats 
            SET height = ?, weight = ?, goal = ?, gender = ?, bmi = ?
            WHERE user_id = ?
        """,
            (
                data.get("height"),
                data.get("weight"),
                data.get("goal"),
                data.get("gender"),
                data.get("bmi"),
                user_id,
            ),
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "Profile updated"}), 200
    else:
        # GET
        stats = conn.execute(
            "SELECT * FROM user_stats WHERE user_id = ?", (user_id,)
        ).fetchone()
        conn.close()
        if stats:
            return jsonify(dict(stats)), 200
        else:
            return jsonify({}), 404


# 3. DIET & MEALS
@app.route("/api/meals", methods=["GET"])
def get_meals():
    diet_type = request.args.get("diet", "balanced")
    day_type = request.args.get("type", "weekdays")  # 'weekdays' or 'weekend'

    conn = get_db_connection()

    # 1. Fetch Meals
    meals_query = "SELECT * FROM meals WHERE diet_plan_id = ? AND day_type = ?"
    meals = conn.execute(meals_query, (diet_type, day_type)).fetchall()

    # 2. Fetch Ingredients for these meals
    meal_list = []
    for meal in meals:
        m = dict(meal)
        ingredients = conn.execute(
            "SELECT name, amount FROM meal_ingredients WHERE meal_id = ?", (m["id"],)
        ).fetchall()
        # Format ingredients as list of lists to match frontend expectation: [['Name', 'Amount'], ...]
        m["ingredients"] = [[i["name"], i["amount"]] for i in ingredients]
        meal_list.append(m)

    conn.close()

    return jsonify(meal_list), 200


@app.route("/api/user/<user_id>/meals", methods=["GET"])
def get_user_meals(user_id):
    conn = get_db_connection()
    meals = conn.execute("SELECT * FROM meals").fetchall()
    conn.close()
    return jsonify([dict(m) for m in meals])


# 4. DASHBOARD & LOGGING
@app.route("/api/user/<user_id>/dashboard", methods=["GET"])
def dashboard_stats(user_id):
    # Fetch real stats from daily_logs
    conn = get_db_connection()
    import datetime

    today = datetime.date.today().isoformat()

    # Get today's logs
    log = conn.execute(
        "SELECT water_intake, calories_consumed FROM daily_logs WHERE user_id = ? AND date = ?",
        (user_id, today),
    ).fetchone()

    # Calculate Streak
    streak = 0
    try:
        # Get all distinct dates for this user, ordered by date DESC
        dates = conn.execute(
            "SELECT DISTINCT date FROM daily_logs WHERE user_id = ? ORDER BY date DESC",
            (user_id,),
        ).fetchall()

        if dates:
            date_list = [d["date"] for d in dates]

            # Check if today is logged
            current_check = datetime.date.today()

            # If today is NOT in list, check if yesterday is (to keep streak alive)
            if today not in date_list:
                # If the most recent log is not today, check if it was yesterday
                # If latest log is older than yesterday, streak is 0 (unless we want to forgive 1 day, but strict streak is 0)
                latest_date = datetime.date.fromisoformat(date_list[0])
                if (current_check - latest_date).days > 1:
                    streak = 0
                else:
                    # It was yesterday, so potential streak is alive, but today doesn't count yet?
                    # Usually streak counts completed days or current active chain.
                    # Let's count backwards from latest_date
                    current_check = latest_date

            # Now count backwards
            for d_str in date_list:
                d_date = datetime.date.fromisoformat(d_str)
                if d_date == current_check:
                    streak += 1
                    current_check -= datetime.timedelta(days=1)
                elif d_date < current_check:
                    # Gap found
                    break
    except Exception as e:
        print(f"Streak logic error: {e}")
        streak = 0

    water = log["water_intake"] if log else 0
    calories = log["calories_consumed"] if log else 0

    conn.close()

    return jsonify({"streak": streak, "water": water, "calories": calories})


@app.route("/api/log/meal", methods=["POST"])
def log_meal():
    data = request.json
    user_id = data.get("user_id")
    meal_id = data.get("meal_id")
    calories = data.get("calories")

    import datetime

    today = datetime.date.today().isoformat()

    conn = get_db_connection()
    try:
        # Check if log exists for today
        log = conn.execute(
            "SELECT id, calories_consumed FROM daily_logs WHERE user_id = ? AND date = ?",
            (user_id, today),
        ).fetchone()

        if log:
            new_cal = log["calories_consumed"] + calories
            conn.execute(
                "UPDATE daily_logs SET calories_consumed = ? WHERE id = ?",
                (new_cal, log["id"]),
            )
        else:
            conn.execute(
                "INSERT INTO daily_logs (user_id, date, calories_consumed) VALUES (?, ?, ?)",
                (user_id, today, calories),
            )

        # [NEW] Insert into detailed food_logs for Phase 3 History
        # We need meal name. Data packet should have it.
        # If not, we fetch it or just use "Meal".
        meal_name = data.get("meal_name", "Quick Add")

        # Ensure table exists (redundant safety)
        conn.execute(
            """CREATE TABLE IF NOT EXISTS food_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            meal_name TEXT,
            calories INTEGER,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )"""
        )

        conn.execute(
            "INSERT INTO food_logs (user_id, meal_name, calories) VALUES (?, ?, ?)",
            (user_id, meal_name, calories),
        )

        conn.commit()
        return (
            jsonify(
                {
                    "message": "Meal logged successfully",
                    "new_total": (
                        (log["calories_consumed"] + calories) if log else calories
                    ),
                }
            ),
            200,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()


@app.route("/api/user/<user_id>/logs/today/detail", methods=["GET"])
def get_daily_log_details(user_id):
    import datetime

    today = datetime.date.today().isoformat()
    conn = get_db_connection()
    conn.execute(
        """CREATE TABLE IF NOT EXISTS food_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        meal_name TEXT,
        calories INTEGER,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )"""
    )

    logs = conn.execute(
        "SELECT * FROM food_logs WHERE user_id = ? AND date(timestamp) = date('now', 'localtime') ORDER BY timestamp DESC",
        (user_id,),
    ).fetchall()
    conn.close()

    return jsonify([dict(l) for l in logs])


# 5. GYM / WORKOUTS
@app.route("/api/workouts", methods=["GET"])
def get_workouts():
    conn = get_db_connection()
    workouts = conn.execute("SELECT * FROM workouts").fetchall()
    conn.close()

    # Init if empty
    if not workouts:
        seed_workouts()
        conn = get_db_connection()
        workouts = conn.execute("SELECT * FROM workouts").fetchall()
        conn.close()

    return jsonify([dict(w) for w in workouts])


@app.route("/api/log/workout", methods=["POST"])
def log_workout():
    data = request.json
    try:
        conn = get_db_connection()
        # Log workout
        log_id = str(uuid.uuid4())
        today = datetime.date.today().isoformat()

        conn.execute(
            "INSERT INTO user_workouts (id, user_id, workout_id, date, status) VALUES (?, ?, ?, ?, ?)",
            (log_id, data["user_id"], data["workout_id"], today, "completed"),
        )

        conn.commit()
        conn.close()
        return jsonify({"message": "Workout logged successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def seed_workouts():
    workouts = [
        (
            "Push Day",
            "Strength",
            60,
            400,
            "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=400",
        ),
        (
            "Pull Day",
            "Strength",
            60,
            400,
            "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=400",
        ),
        (
            "Leg Day",
            "Strength",
            60,
            500,
            "https://images.unsplash.com/photo-1434608519344-49d77a699ded?w=400",
        ),
        (
            "HIIT Cardio",
            "Cardio",
            30,
            350,
            "https://images.unsplash.com/photo-1601422407692-ec4eeec1d9b3?w=400",
        ),
        (
            "Yoga Flow",
            "Flexibility",
            45,
            150,
            "https://images.unsplash.com/photo-1544367563-12123d8965cd?w=400",
        ),
    ]
    conn = get_db_connection()
    for w in workouts:
        w_id = str(uuid.uuid4())
        conn.execute(
            "INSERT INTO workouts (id, name, type, duration_min, calories_burn, image_url) VALUES (?, ?, ?, ?, ?, ?)",
            (w_id, w[0], w[1], w[2], w[3], w[4]),
        )
    conn.commit()
    conn.close()
    print("Seeded Workouts.")


if __name__ == "__main__":
    app.run(debug=True)
