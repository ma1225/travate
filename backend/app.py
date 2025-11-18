import os
import random
import json
import uuid
from datetime import datetime, timedelta
from urllib.parse import quote_plus
from flask import Flask, request, render_template, redirect, url_for
from flask_cors import CORS

# Try to import OpenAI, but make it optional
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("Warning: OpenAI not installed. Install with: pip install openai")

app = Flask(__name__, template_folder='../templates', static_folder='../static')
CORS(app, origins=os.getenv("CORS_ORIGINS", "*"))

# Constants
DEFAULT_INTERVAL_HOURS = 3
DEFAULT_START_TIME = "08:00"
DEFAULT_END_TIME = "22:00"
BREAKFAST_WINDOW = (7, 10)
LUNCH_WINDOW = (12, 14)
DINNER_WINDOW = (18, 21)
MAX_INTERVAL = 4
MIN_INTERVAL = 1

# Initialize OpenAI client if API key is available
openai_client = None
if OPENAI_AVAILABLE:
    api_key = os.getenv("OPENAI_API_KEY")
    api_key = "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"
    if api_key:
        openai_client = OpenAI(api_key=api_key)
    else:
        print("Warning: OPENAI_API_KEY not set. AI features will use fallback mode.")

def generate_random_users(n=9):
    """Generate random users who are willing to join solo travelers"""
    male_names = ["Jake", "David", "Ron", "John", "Mark", "Liam", "Steven", "Noah", 
                  "Josh", "Ethan", "Jose", "Nick", "James", "Chris", "Lucas", "Francis"]
    female_names = ["Emily", "Sarah", "Rachel", "Sharon", "Sophia", "Katy", "Emma", "Christina", 
                    "Olivia", "Alia", "Maya", "Aria", "Jessie", "Isabella", "Gina", "Charlotte"]
    countries = ["USA", "Canada", "Germany", "Brazil", "Japan", "Israel", "France", 
                 "India", "UK", "Australia", "Spain", "Italy", "Netherlands", "Sweden", "Norway"]
    interests = ["Adventure", "Foodie", "Nightlife", "Culture", "Relaxation", 
                 "Photography", "Hiking", "Music", "Art", "Beach", "History"]
    genders = ["Male", "Female"]
    bios = [
        "Always down for a last-minute city tour and exploring hidden gems!",
        "Looking for coffee shops and local experiences.",
        "Nightlife enthusiast—love bars, live music, and meeting new people.",
        "Museum hopper and local cuisine explorer. Food is my passion!",
        "Beach days and sunrise hikes. Nature lover at heart.",
        "Street food and photo walks. Capturing moments everywhere I go.",
        "Solo traveler looking for adventure buddies. Let's explore together!",
        "Love trying new restaurants and discovering local culture."
    ]
    users = []
    for _ in range(n):
        gender = random.choice(genders)
        users.append({
            "gender": gender,
            "name": random.choice(male_names) if gender.lower() == "male" else random.choice(female_names),
            "country": random.choice(countries),
            "age": random.randint(22, 45),
            "interest": random.choice(interests),
            "bio": random.choice(bios),
            "avatar": f"https://i.pravatar.cc/150?img={random.randint(1, 60)}"
        })
    return users


def clamp_interval(interval):
    try:
        interval = int(interval)
    except (TypeError, ValueError):
        return DEFAULT_INTERVAL_HOURS
    return max(MIN_INTERVAL, min(MAX_INTERVAL, interval))


def generate_time_slots(start_time_str, end_time_str, interval_hours):
    """Generate time slots between start and end time using the provided interval."""
    try:
        interval_hours = clamp_interval(interval_hours)
        start_dt = datetime.strptime(start_time_str, "%H:%M")
        end_dt = datetime.strptime(end_time_str, "%H:%M")
    except ValueError:
        start_dt = datetime.strptime(DEFAULT_START_TIME, "%H:%M")
        end_dt = datetime.strptime(DEFAULT_END_TIME, "%H:%M")
        interval_hours = DEFAULT_INTERVAL_HOURS

    if end_dt <= start_dt:
        end_dt = start_dt + timedelta(hours=12)

    slots = []
    current = start_dt
    while current <= end_dt:
        slots.append(current.strftime("%H:%M"))
        current += timedelta(hours=interval_hours)
    return slots


def _create_activity_details(activity_name, city, category="General"):
    rating = round(random.uniform(4.2, 4.9), 1)
    review_count = random.randint(120, 3200)
    description = f"Experience {activity_name} in {city}. A highly rated {category.lower()} highlight recommended for curious travelers."
    search_query = quote_plus(f"{activity_name} {city}")
    link = f"https://www.google.com/maps/search/?api=1&query={search_query}"
    return {
        "title": activity_name,
        "description": description,
        "link": link,
        "rating": rating,
        "reviews": review_count,
        "rating_source": "Google Maps"
    }


