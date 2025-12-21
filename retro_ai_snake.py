#!/usr/bin/env python3
"""
Retro AI Snake - "Classic Snake meets Modern AI"

A nostalgic Snake game with Win95 aesthetics and AI-powered adaptive difficulty.
The AI learns your playing patterns and adjusts the game dynamically.
"""

import pygame
import random
import math
import json
import os
from datetime import datetime
from collections import deque
import numpy as np


class AIGameMaster:
    """AI that learns player patterns and adapts game difficulty"""
    
    def __init__(self):
        self.player_data = {
            'games_played': 0,
            'avg_score': 0,
            'avg_game_time': 0,
            'movement_patterns': [],
            'death_causes': {'wall': 0, 'self': 0},
            'preferred_directions': {'up': 0, 'down': 0, 'left': 0, 'right': 0},
            'reaction_times': [],
            'skill_level': 'beginner'  # beginner, intermediate, advanced, expert
        }
        self.load_player_data()
        
        # AI decision parameters
        self.base_speed = 10
        self.current_speed = 10
        self.power_up_frequency = 0.3
        self.obstacle_chance = 0.0
        
    def load_player_data(self):
        """Load player statistics from file"""
        try:
            if os.path.exists('snake_ai_data.json'):
                with open('snake_ai_data.json', 'r') as f:
                    self.player_data.update(json.load(f))
        except Exception as e:
            print(f"Could not load player data: {e}")
    
    def save_player_data(self):
        """Save player statistics to file"""
        try:
            with open('snake_ai_data.json', 'w') as f:
                json.dump(self.player_data, f, indent=2)
        except Exception as e:
            print(f"Could not save player data: {e}")
    
    def analyze_skill_level(self):
        """Determine player skill level based on performance"""
        if self.player_data['games_played'] < 3:
            return 'beginner'
        
        avg_score = self.player_data['avg_score']
        avg_time = self.player_data['avg_game_time']
        
        if avg_score > 200 and avg_time > 120:
            return 'expert'
        elif avg_score > 100 and avg_time > 60:
            return 'advanced'
        elif avg_score > 50 and avg_time > 30:
            return 'intermediate'
        else:
            return 'beginner'
    
    def adapt_difficulty(self, current_score, game_time):
        """Dynamically adjust game difficulty based on performance"""
        skill = self.analyze_skill_level()
        self.player_data['skill_level'] = skill
        
        # Adjust speed based on skill and current performance
        base_speeds = {
            'beginner': 8,
            'intermediate': 12,
            'advanced': 16,
            'expert': 20
        }
        
        self.base_speed = base_speeds[skill]
        
        # Dynamic speed adjustment during game
        if current_score > self.player_data['avg_score'] * 1.2:
            self.current_speed = min(self.base_speed + 3, 25)
        elif current_score < self.player_data['avg_score'] * 0.8:
            self.current_speed = max(self.base_speed - 2, 6)
        else:
            self.current_speed = self.base_speed
        
        # Adjust power-up frequency
        if skill == 'beginner':
            self.power_up_frequency = 0.4
        elif skill == 'expert':
            self.power_up_frequency = 0.2
        else:
            self.power_up_frequency = 0.3
    
    def predict_next_move(self, snake_head, last_direction):
        """Predict player's likely next move based on patterns"""
        # Simple prediction based on movement history
        if not self.player_data['movement_patterns']:
            return None
        
        # Analyze recent patterns
        recent_patterns = self.player_data['movement_patterns'][-10:]
        direction_weights = {}
        
        for pattern in recent_patterns:
            for direction in pattern:
                direction_weights[direction] = direction_weights.get(direction, 0) + 1
        
        if direction_weights:
            predicted = max(direction_weights, key=direction_weights.get)
            return predicted
        
        return None
    
    def should_spawn_power_up(self, current_score, snake_length):
        """AI decides when to spawn power-ups strategically"""
        # More likely to spawn power-ups if player is struggling
        if current_score < self.player_data['avg_score'] * 0.7:
            return random.random() < self.power_up_frequency * 1.5
        
        # Regular spawn rate
        return random.random() < self.power_up_frequency
    
    def update_player_stats(self, score, game_time, death_cause, movements):
        """Update player statistics after game ends"""
        self.player_data['games_played'] += 1
        
        # Update averages
        games = self.player_data['games_played']
        self.player_data['avg_score'] = (
            (self.player_data['avg_score'] * (games - 1) + score) / games
        )
        self.player_data['avg_game_time'] = (
            (self.player_data['avg_game_time'] * (games - 1) + game_time) / games
        )
        
        # Update death causes
        self.player_data['death_causes'][death_cause] += 1
        
        # Update movement patterns
        self.player_data['movement_patterns'].append(movements[-20:])  # Last 20 moves
        if len(self.player_data['movement_patterns']) > 50:
            self.player_data['movement_patterns'].pop(0)
        
        # Update preferred directions
        for direction in movements:
            if direction in self.player_data['preferred_directions']:
                self.player_data['preferred_directions'][direction] += 1
        
        self.save_player_data()


