# voice_assistant/config.py

import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class Config:
    """
    Configuration class to hold the model selection and API keys.
    
    Attributes:
        TRANSCRIPTION_MODEL (str): The model to use for transcription ('openai', 'groq', 'deepgram', 'fastwhisperapi', 'local').
        RESPONSE_MODEL (str): The model to use for response generation ('openai', 'groq', 'local').
        TTS_MODEL (str): The model to use for text-to-speech ('openai', 'deepgram', 'elevenlabs', 'local').
        OPENAI_API_KEY (str): API key for OpenAI services.
        GROQ_API_KEY (str): API key for Groq services.
        DEEPGRAM_API_KEY (str): API key for Deepgram services.
        ELEVENLABS_API_KEY (str): API key for ElevenLabs services.
        LOCAL_MODEL_PATH (str): Path to the local model.
    """
    # Model selection
    TRANSCRIPTION_MODEL = 'deepgram'  # possible values: openai, groq, deepgram, fastwhisperapi
    RESPONSE_MODEL = 'openai'  # possible values: openai, groq, ollama
    TTS_MODEL = 'openai'  # possible values: openai, deepgram, elevenlabs, melotts, cartesia, piper

    # Piper Server configuration
    PIPER_SERVER_URL = os.getenv("PIPER_SERVER_URL")
    PIPER_OUTPUT_FILE = "output.wav"

    # currently using the MeloTTS for local models. here is how to get started:
    # https://github.com/myshell-ai/MeloTTS/blob/main/docs/install.md#linux-and-macos-install

    # LLM Selection
    OLLAMA_LLM="llama3:8b"
    GROQ_LLM="llama3-8b-8192"
    OPENAI_LLM="gpt-4o"

    # API keys and paths
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
    LOCAL_MODEL_PATH = os.getenv("LOCAL_MODEL_PATH")
    CARTESIA_API_KEY = os.getenv("CARTESIA_API_KEY")

    # for serving the MeloTTS model
    TTS_PORT_LOCAL = 5150

    # temp file generated by the initial STT model
    INPUT_AUDIO = "test.mp3"

    @staticmethod
    def validate_config():
        """
        Validate the configuration to ensure all necessary environment variables are set.
        
        Raises:
            ValueError: If a required environment variable is not set.
        """
        Config._validate_model('TRANSCRIPTION_MODEL', [
            'openai', 'groq', 'deepgram', 'fastwhisperapi', 'local'])
        Config._validate_model('RESPONSE_MODEL', [
            'openai', 'groq', 'ollama', 'local'])
        Config._validate_model('TTS_MODEL', [
            'openai', 'deepgram', 'elevenlabs', 'melotts', 'cartesia', 'local', 'piper'])

        Config._validate_api_key('TRANSCRIPTION_MODEL', 'openai', 'OPENAI_API_KEY')
        Config._validate_api_key('TRANSCRIPTION_MODEL', 'groq', 'GROQ_API_KEY')
        Config._validate_api_key('TRANSCRIPTION_MODEL', 'deepgram', 'DEEPGRAM_API_KEY')

        Config._validate_api_key('RESPONSE_MODEL', 'openai', 'OPENAI_API_KEY')
        Config._validate_api_key('RESPONSE_MODEL', 'groq', 'GROQ_API_KEY')

        Config._validate_api_key('TTS_MODEL', 'openai', 'OPENAI_API_KEY')
        Config._validate_api_key('TTS_MODEL', 'deepgram', 'DEEPGRAM_API_KEY')
        Config._validate_api_key('TTS_MODEL', 'elevenlabs', 'ELEVENLABS_API_KEY')
        Config._validate_api_key('TTS_MODEL', 'cartesia', 'CARTESIA_API_KEY')

    @staticmethod
    def _validate_model(attribute, valid_options):
        model = getattr(Config, attribute)
        if model not in valid_options:
            raise ValueError(
                f"Invalid {attribute}. Must be one of {valid_options}"
            )
        
    @staticmethod
    def _validate_api_key(model_attr, model_value, api_key_attr):
        if getattr(Config, model_attr) == model_value and not getattr(Config, api_key_attr):
            raise ValueError(f"{api_key_attr} is required for {model_value} models")