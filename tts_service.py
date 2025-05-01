import os
import platform
import soundfile as sf
import subprocess

# Import our new file namer
from audio_file_namer import AudioFileNamer


class KokoroTTSService:
    def __init__(self):
        try:
            from kokoro import KPipeline
            self.pipeline = KPipeline(lang_code='a')  # 'a' for American English
            self.available = True
        except ImportError:
            print("Warning: kokoro module not found. Install with: pip install kokoro")
            self.available = False

        # Initialize our file namer
        self.file_namer = AudioFileNamer()

        self.voices = {
            "narrator": "am_michael",
            "trader": "bm_george",
            "female_narrator": "bf_isabella"
        }

        self.sample_rate = 24000

    def generate_and_play(self, text: str, voice: str = "narrator") -> tuple:
        """Generate speech audio and play it automatically"""
        if not self.available:
            print("Error: TTS service unavailable - kokoro not installed")
            return None, "Error: TTS service unavailable"

        # Determine voice ID - handle both direct IDs and named voices
        if voice in self.voices:
            voice_id = self.voices[voice]
        else:
            voice_id = voice  # Assume it's a direct voice ID

        print(f"Generating speech with voice '{voice_id}': {text[:30]}...")

        # Get sequential filename instead of timestamp
        output_file = self.file_namer.get_next_filename(voice)

        try:
            # Generate audio
            generator = self.pipeline(text, voice=voice_id)
            audio_data = None

            # Process the audio
            for _, (_, _, audio) in enumerate(generator):
                audio_data = audio
                # Save audio to file
                sf.write(output_file, audio, self.sample_rate)
                break  # Only take first segment

            if audio_data is None:
                return None, "Error: No audio generated"

            # Play the audio with better error handling
            self._play_audio(output_file)
            return audio_data, output_file

        except Exception as e:
            print(f"Error in TTS: {e}")
            return None, f"Error: {str(e)}"

    def _play_audio(self, file_path):
        """Play audio using platform-specific methods with better error handling"""
        system = platform.system()

        # Windows playback methods
        if system == "Windows":
            # Try pygame first (most reliable)
            try:
                import pygame
                pygame.mixer.init()
                pygame.mixer.music.load(file_path)
                pygame.mixer.music.play()
                # Wait for playback to finish
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                return
            except ImportError:
                print("For better audio playback, install: pip install pygame")
            except Exception as e:
                print(f"Pygame playback failed: {e}")

            # Try winsound as fallback for Windows
            try:
                import winsound
                winsound.PlaySound(file_path, winsound.SND_FILENAME)
                return
            except ImportError:
                print("WinSound not available")
            except Exception as e:
                print(f"WinSound playback failed: {e}")

        # macOS playback
        elif system == "Darwin":
            try:
                subprocess.call(["afplay", file_path])
                return
            except Exception as e:
                print(f"macOS playback failed: {e}")

        # Linux playback
        else:
            for player in ["aplay", "paplay", "play"]:
                try:
                    subprocess.call([player, file_path])
                    return
                except:
                    continue

        # Final fallback: Try playsound
        try:
            from playsound import playsound
            playsound(file_path)
            return
        except ImportError:
            print("For audio playback, install: pip install playsound")
        except Exception as e:
            print(f"Playsound playback failed: {e}")

        print(f"Audio saved to: {file_path}")
        print("To play audio manually, open the file with your media player")