def _meal_activity(meal_type, city):
    templates = {
        "breakfast": {
            "title": f"Gourmet breakfast in {city}",
            "description": f"Start the morning with freshly baked pastries and local coffee culture in {city}.",
            "category": "Breakfast",
        },
        "lunch": {
            "title": f"Local lunch experience in {city}",
            "description": f"Taste the authentic midday flavors of {city}, from street food to cozy bistros.",
            "category": "Lunch",
        },
        "dinner": {
            "title": f"Signature dinner in {city}",
            "description": f"End your day with a memorable dining experience featuring {city}'s culinary classics.",
            "category": "Dinner",
        }
    }
    template = templates[meal_type]
    details = _create_activity_details(template["title"], city, template["category"])
    details["description"] = template["description"]
    details["category"] = template["category"]
    return details

def _attach_timeline(day_schedule, city, time_slots, preferences):
    """Attach timeline to a day's activities using user-defined schedule."""
    activities = day_schedule.get("activities", [])
    if not activities:
        activities = [f"Explore {city}", f"Local experience in {city}"]

    meal_added = {"breakfast": False, "lunch": False, "dinner": False}
    timeline = []
    activity_index = 0

    for idx, time_label in enumerate(time_slots):
        hour = int(time_label.split(":")[0])
        slot_details = None
        if BREAKFAST_WINDOW[0] <= hour < BREAKFAST_WINDOW[1] and not meal_added["breakfast"]:
            slot_details = _meal_activity("breakfast", city)
            meal_added["breakfast"] = True
        elif LUNCH_WINDOW[0] <= hour < LUNCH_WINDOW[1] and not meal_added["lunch"]:
            slot_details = _meal_activity("lunch", city)
            meal_added["lunch"] = True
        elif DINNER_WINDOW[0] <= hour < DINNER_WINDOW[1] and not meal_added["dinner"]:
            slot_details = _meal_activity("dinner", city)
            meal_added["dinner"] = True
        else:
            activity_name = activities[activity_index % len(activities)]
            slot_details = _create_activity_details(activity_name, city)
            category = preferences[activity_index % len(preferences)] if preferences else "General"
            slot_details["category"] = category
            activity_index += 1

        timeline.append({
            "id": f"{day_schedule.get('day', idx)}-{uuid.uuid4().hex[:8]}",
            "time": time_label,
            "title": slot_details["title"],
            "description": slot_details["description"],
            "link": slot_details["link"],
            "rating": slot_details["rating"],
            "reviews": slot_details["reviews"],
            "rating_source": slot_details["rating_source"],
            "category": slot_details.get("category", "Experience")
        })

    day_schedule["timeline"] = timeline
    return day_schedule


