# Nora ai 

This project has been migrated to use Python (Flask) for backend logic and templating. The dashboard UI remains the same, but all data is now rendered from Python using Jinja2 templates.

## How to Run (Python/Flask)

1. Make sure you have Python 3.8+ installed.
2. Install Flask:
   ```sh
   pip install flask
   ```
3. Run the app:
   ```sh
   python app.py
   ```
4. Open your browser at http://127.0.0.1:5000/

---

# Nora ai - Engineering Companion Dashboard

Norait is a comprehensive web dashboard designed specifically for engineers to help them stay focused, monitor their productivity, and grow in their careers. It features real-time activity monitoring, AI-powered assistance, and a suite of productivity tools.

## Features

### 🎯 Core Features
- **Real-time Activity Monitoring**: Track your current applications and system performance
- **AI Chat Assistant (Nora)**: Get coding help, career advice, and productivity tips
- **Focus Timer**: Pomodoro-style timer to maintain focus sessions
- **Process Monitoring**: View top running processes with CPU and memory usage
- **Productivity Analytics**: Track your daily productivity metrics
- **Career Goal Tracking**: Set and monitor your professional development goals

### 🛠 Additional Features
- **Dark/Light Theme Toggle**: Comfortable viewing in any environment
- **Distraction Blocking**: Focus mode to minimize interruptions
- **System Health Monitoring**: CPU, memory, and disk usage indicators
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Offline Support**: Basic functionality available without internet connection
- **Keyboard Shortcuts**: Quick access to common actions

## Setup Instructions

### 1. Firebase Configuration

To enable real-time activity monitoring, you need to set up Firebase Firestore:

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project or select an existing one
3. Enable Firestore Database
4. Create a collection named \`activity\`
5. Get your Firebase configuration from Project Settings

Replace the placeholder configuration in \`script.js\`:

\`\`\`javascript
const firebaseConfig = {
    apiKey: "your-actual-api-key",
    authDomain: "your-project.firebaseapp.com",
    projectId: "your-actual-project-id",
    storageBucket: "your-project.appspot.com",
    messagingSenderId: "123456789012",
    appId: "your-actual-app-id"
};
\`\`\`

### 2. Firestore Data Structure

Your \`activity\` collection should contain documents with the following structure:

\`\`\`json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "currentApp": "Visual Studio Code",
  "cpuUsage": 45,
  "memoryUsage": 62,
  "activeTime": 1800,
  "projectName": "React Dashboard"
}
\`\`\`

### 3. Gemini API Integration

To enable the AI chat functionality:

1. Get a Gemini API key from [Google AI Studio](https://makersuite.google.com/)
2. Set up your backend endpoint to handle \`/askGemini\` requests
3. Update the endpoint URL in \`script.js\`:

\`\`\`javascript
const GEMINI_API_ENDPOINT = 'https://your-backend.com/askGemini';
\`\`\`

### 4. Backend API Endpoint

Create an endpoint that accepts POST requests with this structure:

\`\`\`javascript
// Request body
{
  "message": "How can I improve my coding skills?",
  "context": "engineering_companion"
}

// Expected response
{
  "response": "Here are some ways to improve your coding skills..."
}
\`\`\`

## File Structure

\`\`\`
norait-dashboard/
├── index.html          # Landing page
├── dashboard.html      # Main dashboard
├── style.css          # All styles and responsive design
├── script.js          # JavaScript functionality
├── README.md          # This file
└── assets/            # Images and icons (optional)
\`\`\`

## Installation

1. Clone or download the project files
2. Configure Firebase (see setup instructions above)
3. Set up your Gemini API endpoint
4. Open \`index.html\` in a web browser
5. Click "Enter Dashboard" to access the main interface

## Usage

### Getting Started
1. Start from the intro page (\`index.html\`)
2. Click "Enter Dashboard" to access the main interface
3. The dashboard will begin monitoring your activity automatically

### Key Features Usage

**Focus Timer**
- Click the play button to start a 25-minute focus session
- Use pause/reset controls as needed
- Receive notifications when sessions complete

**AI Chat (Nora)**
- Use the chat sidebar to ask questions
- Try the suggested prompts for quick help
- Ask about coding, career advice, or productivity tips

**Activity Monitoring**
- View your current application and project
- Monitor system performance metrics
- Track daily productivity statistics

**Process Management**
- View top 5 running processes
- Monitor CPU and memory usage
- Refresh data with the refresh button

### Keyboard Shortcuts
- \`Ctrl/Cmd + K\`: Focus chat input
- \`Ctrl/Cmd + T\`: Toggle theme
- \`Space\`: Toggle timer (when not in input fields)
- \`Escape\`: Close modals

## Customization

### Themes
The dashboard supports both light and dark themes. You can customize colors by modifying the CSS variables in \`style.css\`:

\`\`\`css
:root {
    --primary-color: #6366f1;
    --secondary-color: #10b981;
    --accent-color: #f59e0b;
    /* Add your custom colors */
}
\`\`\`

### Adding Features
The modular structure makes it easy to add new features:

1. Add HTML structure to \`dashboard.html\`
2. Add styles to \`style.css\`
3. Add functionality to \`script.js\`
4. Follow the existing patterns for consistency

## Browser Support

- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

## Troubleshooting

### Common Issues

**Firebase not connecting**
- Verify your Firebase configuration
- Check that Firestore is enabled
- Ensure the \`activity\` collection exists

**AI chat not working**
- Verify your Gemini API endpoint is accessible
- Check the API key configuration
- Ensure CORS is properly configured on your backend

**Timer not working**
- Check browser console for JavaScript errors
- Ensure all files are properly linked
- Try refreshing the page

**Responsive issues**
- Clear browser cache
- Check viewport meta tag is present
- Test in different screen sizes

## Contributing

Feel free to contribute to Norait by:
1. Reporting bugs
2. Suggesting new features
3. Submitting pull requests
4. Improving documentation

## License

This project is open source and available under the MIT License.

## Support

For support and questions:
- Check the troubleshooting section above
- Review the browser console for error messages
- Ensure all configuration steps are completed

---

**Happy coding with Norait! 🚀**
