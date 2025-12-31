# FitHub - Complete Fitness Management Platform

## About The Project

FitHub is a comprehensive fitness management platform designed to help users track their workouts, manage nutrition, monitor progress, and achieve their fitness goals. The application provides an intuitive interface with powerful features that make fitness tracking effortless and effective.

Whether you're a beginner starting your fitness journey or an experienced athlete optimizing your training, FitHub provides all the essential tools in one centralized platform.

---

## Key Features

### Dashboard & Home
- Personalized greetings based on time of day
- Quick action buttons for starting workouts and viewing meal plans
- Daily tracking widgets for water intake and calorie consumption
- Consistency tracking with daily streak counter

### Workout Management
- Multiple workout categories including Dumbbells, Barbell, Bodyweight, Cardio, Yoga, and HIIT
- Detailed exercise instructions with step-by-step guidance
- Set, rep, and rest period tracking
- Built-in workout timer with pause and resume functionality
- Comprehensive workout completion summary showing time, reps, calories, and personal bests

### Nutrition & Diet Planning
- Weekly meal plans with separate schedules for weekdays and weekends
- Detailed calorie tracking for each meal
- Multiple meal time slots (breakfast, lunch, dinner)
- Various nutrition style options:
  - Balanced (Mix of everything)
  - Keto/Low Carb (High fat, low carb)
  - Mediterranean (Heart-healthy, plant-focused)
  - Pescatarian (Plant-based with seafood)
  - Vegetarian (Plant-based)
  - Vegan (Strictly plant-based)
- Visual meal representation with food images

### Hydration Tracking
- Daily water intake goal setting (default: 3000ml)
- Quick add buttons for common water amounts (250ml, 500ml)
- Detailed log of all water intake entries with timestamps
- Visual progress indicator with animated water bottle
- Daily reset functionality

### Health Monitoring
- BMI calculator with height and weight inputs
- Health status classification (Obese, Overweight, Normal, Underweight)
- Healthy weight range display based on height
- Unit conversion between metric and imperial systems
- Color-coded health status visualization

### Built-in Tools
- Stopwatch for tracking workout duration
- Real-time date and time display
- Session timer for rest periods between sets

### User Profile & Settings
- User account management with profile information
- Dark mode toggle for comfortable viewing
- Notification preferences for workout reminders
- Unit system selection (Metric/Imperial)
- Secure authentication system with account creation and login

---

## User Interface

### Design Principles
- Clean and modern minimalist design focused on usability
- Fully responsive layout that works seamlessly across all devices
- Intuitive bottom navigation bar for easy access (Home, Workouts, Diet, Profile)
- Real-time visual feedback and progress indicators
- Consistent color scheme with green accent (#2D7552) throughout the application

### Application Screens
1. Sign Up / Login - Secure account creation with terms and conditions
2. Dashboard - Personalized home screen with quick action cards
3. Workout Categories - Grid layout of exercise equipment and workout styles
4. Exercise Details - Comprehensive instructions with sets, reps, and rest information
5. Workout Timer - Real-time countdown with set completion tracking
6. Completion Summary - Detailed workout statistics and achievements
7. Hydration Monitor - Visual water intake tracker with progress indicator
8. BMI Calculator - Health metric computation with visual feedback
9. Meal Planner - Weekly nutrition schedule with calorie information
10. Nutrition Style Selector - Dietary preference selection interface
11. Stopwatch - Time tracking utility tool
12. Settings - User preferences and account management

---

## Getting Started

### Prerequisites
- Flask
- Git version control
- SQL-Lite database

### Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/fithub.git
cd fithub
```

2. Install dependencies
```bash
npm install
# or
yarn install
```

3. Set up environment variables
```bash
cp .env.example .env
# Edit .env file with your database credentials and configuration
```

4. Run the development server
```bash
npm run dev
# or
yarn dev
```

5. Open your browser and navigate to
```
http://localhost:5000
```

---

## Tech Stack

### Frontend
- React.js - Component-based UI library
- Tailwind CSS - Utility-first CSS framework
- React Router - Client-side routing

### Backend
- Flask
- SQL-Lite

### Authentication & Security
- Secure authentication

### Additional Tools
- Vs Code
- DB(browser) SQL-lite

---

## Usage Examples

### User Registration
```javascript
POST /api/auth/register
{
  "name": "Usama",
  "email": "usama@gmail.com",
  "password": "securepassword123"
}
```

### Starting a Workout Session
```javascript
GET /api/workouts/barbell-blast
// Returns: Sets, Reps, Rest periods, Exercise instructions
```

### Adding Water Intake
```javascript
POST /api/hydration/add
{
  "amount": 500,
  "timestamp": "2025-12-31T23:12:00"
}
```

### Calculating BMI
```javascript
POST /api/health/bmi
{
  "height": 175,
  "weight": 70,
  "unit": "metric"
}
```

---

## Roadmap

### Completed Features
- [x] User authentication and authorization system
- [x] Workout tracking with multiple categories
- [x] Meal planning and nutrition tracking
- [x] BMI calculator and health metrics
- [x] Hydration monitoring system
- [x] Dark mode support

### Planned Features
- [ ] Social features (friend connections, fitness challenges)
- [ ] Progress photos and body measurement tracking
- [ ] Expanded workout video library
- [ ] AI-powered personalized workout recommendations
- [ ] Integration with fitness wearables and smartwatches
- [ ] Native mobile applications (iOS & Android)
- [ ] Advanced analytics and progress reports
- [ ] Custom workout plan creation
- [ ] Trainer-client connection system

---

## Contributing

Contributions are welcome and greatly appreciated. To contribute to this project:

1. Fork the repository
2. Create your feature branch
```bash
git checkout -b feature/AmazingFeature
```
3. Commit your changes
```bash
git commit -m 'Add some AmazingFeature'
```
4. Push to the branch
```bash
git push origin feature/AmazingFeature
```
5. Open a Pull Request

Please ensure your code follows the existing code style and includes appropriate tests.

---

## Author

**Your Name**
- GitHub: https://github.com/m-asad01
- Email: bsef24a034@pucit.edu.pk
- LinkedIn: https://www.linkedin.com/in/muhammad-asad-7761b8335?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app
---

## Acknowledgments

- Fitness icons and assets from open-source libraries
- Community feedback and contributions
- Open-source frameworks and tools that made this project possible

---

## Support

For questions, issues, or feature requests:
- Open an issue on GitHub
- Email: bsef24a034@pucit.edu.pk

---
