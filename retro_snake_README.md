# 🐍 Retro AI Snake - Win95 Edition

**"Classic Snake meets Modern AI Intelligence"**

A nostalgic recreation of the classic Snake game with authentic Windows 95 aesthetics, enhanced by an AI Game Master that learns your playing patterns and adapts the experience in real-time.

## 🎮 The Modern AI Twist

### Intelligent Game Master
- **Skill Assessment**: AI analyzes your performance and categorizes you (Beginner → Expert)
- **Dynamic Difficulty**: Game speed adapts based on your skill level and current performance
- **Smart Power-ups**: AI strategically spawns power-ups when you're struggling
- **Movement Prediction**: Shows AI predictions of your next move based on learned patterns
- **Persistent Learning**: Saves your playing data to improve over multiple sessions

### AI Features in Action
- **Adaptive Speed**: Beginners get slower gameplay, experts face lightning-fast challenges
- **Strategic Assistance**: More power-ups appear when you're underperforming
- **Pattern Recognition**: AI learns your preferred movement patterns
- **Performance Analytics**: Tracks death causes, reaction times, and improvement over time

## 🎨 Retro Aesthetics

### Authentic Win95 Design
- Classic Windows 95 color palette (that nostalgic gray!)
- 3D beveled buttons with proper highlight/shadow effects
- Inset game area with authentic border styling
- Pixel-perfect retro fonts and UI elements
- Classic green snake with white pixel highlights

### Visual Elements
- **Snake**: Classic green with bright head and retro pixel effects
- **Food**: Traditional red squares
- **Power-ups**: Blinking yellow items with timer effects
- **UI**: Authentic Windows 95 button styling and layout

## 🧠 Complex Logic Implementation

### AI Learning System
```python
# Skill level determination
def analyze_skill_level(self):
    if avg_score > 200 and avg_time > 120: return 'expert'
    elif avg_score > 100 and avg_time > 60: return 'advanced'
    # ... adaptive classification
```

### Dynamic Difficulty Engine
- Real-time speed adjustment based on performance
- Power-up frequency modulation
- Predictive movement analysis
- Statistical pattern recognition

### Data Persistence
- JSON-based player profile storage
- Cross-session learning continuity
- Performance trend analysis
- Movement pattern history

## 🎯 Game Features

### Core Gameplay
- **Classic Snake Mechanics**: Grow by eating food, avoid walls and self-collision
- **Power-ups**: Score multipliers, speed boosts, and invincibility
- **Progressive Difficulty**: AI adjusts challenge level dynamically
- **Smart Hints**: Optional AI movement predictions

### Controls
- **Arrow Keys**: Move snake (classic 4-directional movement)
- **SPACE**: Pause/Resume game (or restart when game over)
- **H**: Toggle AI prediction hints on/off
- **ESC**: Quit game

### AI Statistics Tracked
- Games played and average scores
- Average game duration
- Death cause analysis (wall vs self-collision)
- Preferred movement directions
- Reaction time measurements
- Movement pattern sequences

## 🚀 Quick Start

### Installation
```bash
# Install dependencies
pip install -r retro_requirements.txt

# Run the game
python retro_ai_snake.py
```

### First Launch
The AI starts with default beginner settings and begins learning immediately:
1. Play a few games to let the AI assess your skill
2. Watch as game speed and power-up frequency adapt
3. Toggle AI hints with 'H' to see movement predictions
4. Your progress is automatically saved between sessions

## 📊 AI Learning Examples

### Beginner Player Detection
- Slower base speed (8 FPS)
- Higher power-up frequency (40%)
- More forgiving difficulty scaling

### Expert Player Adaptation
- Faster base speed (20 FPS)
- Reduced power-up frequency (20%)
- Aggressive difficulty ramping

### Pattern Recognition
```
Player tends to move: UP → RIGHT → DOWN → LEFT (clockwise)
AI Prediction: "Next move likely RIGHT"
Confidence: 78%
```

## 🎨 Technical Implementation

### Retro UI System
- Custom Win95-style button renderer
- Authentic 3D border effects using highlight/shadow lines
- Classic inset/outset visual depth
- Period-accurate color palette

### AI Architecture
- **Data Collection**: Continuous gameplay metrics gathering
- **Pattern Analysis**: Movement sequence recognition
- **Adaptive Response**: Real-time difficulty adjustment
- **Predictive Modeling**: Next-move probability calculation

### Performance Optimization
- Efficient collision detection
- Minimal memory footprint
- 60 FPS capability with dynamic speed control
- Lightweight JSON data persistence

## 🎮 Gameplay Tips

1. **Let the AI Learn**: Play several games to see full adaptation
2. **Watch the Predictions**: Use AI hints to improve your strategy
3. **Challenge Yourself**: AI will increase difficulty as you improve
4. **Study Your Stats**: Check the skill assessment in the UI

## 🔧 Customization

Want to modify the AI behavior? Key parameters in `AIGameMaster`:

```python
# Adjust skill thresholds
base_speeds = {
    'beginner': 8,      # Slower for beginners
    'expert': 20        # Lightning fast for experts
}

# Modify power-up frequency
self.power_up_frequency = 0.3  # 30% chance per food eaten
```

## 🏆 Achievement System (Future Enhancement)

The AI framework supports adding:
- Skill milestone achievements
- Pattern mastery rewards
- Consistency bonuses
- Speed demon challenges

## 📈 Data Analytics

The game saves detailed analytics in `snake_ai_data.json`:
- Performance trends over time
- Skill progression tracking
- Behavioral pattern analysis
- Personalized difficulty curves

---

**Experience the perfect blend of retro gaming nostalgia and cutting-edge AI adaptation!**

*The more you play, the smarter it gets. The smarter it gets, the better you become.*