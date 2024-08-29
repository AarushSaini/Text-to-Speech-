import pyttsx3
import logging
import os
import configparser

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration file handling
CONFIG_FILE = 'tts_config.ini'

def load_configuration():
    config = configparser.ConfigParser()

    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
        logger.info(f"Loaded configuration from {CONFIG_FILE}.")
    else:
        logger.warning(f"{CONFIG_FILE} not found. Using environment variables or defaults.")

    # Fetch configuration from file, environment, or default
    rate = config.getint('Settings', 'rate', fallback=int(os.getenv('TTS_RATE', 100)))
    volume = config.getfloat('Settings', 'volume', fallback=float(os.getenv('TTS_VOLUME', 1.0)))
    voice = config.get('Settings', 'voice', fallback=os.getenv('TTS_VOICE', 'female'))

    return {'rate': rate, 'volume': volume, 'voice': voice}

def initialize_engine(config):
    engine = pyttsx3.init()
    engine.setProperty('rate', config['rate'])
    engine.setProperty('volume', config['volume'])

    voices = engine.getProperty('voices')
    selected_voice = voices[1].id if config['voice'].lower() == 'female' else voices[0].id
    engine.setProperty('voice', selected_voice)

    logger.info(f"Engine initialized with rate={config['rate']}, volume={config['volume']}, voice={config['voice']}.")

    return engine

def text_to_speech(engine, text):
    try:
        engine.say(text)
        engine.runAndWait()
        logger.info("Text-to-speech conversion successful.")
    except Exception as e:
        logger.error(f"Failed to convert text to speech: {e}")

def main():
    config = load_configuration()
    engine = initialize_engine(config)

    while True:
        text = input("Enter the text you want to listen (or type 'exit' to quit): ")
        if text.lower() == 'exit':
            logger.info("Exiting the program.")
            break
        if not text.strip():
            logger.warning("Empty input received. Prompting user again.")
            print("Empty input. Please enter some text.")
            continue

        text_to_speech(engine, text)

if __name__ == "__main__":
    main()
