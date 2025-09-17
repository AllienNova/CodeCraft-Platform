/**
 * Professor Sparkle Voice Integration
 * 
 * Handles real-time voice interaction with Professor Sparkle AI tutor
 * using Gemini Live API and WebSocket connections
 */

class ProfessorSparkleVoice {
    constructor() {
        this.isInitialized = false;
        this.isListening = false;
        this.isConnected = false;
        this.websocket = null;
        this.sessionId = null;
        this.mediaRecorder = null;
        this.audioChunks = [];
        this.childProfile = null;
        
        // Audio context for voice processing
        this.audioContext = null;
        this.microphone = null;
        this.analyser = null;
        
        // UI elements
        this.sparkleButton = null;
        this.sparkleAvatar = null;
        this.voiceIndicator = null;
        this.responseArea = null;
        
        // Voice recognition settings
        this.voiceThreshold = 0.01;
        this.silenceTimeout = 2000; // 2 seconds of silence
        this.maxRecordingTime = 30000; // 30 seconds max
        
        this.init();
    }
    
    async init() {
        try {
            await this.setupAudioContext();
            this.createUI();
            this.setupEventListeners();
            this.isInitialized = true;
            console.log('✨ Professor Sparkle Voice initialized successfully!');
        } catch (error) {
            console.error('Failed to initialize Professor Sparkle Voice:', error);
            this.showError('Voice features are not available in this browser.');
        }
    }
    
    async setupAudioContext() {
        // Check for browser support
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            throw new Error('Voice features not supported in this browser');
        }
        
        // Initialize audio context
        this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
        
        // Request microphone access
        const stream = await navigator.mediaDevices.getUserMedia({ 
            audio: {
                echoCancellation: true,
                noiseSuppression: true,
                autoGainControl: true
            } 
        });
        
        this.microphone = this.audioContext.createMediaStreamSource(stream);
        this.analyser = this.audioContext.createAnalyser();
        this.analyser.fftSize = 256;
        
        this.microphone.connect(this.analyser);
        
        // Setup media recorder for voice capture
        this.mediaRecorder = new MediaRecorder(stream, {
            mimeType: 'audio/webm;codecs=opus'
        });
        
        this.mediaRecorder.ondataavailable = (event) => {
            if (event.data.size > 0) {
                this.audioChunks.push(event.data);
            }
        };
        
