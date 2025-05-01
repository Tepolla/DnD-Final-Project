from tts_service import KokoroTTSService


def main():
    tts = KokoroTTSService()

    texts = {
        "narrator": "The party enters the ancient forest, where shadows dance between twisted trees.",
        "trader": "Well met, travelers! I've got rare items from across the realms. What are ye lookin' for?",
        "female_narrator": "As moonlight filters through the canopy, the sound of distant whispers grows stronger."
    }

    for voice, text in texts.items():
        print(f"Testing voice: {voice}")
        audio, file_path = tts.generate_speech(text, voice)
        print(f"Generated audio saved to: {file_path}\n")


if __name__ == '__main__':
    main()