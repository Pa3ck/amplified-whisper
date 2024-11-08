try:
    from pyannote.audio import Model
    from pyannote.audio.pipelines.speaker_verification import PretrainedSpeakerEmbedding
    from pyannote.audio.utils.powerset import Powerset

    IS_PYANNOTE_AVAILABLE = True
except ImportError as e:
    print(f"ImportError: {e}")
    IS_PYANNOTE_AVAILABLE = False


print("IS_PYANNOTE_AVAILABLE ")
print(IS_PYANNOTE_AVAILABLE)

import os
running_in_virtualenv = "VIRTUAL_ENV" in os.environ

# alternative ways to write this, also supporting the case where
# the variable is set but contains an empty string to indicate
# 'not in a virtual environment':
running_in_virtualenv = bool(os.environ.get("VIRTUAL_ENV"))
running_in_virtualenv = bool(os.getenv("VIRTUAL_ENV"))

print(running_in_virtualenv)