class RetroSnakeGame:
    """Main game class with retro aesthetics and AI integration"""
    
    def __init__(self):
        pygame.init()
        
        # Game constants
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 600
        self.GRID_SIZE = 20
        self.GRID_WIDTH = self.WINDOW_WIDTH // self.GRID_SIZE
        self.GRID_HEIGHT = (self.WINDOW_HEIGHT - 100) // self.GRID_SIZE  # Leave space for UI
        
        # Colors (Win95 inspired)
        self.COLORS = {
            'bg': (192, 192, 192),  # Classic Windows gray
            'snake': (0, 128, 0),   # Classic green
            'food': (255, 0, 0),    # Classic red
            'power_up': (255, 255, 0),  # Yellow
            'ui_bg': (192, 192, 192),
            'ui_border': (128, 128, 128),
            'text': (0, 0, 0),
            'button': (192, 192, 192),
            'button_pressed': (160, 160, 160)
        }
        
        # Initialize display
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Retro AI Snake - Win95 Style")
        
        # Fonts
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)
        
        # Game state
        self.clock = pygame.time.Clock()
        self.ai_master = AIGameMaster()
        self.reset_game()
        
    def reset_game(self):
        """Reset game to initial state"""
        # Snake
        start_x = self.GRID_WIDTH // 2
        start_y = self.GRID_HEIGHT // 2
        self.snake = deque([(start_x, start_y)])
        self.direction = 'right'
        self.last_direction = 'right'
        
        # Game objects
        self.food = self.spawn_food()
        self.power_ups = []
        self.obstacles = []
        
        # Game state
        self.score = 0
        self.game_over = False
        self.paused = False
        self.start_time = datetime.now()
        self.movement_history = []
        
        # AI predictions
        self.ai_prediction = None
        self.show_ai_hints = True
        
    def spawn_food(self):
        """Spawn food at random location"""
        while True:
            x = random.randint(0, self.GRID_WIDTH - 1)
            y = random.randint(0, self.GRID_HEIGHT - 1)
            if (x, y) not in self.snake:
                return (x, y)
    
    def spawn_power_up(self):
        """Spawn power-up at random location"""
        while True:
            x = random.randint(0, self.GRID_WIDTH - 1)
            y = random.randint(0, self.GRID_HEIGHT - 1)
            if (x, y) not in self.snake and (x, y) != self.food:
                return {
                    'pos': (x, y),
                    'type': random.choice(['speed_boost', 'score_multiplier', 'invincible']),
                    'timer': 300  # 5 seconds at 60 FPS
                }
    
    def handle_input(self):
        """Handle player input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_SPACE:
                    if self.game_over:
                        self.reset_game()
                    else:
                        self.paused = not self.paused
                elif event.key == pygame.K_h:
                    self.show_ai_hints = not self.show_ai_hints
                elif not self.paused and not self.game_over:
                    # Movement keys
                    new_direction = None
                    if event.key == pygame.K_UP and self.direction != 'down':
                        new_direction = 'up'
                    elif event.key == pygame.K_DOWN and self.direction != 'up':
                        new_direction = 'down'
                    elif event.key == pygame.K_LEFT and self.direction != 'right':
                        new_direction = 'left'
                    elif event.key == pygame.K_RIGHT and self.direction != 'left':
                        new_direction = 'right'
                    
                    if new_direction:
                        self.direction = new_direction
                        self.movement_history.append(new_direction)
        
        return True
    
    def update_game(self):
        """Update game logic"""
        if self.paused or self.game_over:
            return
        
        # AI adapts difficulty
        game_time = (datetime.now() - self.start_time).total_seconds()
        self.ai_master.adapt_difficulty(self.score, game_time)
        
        # AI prediction
        head = self.snake[0]
        self.ai_prediction = self.ai_master.predict_next_move(head, self.last_direction)
        
        # Move snake
        head_x, head_y = head
        
        if self.direction == 'up':
            head_y -= 1
        elif self.direction == 'down':
            head_y += 1
        elif self.direction == 'left':
            head_x -= 1
        elif self.direction == 'right':
            head_x += 1
        
        new_head = (head_x, head_y)
        
        # Check collisions
        death_cause = None
        
        # Wall collision
        if (head_x < 0 or head_x >= self.GRID_WIDTH or 
            head_y < 0 or head_y >= self.GRID_HEIGHT):
            death_cause = 'wall'
        
        # Self collision
        elif new_head in self.snake:
            death_cause = 'self'
        
        if death_cause:
            self.game_over = True
            game_time = (datetime.now() - self.start_time).total_seconds()
            self.ai_master.update_player_stats(
                self.score, game_time, death_cause, self.movement_history
            )
            return
        
        self.snake.appendleft(new_head)
        self.last_direction = self.direction
        
        # Check food collision
        if new_head == self.food:
            self.score += 10
            self.food = self.spawn_food()
            
            # AI decides if power-up should spawn
            if self.ai_master.should_spawn_power_up(self.score, len(self.snake)):
                self.power_ups.append(self.spawn_power_up())
        else:
            self.snake.pop()
        
        # Check power-up collisions
        for power_up in self.power_ups[:]:
            if new_head == power_up['pos']:
                self.handle_power_up(power_up)
                self.power_ups.remove(power_up)
        
        # Update power-up timers
        for power_up in self.power_ups[:]:
            power_up['timer'] -= 1
            if power_up['timer'] <= 0:
                self.power_ups.remove(power_up)
    
    def handle_power_up(self, power_up):
        """Handle power-up collection"""
        if power_up['type'] == 'score_multiplier':
            self.score += 50
        elif power_up['type'] == 'speed_boost':
            self.score += 25
        elif power_up['type'] == 'invincible':
            self.score += 30
    
    def draw_retro_button(self, surface, rect, text, pressed=False):
        """Draw a Win95-style button"""
        color = self.COLORS['button_pressed'] if pressed else self.COLORS['button']
        
        # Main button area
        pygame.draw.rect(surface, color, rect)
        
        # 3D effect borders
        if not pressed:
            # Light borders (top and left)
            pygame.draw.line(surface, (255, 255, 255), 
                           (rect.left, rect.top), (rect.right-1, rect.top), 2)
            pygame.draw.line(surface, (255, 255, 255), 
                           (rect.left, rect.top), (rect.left, rect.bottom-1), 2)
            
            # Dark borders (bottom and right)
            pygame.draw.line(surface, (128, 128, 128), 
                           (rect.left+1, rect.bottom-1), (rect.right-1, rect.bottom-1), 2)
            pygame.draw.line(surface, (128, 128, 128), 
                           (rect.right-1, rect.top+1), (rect.right-1, rect.bottom-1), 2)
        
        # Button text
        text_surface = self.font_medium.render(text, True, self.COLORS['text'])
        text_rect = text_surface.get_rect(center=rect.center)
        if pressed:
            text_rect.x += 1
            text_rect.y += 1
        surface.blit(text_surface, text_rect)
    
    def draw_game(self):
        """Render the game"""
        self.screen.fill(self.COLORS['bg'])
        
        # Draw game area border (Win95 style inset)
        game_rect = pygame.Rect(10, 10, self.WINDOW_WIDTH-20, self.GRID_HEIGHT * self.GRID_SIZE + 20)
        pygame.draw.rect(self.screen, (128, 128, 128), game_rect, 2)
        pygame.draw.rect(self.screen, (255, 255, 255), 
                        (game_rect.left+2, game_rect.top+2, game_rect.width-4, game_rect.height-4), 1)
        
        # Game area background
        game_bg = pygame.Rect(15, 15, self.WINDOW_WIDTH-30, self.GRID_HEIGHT * self.GRID_SIZE + 10)
        pygame.draw.rect(self.screen, (0, 0, 0), game_bg)
        
        # Draw snake
        for i, segment in enumerate(self.snake):
            x = 15 + segment[0] * self.GRID_SIZE
            y = 15 + segment[1] * self.GRID_SIZE
            
            # Snake head is brighter
            color = (0, 255, 0) if i == 0 else self.COLORS['snake']
            pygame.draw.rect(self.screen, color, 
                           (x, y, self.GRID_SIZE-1, self.GRID_SIZE-1))
            
            # Add retro pixel effect
            pygame.draw.rect(self.screen, (255, 255, 255), 
                           (x, y, 3, 3))
        
        # Draw food
        food_x = 15 + self.food[0] * self.GRID_SIZE
        food_y = 15 + self.food[1] * self.GRID_SIZE
        pygame.draw.rect(self.screen, self.COLORS['food'], 
                        (food_x, food_y, self.GRID_SIZE-1, self.GRID_SIZE-1))
        
        # Draw power-ups
        for power_up in self.power_ups:
            x = 15 + power_up['pos'][0] * self.GRID_SIZE
            y = 15 + power_up['pos'][1] * self.GRID_SIZE
            
            # Blinking effect
            if (power_up['timer'] // 10) % 2:
                pygame.draw.rect(self.screen, self.COLORS['power_up'], 
                               (x, y, self.GRID_SIZE-1, self.GRID_SIZE-1))
        
        # Draw UI panel
        ui_y = self.GRID_HEIGHT * self.GRID_SIZE + 30
        ui_rect = pygame.Rect(10, ui_y, self.WINDOW_WIDTH-20, 80)
        self.draw_retro_button(self.screen, ui_rect, "", False)
        
        # Score and stats
        score_text = self.font_large.render(f"Score: {self.score}", True, self.COLORS['text'])
        self.screen.blit(score_text, (20, ui_y + 10))
        
        # AI info
        skill_text = self.font_medium.render(f"AI Skill Assessment: {self.ai_master.player_data['skill_level'].title()}", 
                                           True, self.COLORS['text'])
        self.screen.blit(skill_text, (20, ui_y + 40))
        
        speed_text = self.font_medium.render(f"Speed: {self.ai_master.current_speed}", 
                                           True, self.COLORS['text'])
        self.screen.blit(speed_text, (300, ui_y + 40))
        
        # AI prediction hint
        if self.show_ai_hints and self.ai_prediction:
            hint_text = self.font_small.render(f"AI Predicts: {self.ai_prediction.upper()}", 
                                             True, (0, 0, 255))
            self.screen.blit(hint_text, (500, ui_y + 10))
        
        # Controls
        controls_text = self.font_small.render("SPACE: Pause | H: Toggle AI Hints | ESC: Quit", 
                                             True, self.COLORS['text'])
        self.screen.blit(controls_text, (20, ui_y + 60))
        
        # Game over screen
        if self.game_over:
            overlay = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            
            # Game over dialog (Win95 style)
            dialog_rect = pygame.Rect(200, 200, 400, 200)
            self.draw_retro_button(self.screen, dialog_rect, "", False)
            
            game_over_text = self.font_large.render("Game Over!", True, self.COLORS['text'])
            text_rect = game_over_text.get_rect(center=(dialog_rect.centerx, dialog_rect.y + 40))
            self.screen.blit(game_over_text, text_rect)
            
            final_score = self.font_medium.render(f"Final Score: {self.score}", True, self.COLORS['text'])
            text_rect = final_score.get_rect(center=(dialog_rect.centerx, dialog_rect.y + 80))
            self.screen.blit(final_score, text_rect)
            
            games_played = self.font_medium.render(f"Games Played: {self.ai_master.player_data['games_played']}", 
                                                 True, self.COLORS['text'])
            text_rect = games_played.get_rect(center=(dialog_rect.centerx, dialog_rect.y + 110))
            self.screen.blit(games_played, text_rect)
            
            restart_text = self.font_medium.render("Press SPACE to play again", True, self.COLORS['text'])
            text_rect = restart_text.get_rect(center=(dialog_rect.centerx, dialog_rect.y + 150))
            self.screen.blit(restart_text, text_rect)
        
        # Pause screen
        elif self.paused:
            pause_text = self.font_large.render("PAUSED", True, (255, 255, 0))
            text_rect = pause_text.get_rect(center=(self.WINDOW_WIDTH//2, self.WINDOW_HEIGHT//2))
            self.screen.blit(pause_text, text_rect)
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            running = self.handle_input()
            self.update_game()
            self.draw_game()
            
            # AI-controlled frame rate
            self.clock.tick(self.ai_master.current_speed)
        
        pygame.quit()


def main():
    """Entry point"""
    print("🐍 Retro AI Snake - Win95 Edition")
    print("=" * 40)
    print("Features:")
    print("• Classic Snake gameplay with Win95 aesthetics")
    print("• AI learns your playing patterns")
    print("• Dynamic difficulty adjustment")
    print("• Smart power-up spawning")
    print("• Movement prediction hints")
    print("\nControls:")
    print("• Arrow Keys: Move snake")
    print("• SPACE: Pause/Resume (or restart when game over)")
    print("• H: Toggle AI prediction hints")
    print("• ESC: Quit")
    print("\nStarting game...")
    
    game = RetroSnakeGame()
    game.run()


if __name__ == "__main__":
    main()