        this.mediaRecorder.onstop = () => {
            this.processRecordedAudio();
        };
    }
    
    createUI() {
        // Create Professor Sparkle UI elements
        const sparkleContainer = document.createElement('div');
        sparkleContainer.id = 'professor-sparkle-container';
        sparkleContainer.innerHTML = `
            <div class="sparkle-avatar-container">
                <div class="sparkle-avatar" id="sparkleAvatar">
                    <div class="avatar-face">🧙‍♂️</div>
                    <div class="avatar-sparkles">✨</div>
                    <div class="voice-indicator" id="voiceIndicator"></div>
                </div>
                <div class="sparkle-name">Professor Sparkle</div>
            </div>
            
            <div class="sparkle-controls">
                <button class="sparkle-talk-btn" id="sparkleTalkBtn">
                    <span class="btn-icon">🎤</span>
                    <span class="btn-text">Talk to Professor Sparkle</span>
                </button>
                <div class="voice-status" id="voiceStatus">Ready to help!</div>
            </div>
            
            <div class="sparkle-response" id="sparkleResponse" style="display: none;">
                <div class="response-text" id="responseText"></div>
                <div class="response-audio" id="responseAudio"></div>
                <div class="teaching-hints" id="teachingHints"></div>
            </div>
            
            <div class="sparkle-progress" id="sparkleProgress">
                <div class="progress-label">Learning Progress</div>
                <div class="progress-bar">
                    <div class="progress-fill" id="progressFill" style="width: 0%"></div>
                </div>
                <div class="progress-text" id="progressText">Just getting started!</div>
            </div>
        `;
        
        // Add CSS styles
        const styles = document.createElement('style');
        styles.textContent = `
            #professor-sparkle-container {
                position: fixed;
                bottom: 20px;
                right: 20px;
                width: 320px;
                background: rgba(255, 255, 255, 0.95);
                border-radius: 20px;
                padding: 20px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
                z-index: 1000;
                font-family: 'Comic Sans MS', cursive, sans-serif;
                backdrop-filter: blur(10px);
                border: 2px solid rgba(102, 126, 234, 0.3);
            }
            
            .sparkle-avatar-container {
                text-align: center;
                margin-bottom: 15px;
            }
            
            .sparkle-avatar {
                position: relative;
                width: 80px;
                height: 80px;
                margin: 0 auto 10px;
                background: linear-gradient(135deg, #667eea, #764ba2);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
                transition: transform 0.3s ease;
            }
            
            .sparkle-avatar.talking {
                transform: scale(1.1);
                animation: pulse 1s infinite;
            }
            
            .avatar-face {
                font-size: 36px;
                z-index: 2;
            }
            
            .avatar-sparkles {
                position: absolute;
                top: -10px;
                right: -10px;
                font-size: 20px;
                animation: sparkle 2s infinite;
            }
            
            .voice-indicator {
                position: absolute;
                bottom: -5px;
                left: 50%;
                transform: translateX(-50%);
                width: 20px;
                height: 20px;
                background: #27ae60;
                border-radius: 50%;
                opacity: 0;
                transition: opacity 0.3s;
            }
            
            .voice-indicator.active {
                opacity: 1;
                animation: pulse 1s infinite;
            }
            
            .sparkle-name {
                font-weight: bold;
                color: #667eea;
                font-size: 16px;
            }
            
            .sparkle-controls {
                margin-bottom: 15px;
            }
            
            .sparkle-talk-btn {
                width: 100%;
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 25px;
                cursor: pointer;
                font-size: 14px;
                font-weight: bold;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 8px;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
            }
            
            .sparkle-talk-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
            }
            
            .sparkle-talk-btn.listening {
                background: linear-gradient(135deg, #e74c3c, #c0392b);
                animation: pulse 1s infinite;
            }
            
            .sparkle-talk-btn.processing {
                background: linear-gradient(135deg, #f39c12, #e67e22);
            }
            
            .voice-status {
                text-align: center;
                font-size: 12px;
                color: #666;
                margin-top: 8px;
            }
            
            .sparkle-response {
                background: rgba(102, 126, 234, 0.1);
                border-radius: 15px;
                padding: 15px;
                margin-bottom: 15px;
                border-left: 4px solid #667eea;
            }
            
            .response-text {
                font-size: 14px;
                color: #333;
                line-height: 1.4;
                margin-bottom: 10px;
            }
            
            .teaching-hints {
                font-size: 12px;
                color: #667eea;
                font-style: italic;
            }
            
            .sparkle-progress {
                text-align: center;
            }
            
            .progress-label {
                font-size: 12px;
                color: #666;
                margin-bottom: 5px;
            }
            
            .progress-bar {
                background: #f0f0f0;
                border-radius: 10px;
                height: 6px;
                overflow: hidden;
                margin-bottom: 5px;
            }
            
            .progress-fill {
                background: linear-gradient(90deg, #667eea, #764ba2);
                height: 100%;
                transition: width 0.5s ease;
            }
            
            .progress-text {
                font-size: 11px;
                color: #666;
            }
            
            @keyframes pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.05); }
            }
            
            @keyframes sparkle {
                0%, 100% { transform: rotate(0deg) scale(1); }
                25% { transform: rotate(90deg) scale(1.2); }
                50% { transform: rotate(180deg) scale(1); }
                75% { transform: rotate(270deg) scale(1.2); }
            }
            
            @media (max-width: 768px) {
                #professor-sparkle-container {
                    bottom: 10px;
                    right: 10px;
                    left: 10px;
                    width: auto;
                }
            }
        `;
        
        document.head.appendChild(styles);
        document.body.appendChild(sparkleContainer);
        
        // Store references to UI elements
        this.sparkleButton = document.getElementById('sparkleTalkBtn');
        this.sparkleAvatar = document.getElementById('sparkleAvatar');
        this.voiceIndicator = document.getElementById('voiceIndicator');
        this.responseArea = document.getElementById('sparkleResponse');
        this.voiceStatus = document.getElementById('voiceStatus');
    }
    
    setupEventListeners() {
        this.sparkleButton.addEventListener('click', () => {
            if (this.isListening) {
                this.stopListening();
            } else {
                this.startListening();
            }
        });
        
        // Keyboard shortcut (Space bar to talk)
        document.addEventListener('keydown', (e) => {
            if (e.code === 'Space' && e.target.tagName !== 'INPUT' && e.target.tagName !== 'TEXTAREA') {
                e.preventDefault();
                if (!this.isListening) {
                    this.startListening();
                }
            }
        });
        
        document.addEventListener('keyup', (e) => {
            if (e.code === 'Space' && this.isListening) {
                this.stopListening();
            }
        });
    }
    
    async connectToSparkle(childProfile) {
        try {
            this.childProfile = childProfile;
            
            // Connect to WebSocket
            const wsUrl = `wss://${window.location.host}/ws/sparkle`;
            this.websocket = new WebSocket(wsUrl);
            
            this.websocket.onopen = () => {
                this.isConnected = true;
                this.initializeSession();
                this.updateStatus('Connected to Professor Sparkle! 🪄');
            };
            
            this.websocket.onmessage = (event) => {
                this.handleSparkleResponse(JSON.parse(event.data));
            };
            
            this.websocket.onclose = () => {
                this.isConnected = false;
                this.updateStatus('Disconnected from Professor Sparkle');
            };
            
            this.websocket.onerror = (error) => {
                console.error('WebSocket error:', error);
                this.showError('Connection to Professor Sparkle failed');
            };
            
        } catch (error) {
            console.error('Failed to connect to Professor Sparkle:', error);
            this.showError('Unable to connect to Professor Sparkle');
        }
    }
    
    initializeSession() {
        if (!this.websocket || !this.childProfile) return;
        
        const initMessage = {
            type: 'initialize',
            child_profile: this.childProfile,
            lesson_id: this.getCurrentLessonId()
        };
        
        this.websocket.send(JSON.stringify(initMessage));
    }
    
    getCurrentLessonId() {
        // Get current lesson ID from URL or page context
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get('lesson') || 'mw_001'; // Default to first Magic Workshop lesson
    }
    
    async startListening() {
        if (!this.isInitialized || this.isListening) return;
        
        try {
            this.isListening = true;
            this.audioChunks = [];
            
            // Update UI
            this.sparkleButton.classList.add('listening');
            this.sparkleButton.innerHTML = '<span class="btn-icon">🔴</span><span class="btn-text">Listening...</span>';
            this.sparkleAvatar.classList.add('talking');
            this.voiceIndicator.classList.add('active');
            this.updateStatus('Listening... Speak to Professor Sparkle!');
            
            // Start recording
            this.mediaRecorder.start();
            
            // Auto-stop after max recording time
            setTimeout(() => {
                if (this.isListening) {
                    this.stopListening();
                }
            }, this.maxRecordingTime);
            
            // Monitor for silence
            this.monitorSilence();
            
        } catch (error) {
            console.error('Failed to start listening:', error);
            this.showError('Unable to start voice recording');
            this.resetListeningState();
        }
    }
    
    stopListening() {
        if (!this.isListening) return;
        
        this.isListening = false;
        this.mediaRecorder.stop();
        
        // Update UI
        this.sparkleButton.classList.remove('listening');
        this.sparkleButton.classList.add('processing');
        this.sparkleButton.innerHTML = '<span class="btn-icon">⏳</span><span class="btn-text">Processing...</span>';
        this.sparkleAvatar.classList.remove('talking');
        this.voiceIndicator.classList.remove('active');
        this.updateStatus('Processing your question...');
    }
    
    monitorSilence() {
        if (!this.isListening) return;
        
        const bufferLength = this.analyser.frequencyBinCount;
        const dataArray = new Uint8Array(bufferLength);
        
        const checkSilence = () => {
            if (!this.isListening) return;
            
            this.analyser.getByteFrequencyData(dataArray);
            
            // Calculate average volume
            const average = dataArray.reduce((sum, value) => sum + value, 0) / bufferLength;
            const normalizedVolume = average / 255;
            
            // Update voice indicator based on volume
            if (normalizedVolume > this.voiceThreshold) {
                this.voiceIndicator.style.opacity = Math.min(normalizedVolume * 2, 1);
            } else {
                this.voiceIndicator.style.opacity = 0.3;
            }
            
            requestAnimationFrame(checkSilence);
        };
        
        checkSilence();
    }
    
    async processRecordedAudio() {
        try {
            // Convert audio chunks to blob
            const audioBlob = new Blob(this.audioChunks, { type: 'audio/webm;codecs=opus' });
            
            // Convert to base64 for transmission
            const audioBase64 = await this.blobToBase64(audioBlob);
            
            // Send to Professor Sparkle
            if (this.websocket && this.isConnected) {
                const message = {
                    type: 'voice_input',
                    session_id: this.sessionId,
                    audio_data: audioBase64,
                    timestamp: new Date().toISOString()
                };
                
                this.websocket.send(JSON.stringify(message));
            } else {
                this.showError('Not connected to Professor Sparkle');
                this.resetListeningState();
            }
            
        } catch (error) {
            console.error('Failed to process recorded audio:', error);
            this.showError('Unable to process your voice');
            this.resetListeningState();
        }
    }
    
    handleSparkleResponse(data) {
        switch (data.type) {
            case 'session_initialized':
                this.sessionId = data.data.session_id;
                this.showWelcomeMessage(data.data.welcome_message);
                this.updateProgress(0);
                break;
                
            case 'voice_response':
                this.displayResponse(data.data);
                this.resetListeningState();
                break;
                
            case 'progress_updated':
                this.updateProgress(data.data.lesson_progress);
                break;
                
            default:
                console.log('Unknown message type:', data.type);
        }
    }
    
    showWelcomeMessage(message) {
        this.displayResponse({
            text: message,
            teaching_context: {
                encouragement: "Welcome to your magical coding adventure! 🪄"
            }
        });
    }
    
    displayResponse(responseData) {
        const responseArea = document.getElementById('sparkleResponse');
        const responseText = document.getElementById('responseText');
        const teachingHints = document.getElementById('teachingHints');
        const responseAudio = document.getElementById('responseAudio');
        
        // Display text response
        if (responseData.text) {
            responseText.textContent = responseData.text;
        }
        
        // Display teaching hints
        if (responseData.teaching_context && responseData.teaching_context.encouragement) {
            teachingHints.textContent = responseData.teaching_context.encouragement;
        }
        
        // Play audio response if available
        if (responseData.audio) {
            this.playAudioResponse(responseData.audio);
        }
        
        // Show visual aids if suggested
        if (responseData.teaching_context && responseData.teaching_context.visual_aids) {
            this.showVisualAids(responseData.teaching_context.visual_aids);
        }
        
        // Update progress if provided
        if (responseData.progress_update) {
            this.updateProgress(responseData.progress_update.lesson_progress);
        }
        
        responseArea.style.display = 'block';
        
        // Auto-hide after 10 seconds
        setTimeout(() => {
            responseArea.style.display = 'none';
        }, 10000);
    }
    
    async playAudioResponse(audioData) {
        try {
            // Convert base64 audio to blob and play
            const audioBlob = this.base64ToBlob(audioData, 'audio/webm');
            const audioUrl = URL.createObjectURL(audioBlob);
            
            const audio = new Audio(audioUrl);
            audio.play();
            
            // Animate avatar while speaking
            this.sparkleAvatar.classList.add('talking');
            audio.onended = () => {
                this.sparkleAvatar.classList.remove('talking');
                URL.revokeObjectURL(audioUrl);
            };
            
        } catch (error) {
            console.error('Failed to play audio response:', error);
        }
    }
    
    showVisualAids(visualAids) {
        // Highlight specific blocks or elements
        if (visualAids.highlight_blocks) {
            visualAids.highlight_blocks.forEach(blockType => {
                const blocks = document.querySelectorAll(`[data-spell="${blockType}"]`);
                blocks.forEach(block => {
                    block.style.animation = 'pulse 1s ease-in-out 3';
                    setTimeout(() => {
                        block.style.animation = '';
                    }, 3000);
                });
            });
        }
        
        // Show animations
        if (visualAids.show_animation) {
            this.triggerAnimation(visualAids.show_animation);
        }
        
        // Display hints
        if (visualAids.display_hint) {
            this.showHint(visualAids.display_hint);
        }
    }
    
    triggerAnimation(animationType) {
        // Trigger specific animations based on type
        switch (animationType) {
            case 'wizard_walking':
                const wizard = document.getElementById('wizard');
                if (wizard) {
                    wizard.classList.add('moving');
                    setTimeout(() => wizard.classList.remove('moving'), 2000);
                }
                break;
        }
    }
    
    showHint(hintText) {
        const hint = document.createElement('div');
        hint.style.cssText = `
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(102, 126, 234, 0.9);
            color: white;
            padding: 10px 20px;
            border-radius: 20px;
            font-size: 14px;
            z-index: 1001;
            animation: fadeInOut 4s ease-in-out;
        `;
        hint.textContent = hintText;
        
        document.body.appendChild(hint);
        
        setTimeout(() => {
            document.body.removeChild(hint);
        }, 4000);
    }
    
    updateProgress(percentage) {
        const progressFill = document.getElementById('progressFill');
        const progressText = document.getElementById('progressText');
        
        if (progressFill) {
            progressFill.style.width = percentage + '%';
        }
        
        if (progressText) {
            if (percentage < 25) {
                progressText.textContent = 'Just getting started! 🌟';
            } else if (percentage < 50) {
                progressText.textContent = 'Making great progress! ✨';
            } else if (percentage < 75) {
                progressText.textContent = 'Doing amazing! 🎉';
            } else if (percentage < 100) {
                progressText.textContent = 'Almost there! 🚀';
            } else {
                progressText.textContent = 'Lesson complete! 🏆';
            }
        }
    }
    
    resetListeningState() {
        this.sparkleButton.classList.remove('listening', 'processing');
        this.sparkleButton.innerHTML = '<span class="btn-icon">🎤</span><span class="btn-text">Talk to Professor Sparkle</span>';
        this.sparkleAvatar.classList.remove('talking');
        this.voiceIndicator.classList.remove('active');
        this.updateStatus('Ready to help!');
    }
    
    updateStatus(message) {
        if (this.voiceStatus) {
            this.voiceStatus.textContent = message;
        }
    }
    
    showError(message) {
        this.updateStatus(`❌ ${message}`);
        setTimeout(() => {
            this.updateStatus('Ready to help!');
        }, 3000);
    }
    
    // Utility functions
    async blobToBase64(blob) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => resolve(reader.result.split(',')[1]);
            reader.onerror = reject;
            reader.readAsDataURL(blob);
        });
    }
    
    base64ToBlob(base64, mimeType) {
        const byteCharacters = atob(base64);
        const byteNumbers = new Array(byteCharacters.length);
        for (let i = 0; i < byteCharacters.length; i++) {
            byteNumbers[i] = byteCharacters.charCodeAt(i);
        }
        const byteArray = new Uint8Array(byteNumbers);
        return new Blob([byteArray], { type: mimeType });
    }
}

// Initialize Professor Sparkle when page loads
document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on a learning page
    if (window.location.pathname.includes('/learning/') || 
        document.querySelector('.magic-container') || 
        document.querySelector('.learning-environment')) {
        
        window.professorSparkle = new ProfessorSparkleVoice();
        
        // Auto-connect if child profile is available
        const childProfile = window.childProfile || {
            id: 'demo_child',
            name: 'Young Coder',
            age: 6,
            tier: 'magic_workshop'
        };
        
        // Connect after a short delay to ensure everything is loaded
        setTimeout(() => {
            window.professorSparkle.connectToSparkle(childProfile);
        }, 1000);
    }
});

// Export for use in other scripts
window.ProfessorSparkleVoice = ProfessorSparkleVoice;

