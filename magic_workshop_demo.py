from flask import Flask, render_template_string
import os

app = Flask(__name__)

# Magic Workshop HTML Template
magic_workshop_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Magic Workshop - Codopia</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Comic Sans MS', cursive; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: white;
        }
        .header {
            background: rgba(255,255,255,0.1);
            padding: 20px;
            text-align: center;
            backdrop-filter: blur(10px);
        }
        .workshop-container {
            display: grid;
            grid-template-columns: 1fr 2fr 1fr;
            gap: 20px;
            padding: 20px;
            height: calc(100vh - 100px);
        }
        .spell-blocks {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 20px;
            backdrop-filter: blur(10px);
        }
        .spell-canvas {
            background: rgba(255,255,255,0.95);
            border-radius: 15px;
            padding: 20px;
            color: #333;
            position: relative;
        }
        .magic-stage {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 20px;
            backdrop-filter: blur(10px);
            text-align: center;
        }
        .spell-block {
            background: linear-gradient(45deg, #ff6b6b, #feca57);
            border: none;
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
            color: white;
            font-weight: bold;
            cursor: pointer;
            width: 100%;
            font-size: 14px;
            transition: transform 0.2s;
        }
        .spell-block:hover {
            transform: scale(1.05);
        }
        .movement-spell { background: linear-gradient(45deg, #4ecdc4, #44a08d); }
        .action-spell { background: linear-gradient(45deg, #ff9a9e, #fecfef); }
        .control-spell { background: linear-gradient(45deg, #a8edea, #fed6e3); }
        
        .wizard {
            width: 80px;
            height: 80px;
            background: linear-gradient(45deg, #667eea, #764ba2);
            border-radius: 50%;
            margin: 20px auto;
            position: relative;
            transition: all 0.5s ease;
        }
        .wizard::before {
            content: "🧙‍♂️";
            font-size: 40px;
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
        }
        .sparkle-ai {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 15px;
            margin-top: 20px;
            backdrop-filter: blur(10px);
        }
        .run-spell {
            background: linear-gradient(45deg, #56ab2f, #a8e6cf);
            border: none;
            border-radius: 10px;
            padding: 15px 30px;
            color: white;
            font-weight: bold;
            cursor: pointer;
            font-size: 16px;
            margin: 20px 0;
        }
        .progress-bar {
            background: rgba(255,255,255,0.2);
            border-radius: 10px;
            height: 20px;
            margin: 10px 0;
            overflow: hidden;
        }
        .progress-fill {
            background: linear-gradient(45deg, #56ab2f, #a8e6cf);
            height: 100%;
            width: 30%;
            transition: width 0.5s ease;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>✨ Magic Workshop ✨</h1>
        <p>Create magical spells with code blocks!</p>
        <div class="progress-bar">
            <div class="progress-fill"></div>
        </div>
        <p>Lesson 1: Making the Wizard Move</p>
    </div>
    
    <div class="workshop-container">
        <div class="spell-blocks">
            <h3>🪄 Spell Blocks</h3>
            <button class="spell-block movement-spell" onclick="addSpell('Move Forward')">
                🏃‍♂️ Move Forward
            </button>
            <button class="spell-block movement-spell" onclick="addSpell('Turn Left')">
                ↪️ Turn Left
            </button>
            <button class="spell-block movement-spell" onclick="addSpell('Turn Right')">
                ↩️ Turn Right
            </button>
            <button class="spell-block action-spell" onclick="addSpell('Cast Sparkles')">
                ✨ Cast Sparkles
            </button>
            <button class="spell-block action-spell" onclick="addSpell('Say Hello')">
                👋 Say Hello
            </button>
            <button class="spell-block control-spell" onclick="addSpell('Repeat 3 times')">
                🔄 Repeat 3 times
            </button>
            
            <div class="sparkle-ai">
                <h4>🧙‍♂️ Professor Sparkle</h4>
                <p id="sparkle-message">"Welcome, young wizard! Drag spell blocks to create your first magical program!"</p>
                <button onclick="askSparkle()" style="background: #667eea; border: none; color: white; padding: 10px; border-radius: 5px; margin-top: 10px;">
                    🎙️ Talk to Professor Sparkle
                </button>
            </div>
        </div>
        
        <div class="spell-canvas">
            <h3>📜 Your Magical Spell</h3>
            <div id="spell-sequence" style="min-height: 200px; border: 2px dashed #ccc; border-radius: 10px; padding: 20px; margin: 20px 0;">
                <p style="color: #999; text-align: center;">Drag spell blocks here to create your program!</p>
            </div>
            <button class="run-spell" onclick="runSpell()">
                🚀 Cast Your Spell!
            </button>
            <button onclick="clearSpell()" style="background: #ff6b6b; border: none; color: white; padding: 10px 20px; border-radius: 5px; margin-left: 10px;">
                🗑️ Clear Spell
            </button>
        </div>
        
        <div class="magic-stage">
            <h3>🎭 Magic Stage</h3>
            <div class="wizard" id="wizard"></div>
            <div id="magic-output">
                <p>Your wizard is ready for adventure!</p>
            </div>
            <div style="margin-top: 20px;">
                <h4>🏆 Achievements</h4>
                <div id="achievements">
                    <p>🌟 First Spell: Not yet earned</p>
                    <p>⭐ Spell Master: Not yet earned</p>
                    <p>✨ Magic Points: 0</p>
                </div>
            </div>
        </div>
    </div>

    <script>
        let spellSequence = [];
        let magicPoints = 0;
        
        function addSpell(spellName) {
            spellSequence.push(spellName);
            updateSpellCanvas();
            updateSparkleMessage("Great choice! " + spellName + " added to your spell!");
        }
        
        function updateSpellCanvas() {
            const canvas = document.getElementById('spell-sequence');
            if (spellSequence.length === 0) {
                canvas.innerHTML = '<p style="color: #999; text-align: center;">Drag spell blocks here to create your program!</p>';
                return;
            }
            
            let html = '';
            spellSequence.forEach((spell, index) => {
                html += `<div style="background: linear-gradient(45deg, #667eea, #764ba2); color: white; padding: 10px; margin: 5px 0; border-radius: 8px; display: flex; justify-content: space-between; align-items: center;">
                    <span>${index + 1}. ${spell}</span>
                    <button onclick="removeSpell(${index})" style="background: rgba(255,255,255,0.2); border: none; color: white; padding: 5px 10px; border-radius: 5px; cursor: pointer;">❌</button>
                </div>`;
            });
            canvas.innerHTML = html;
        }
        
        function removeSpell(index) {
            spellSequence.splice(index, 1);
            updateSpellCanvas();
        }
        
        function clearSpell() {
            spellSequence = [];
            updateSpellCanvas();
            updateSparkleMessage("Spell cleared! Ready for a new magical creation!");
        }
        
        function runSpell() {
            if (spellSequence.length === 0) {
                updateSparkleMessage("You need to add some spell blocks first, young wizard!");
                return;
            }
            
            const wizard = document.getElementById('wizard');
            const output = document.getElementById('magic-output');
            
            // Animate the wizard
            wizard.style.transform = 'scale(1.2) rotate(360deg)';
            setTimeout(() => {
                wizard.style.transform = 'scale(1) rotate(0deg)';
            }, 1000);
            
            // Execute spell sequence
            let outputText = '<h4>🎭 Spell Execution:</h4>';
            spellSequence.forEach((spell, index) => {
                outputText += `<p>${index + 1}. ${spell} ✨</p>`;
            });
            
            output.innerHTML = outputText;
            
            // Award achievements
            magicPoints += spellSequence.length * 10;
            updateAchievements();
            updateSparkleMessage(`Magnificent! Your spell worked perfectly! You earned ${spellSequence.length * 10} magic points!`);
        }
        
        function updateAchievements() {
            const achievements = document.getElementById('achievements');
            let html = '';
            
            if (spellSequence.length > 0) {
                html += '<p>🌟 First Spell: ✅ Earned!</p>';
            } else {
                html += '<p>🌟 First Spell: Not yet earned</p>';
            }
            
            if (magicPoints >= 50) {
                html += '<p>⭐ Spell Master: ✅ Earned!</p>';
            } else {
                html += '<p>⭐ Spell Master: Not yet earned</p>';
            }
            
            html += `<p>✨ Magic Points: ${magicPoints}</p>`;
            achievements.innerHTML = html;
        }
        
        function updateSparkleMessage(message) {
            document.getElementById('sparkle-message').innerHTML = `"${message}"`;
        }
        
        function askSparkle() {
            const messages = [
                "Try combining movement spells with action spells for more magic!",
                "Did you know you can repeat spells to make patterns?",
                "Great job, young wizard! You're learning the art of magical programming!",
                "Remember, every great wizard started with simple spells like yours!",
                "What happens if you add 'Cast Sparkles' after 'Move Forward'? Try it!",
                "You're doing wonderfully! Programming is just like casting spells - you give instructions step by step!"
            ];
            const randomMessage = messages[Math.floor(Math.random() * messages.length)];
            updateSparkleMessage(randomMessage);
        }
        
        // Initialize with a welcome message
        setTimeout(() => {
            updateSparkleMessage("Welcome to the Magic Workshop! Click on spell blocks to add them to your magical program. When you're ready, cast your spell to see the magic happen!");
        }, 1000);
    </script>
</body>
</html>
'''

@app.route('/')
def magic_workshop():
    return render_template_string(magic_workshop_html)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
