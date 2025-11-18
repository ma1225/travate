# 🤖 AI Setup Guide for Travel Mate AI

This guide explains how to set up the AI features using OpenAI API.

## 📋 What is OpenAI API?

OpenAI API allows the application to generate **real, specific travel information** based on your destination and preferences. For example, if you select "Vienna" and "Popular Attractions", it will suggest actual places like "Schönbrunn Palace" and "St. Stephen's Cathedral" instead of generic suggestions.

## 🚀 Setup Instructions

### Step 1: Get an OpenAI API Key

1. Go to [OpenAI's website](https://platform.openai.com/)
2. Sign up for an account (or log in if you have one)
3. Navigate to [API Keys section](https://platform.openai.com/api-keys)
4. Click "Create new secret key"
5. Give it a name (e.g., "Travel Mate AI")
6. **Copy the key immediately** - you won't be able to see it again!

### Step 2: Set the API Key

#### Option A: Environment Variable (Recommended)

**Windows:**
1. Open Command Prompt
2. Set the environment variable:
   ```
   set OPENAI_API_KEY=your-api-key-here
   ```
3. Then run your Flask app in the same window

**Mac/Linux:**
1. Open Terminal
2. Set the environment variable:
   ```bash
   export OPENAI_API_KEY=your-api-key-here
   ```
3. Then run your Flask app in the same terminal

**Permanent Setup (Windows):**
1. Right-click "This PC" → Properties
2. Click "Advanced system settings"
3. Click "Environment Variables"
4. Under "User variables", click "New"
5. Variable name: `OPENAI_API_KEY`
6. Variable value: `your-api-key-here`
7. Click OK

**Permanent Setup (Mac/Linux):**
Add to your `~/.bashrc` or `~/.zshrc`:
```bash
export OPENAI_API_KEY=your-api-key-here
```
Then run: `source ~/.bashrc` (or `source ~/.zshrc`)

#### Option B: Create a .env File

1. Create a file named `.env` in the `backend` folder
2. Add this line:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```
3. The `python-dotenv` package (already in requirements.txt) will automatically load it

### Step 3: Install OpenAI Package

Make sure you've installed the OpenAI package:

```bash
cd backend
pip install -r requirements.txt
```

This will install `openai` along with other dependencies.

### Step 4: Test It!

1. Start your Flask server:
   ```bash
   python app.py
   ```

2. Go to the website and fill out the form:
   - Select a destination (e.g., "Austria: Vienna")
   - Choose dates
   - Select preferences (e.g., "Popular Attractions")
   - Submit

3. You should see **specific, real attractions** for Vienna!

## 💰 Cost Information

- OpenAI API charges based on usage
- The app uses `gpt-4o-mini` model, which is very affordable
- Typical cost: **$0.15 - $0.60 per 1 million input tokens**
- A typical travel itinerary request costs **less than $0.01**
- You get **$5 free credit** when you sign up

## 🔧 Troubleshooting

### Problem: "Warning: OPENAI_API_KEY not set"
**Solution**: Make sure you've set the environment variable or created the `.env` file correctly.

### Problem: "Error calling OpenAI"
**Solution**: 
- Check that your API key is correct
- Make sure you have credits in your OpenAI account
- Check your internet connection

### Problem: Still seeing generic activities
**Solution**: 
- Check the terminal/console for error messages
- Verify the API key is set correctly
- Make sure `openai` package is installed: `pip install openai`

### Problem: API key not working
**Solution**:
- Make sure there are no extra spaces in the API key
- Try creating a new API key
- Check that your OpenAI account has credits

## 🎯 How It Works

1. **User submits form** with destination and preferences
2. **Backend creates a prompt** asking AI for specific attractions/activities
3. **AI generates response** with real place names and activities
4. **Backend parses the response** and creates the schedule table
5. **Results page displays** the AI-generated itinerary

## 🔄 Fallback Mode

If OpenAI API is not available or fails, the app will automatically use a **fallback mode** that generates city-specific but generic activities. This ensures the app always works, even without AI.

## 📝 Example

**Without AI (Fallback):**
- "Visit famous landmarks in Vienna"
- "Explore Vienna's historic center"

**With AI:**
- "Visit Schönbrunn Palace"
- "Explore Vienna's Historic Center (Innere Stadt)"
- "Dinner at Figlmüller (famous for Wiener Schnitzel)"
- "Tour of St. Stephen's Cathedral"

## 🎉 You're All Set!

Once configured, the AI will automatically generate detailed, destination-specific travel plans for every trip you plan!

---

**Need Help?** Check the main README.md or the error messages in your terminal for more information.

