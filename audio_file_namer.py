import os

class AudioFileNamer:
    def __init__(self, directory="tts_output"):
        self.directory = directory
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        self.counter = self._get_last_counter() + 1

    def _get_last_counter(self):
        # Find the highest numbered file in the directory
        max_num = 0
        for filename in os.listdir(self.directory):
            if filename.endswith('.wav'):
                parts = filename.split('_')
                if len(parts) >= 2:
                    try:
                        num_part = parts[-1].replace('.wav', '')
                        num = int(num_part)
                        if num > max_num:
                            max_num = num
                    except ValueError:
                        continue
        return max_num

    def get_next_filename(self, voice):
        filename = f"{voice}_{self.counter}.wav"
        self.counter += 1
        return os.path.join(self.directory, filename)