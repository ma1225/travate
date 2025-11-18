# 🌍 Travel Mate AI

A modern web application that helps you plan your perfect trip using AI-powered scheduling and connects you with fellow travelers!

## 📋 What is Travel Mate AI?

Travel Mate AI is a user-friendly website that:
- **Creates personalized travel schedules** using AI based on your destination, dates and preferences
- **Suggests real, specific activities** for your chosen destination (e.g., "Visit Schönbrunn Palace" in Vienna)
- **Select from 50+ destinations** worldwide (Country: City format)
- **AI-powered itinerary generation** that provides actual attractions, restaurants, and activities
- **Connects solo travelers** with potential travel companions
- **Provides a beautiful, modern interface** that's easy to use

## 🚀 Getting Started (For Beginners)

### Step 1: Install Python

1. Download Python from [python.org](https://www.python.org/downloads/)
2. During installation, check the box that says "Add Python to PATH"
3. Verify installation by opening Command Prompt (Windows) or Terminal (Mac/Linux) and typing:
   ```
   python --version
   ```
   You should see something like "Python 3.x.x"

### Step 2: Navigate to Project Folder

1. Open Command Prompt (Windows) or Terminal (Mac/Linux)
2. Navigate to your project folder. For example:
   ```
   cd C:\Users\ma122\PycharmProjects\TravelMateAI
   ```

### Step 3: Install Required Packages

1. Navigate to the backend folder:
   ```
   cd backend
   ```

2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

   This will install:
   - Flask (web framework)
   - flask-cors (for handling web requests)
   - python-dotenv (for environment variables)
   - openai (for AI-powered travel planning)

### Step 3.5: Set Up AI (Optional but Recommended)

For **real, destination-specific travel information**, set up OpenAI API:
1. See `AI_SETUP.md` for detailed instructions
2. Get a free API key from [OpenAI](https://platform.openai.com/)
3. Set it as an environment variable: `OPENAI_API_KEY=your-key-here`
4. The app works without it, but will show generic activities instead of real places

### Step 4: Run the Application

1. Make sure you're in the `backend` folder
2. Run the application:
   ```
   python app.py
   ```

3. You should see a message like:
   ```
   * Running on http://127.0.0.1:5000
   ```

### Step 5: Open in Browser

1. Open your web browser (Chrome, Firefox, Safari, etc.)
2. Go to: `http://localhost:5000` or `http://127.0.0.1:5000`
3. You should see the Travel Mate AI homepage!

## 📁 Project Structure

```
TravelMateAI/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── requirements.txt     # Python dependencies
│   └── __init__.py
├── templates/
│   ├── index.html          # Home page with travel form
│   ├── results.html        # Results page with schedule
│   └── about.html          # About page
├── static/
│   └── style.css           # Custom styling
└── README.md               # This file
```

## 🎯 How to Use

### 1. Plan Your Trip
- Go to the home page
- **Select your destination** from the dropdown (Country: City format, e.g., "Austria: Vienna")
- Enter your **start date** and **end date**
- Select your **vacation preferences**:
  - Popular Attractions
  - Bars & Nightlife
  - Restaurants
  - Beaches
  - Shopping
  - Nature & Hiking

### 2. Traveling Alone?
- Select "Yes" if you want to see potential travel companions
- Select "No" if you're traveling with others

### 3. Submit and View Results
- Click "Submit for the best traveling experience you will encounter"
- **AI generates a personalized schedule** with real attractions and activities for your destination
- View your detailed schedule table with specific place names
- See matching travelers (if you selected "traveling alone")

## 🛠️ Technical Details

### Technologies Used
- **Backend**: Python with Flask framework
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Icons**: Font Awesome
- **Styling**: Custom CSS with modern design

### Key Features
- **Destination Selection**: Choose from 50+ cities worldwide
- **AI-Powered Planning**: Uses OpenAI to generate real, specific travel recommendations
- **Form Handling**: Collects user input (destination, dates, and preferences)
- **Schedule Generation**: Creates day-by-day itinerary with actual attractions and activities
- **User Matching**: Generates random travel companions for solo travelers
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Fallback Mode**: Works even without AI (shows city-specific generic activities)

## 🔧 Troubleshooting

### Problem: "Module not found" error
**Solution**: Make sure you installed all requirements:
```
pip install -r backend/requirements.txt
```

### Problem: Port already in use
**Solution**: The default port is 5000. If it's busy, you can change it in `backend/app.py`:
```python
app.run(host="0.0.0.0", port=5001, debug=True)  # Change 5001 to any available port
```

### Problem: Page not loading
**Solution**: 
1. Make sure the Flask server is running
2. Check that you're using the correct URL: `http://localhost:5000`
3. Check the terminal/command prompt for error messages

## 📝 Code Explanation

### Backend (app.py)
- **`/` route**: Shows the home page
- **`/submit` route**: Handles form submission and generates the travel schedule
- **`/about` route**: Shows the about page
- **`generate_travel_schedule()`**: Creates activities for each day based on preferences
- **`generate_random_users()`**: Creates fake travel companions with random data

### Frontend (HTML Templates)
- **index.html**: Home page with the travel form
- **results.html**: Displays the schedule table and matching users
- **about.html**: Information about the application

### Styling (style.css)
- Modern design with animations
- Responsive layout for all devices
- Beautiful color scheme and typography

## 🎨 Customization Ideas

You can customize the application by:
1. **Adding more preferences**: Edit the checkboxes in `templates/index.html`
2. **Changing activities**: Modify `activity_templates` in `backend/app.py`
3. **Updating colors**: Edit `static/style.css`
4. **Adding more user fields**: Modify `generate_random_users()` in `backend/app.py`

## 📚 Learning Resources

If you want to learn more:
- **Flask**: [Flask Documentation](https://flask.palletsprojects.com/)
- **HTML/CSS**: [MDN Web Docs](https://developer.mozilla.org/)
- **Bootstrap**: [Bootstrap Documentation](https://getbootstrap.com/)

## 🤝 Contributing

Feel free to improve this project! Some ideas:
- Add more activity types
- Integrate with real travel APIs
- Add user authentication
- Create a database to store travel plans

## 📄 License

This project is open source and available for educational purposes.

## 💡 Tips for Beginners

1. **Read the code comments**: They explain what each part does
2. **Experiment**: Try changing colors, text, or adding new features
3. **Use browser developer tools**: Press F12 to inspect elements
4. **Test thoroughly**: Try different date ranges and preference combinations

## 🎉 Enjoy Your Travel Planning!

Happy travels! 🌍✈️

---

**Need Help?** Check the code comments or experiment with the application to understand how it works!