def generate_travel_schedule_with_ai(destination, start_date, end_date, preferences,
                                     interval_hours=DEFAULT_INTERVAL_HOURS,
                                     start_time=DEFAULT_START_TIME,
                                     end_time=DEFAULT_END_TIME):
    """Generate a travel schedule using AI based on destination, dates and preferences"""
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        num_days = (end - start).days + 1
    except:
        return []
    
    # Parse destination
    if ':' in destination:
        country, city = destination.split(':', 1)
        city = city.strip()
        country = country.strip()
    else:
        city = destination
        country = ""
    
    # If OpenAI is available and configured, use it
    time_slots = generate_time_slots(start_time, end_time, interval_hours)

    if openai_client:
        try:
            # Create a detailed prompt for the AI
            preferences_text = ", ".join(preferences) if preferences else "general travel experiences"
            
            prompt = f"""Create a detailed {num_days}-day travel itinerary for {city}, {country}.

Travel Preferences: {preferences_text}

For each day, provide specific, real attractions, restaurants, bars, or activities that match the preferences. 
Be specific with actual place names and locations in {city}.

Return the response as a JSON array where each day is an object with:
- "day": day number (1, 2, 3, etc.)
- "date": date in YYYY-MM-DD format (starting from {start_date})
- "activities": array of specific activity names (e.g., "Visit Schönbrunn Palace" not "Visit palace")

Example format:
[
  {{
    "day": 1,
    "date": "{start_date}",
    "activities": ["Visit Schönbrunn Palace", "Explore Vienna's Historic Center", "Dinner at Figlmüller"]
  }},
  {{
    "day": 2,
    "date": "{start_date}",
    "activities": ["Tour of St. Stephen's Cathedral", "Visit Hofburg Palace", "Coffee at Café Central"]
  }}
]

Make sure activities are specific to {city} and match the preferences: {preferences_text}.
Include {len(preferences)} activities per day on average, distributed across the selected preferences."""

            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",  # Using the more affordable model
                messages=[
                    {"role": "system", "content": "You are a professional travel planner. Always return valid JSON arrays."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            # Parse the AI response
            ai_response = response.choices[0].message.content.strip()
            
            # Try to extract JSON from the response (sometimes AI wraps it in markdown)
            if "```json" in ai_response:
                ai_response = ai_response.split("```json")[1].split("```")[0].strip()
            elif "```" in ai_response:
                ai_response = ai_response.split("```")[1].split("```")[0].strip()
            
            schedule = json.loads(ai_response)
            
            # Format dates properly and attach timeline
            current_date = start
            for day_schedule in schedule:
                day_schedule["date"] = current_date.strftime('%Y-%m-%d')
                day_schedule["date_formatted"] = current_date.strftime('%B %d, %Y')
                _attach_timeline(day_schedule, city, time_slots, preferences)
                current_date += timedelta(days=1)
            
            return schedule
            
        except Exception as e:
            print(f"Error calling OpenAI: {e}")
            # Fall through to fallback method
            pass
    
    # Fallback: Generate schedule without AI (if OpenAI not available or fails)
    return generate_travel_schedule_fallback(city, country, start_date, end_date, preferences, time_slots)


def generate_travel_schedule_fallback(city, country, start_date, end_date, preferences, time_slots):
    """Fallback method to generate schedule without AI"""
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
    except:
        return []
    
    schedule = []
    current_date = start
    day_num = 1
    
    # City-specific activity templates
    activity_templates = {
        "Popular Attractions": [
            f"Visit famous landmarks in {city}",
            f"Explore {city}'s historic center",
            f"Take a guided tour of {city}",
            f"Visit museums and cultural sites in {city}",
            f"See the main tourist attractions in {city}",
            f"Explore {city}'s architecture"
        ],
        "Bars": [
            f"Evening drinks at rooftop bar in {city}",
            f"Local pub crawl in {city}",
            f"Cocktail tasting at trendy bars in {city}",
            f"Live music venue in {city}",
            f"Wine bar exploration in {city}",
            f"Nightlife district tour in {city}"
        ],
        "Restaurants": [
            f"Traditional local cuisine dinner in {city}",
            f"Street food market tour in {city}",
            f"Fine dining experience in {city}",
            f"Breakfast at famous local spot in {city}",
            f"Food tour of local specialties in {city}",
            f"Cooking class experience in {city}"
        ],
        "Beaches": [
            f"Beach day and relaxation in {city}",
            f"Water sports activities in {city}",
            f"Sunset beach walk in {city}",
            f"Beachside dining in {city}"
        ],
        "Shopping": [
            f"Local market shopping in {city}",
            f"Boutique store exploration in {city}",
            f"Souvenir hunting in {city}",
            f"Shopping district tour in {city}"
        ],
        "Nature": [
            f"Hiking trail adventure near {city}",
            f"Nature park visit near {city}",
            f"Scenic viewpoint exploration in {city}",
            f"Outdoor activities in {city}"
        ]
    }
    
    while current_date <= end:
        day_schedule = {
            "day": day_num,
            "date": current_date.strftime('%Y-%m-%d'),
            "date_formatted": current_date.strftime('%B %d, %Y'),
            "activities": []
        }
        
        # Add activities based on preferences
        for pref in preferences:
            if pref in activity_templates:
                activities = activity_templates[pref]
                num_activities = random.randint(1, 2) if day_num <= 3 else 1
                for _ in range(min(num_activities, len(activities))):
                    activity = random.choice(activities)
                    if activity not in day_schedule["activities"]:
                        day_schedule["activities"].append(activity)
        
        # If no preferences, add default activities
        if not day_schedule["activities"]:
            day_schedule["activities"] = [f"Explore {city}", f"Local experience in {city}"]
        
        _attach_timeline(day_schedule, city, time_slots, preferences)
        schedule.append(day_schedule)
        current_date += timedelta(days=1)
        day_num += 1
    
    return schedule

@app.route("/")
def index():
    """Home page with travel form"""
    return render_template('index.html')

@app.route("/submit", methods=["POST"])
def submit():
    """Handle form submission and generate travel plan"""
    destination = request.form.get('destination', '')
    start_date = request.form.get('start_travel_date')
    end_date = request.form.get('end_travel_date')
    preferences = request.form.getlist('preferences')
    travel_alone = request.form.get('travel_alone', 'no')
    interval_choice = clamp_interval(request.form.get('activity_interval', DEFAULT_INTERVAL_HOURS))
    activity_start_time = request.form.get('activity_start_time', DEFAULT_START_TIME)
    activity_end_time = request.form.get('activity_end_time', DEFAULT_END_TIME)
    
    # Generate travel schedule using AI
    schedule = generate_travel_schedule_with_ai(
        destination,
        start_date,
        end_date,
        preferences,
        interval_choice,
        activity_start_time,
        activity_end_time
    )
    
    # Generate matching users (only if traveling alone)
    matching_users = generate_random_users(9) if travel_alone == 'yes' else []
    
    # Parse destination for display
    if ':' in destination:
        country, city = destination.split(':', 1)
        city = city.strip()
        country = country.strip()
    else:
        city = destination
        country = ""
    
    return render_template('results.html', 
                         destination=destination,
                         city=city,
                         country=country,
                         start_date=start_date,
                         end_date=end_date,
                         preferences=preferences,
                         schedule=schedule,
                         activity_interval=interval_choice,
                         activity_start_time=activity_start_time,
                         activity_end_time=activity_end_time,
                         matching_users=matching_users,
                         travel_alone=travel_alone)

@app.route("/about")
def about():
    """About page"""
    return render_template('about.html')

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
