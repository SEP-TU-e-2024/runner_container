from validator.IOModule import IOModule


class Validator(IOModule):
    def __init__(self):

        # Values chosen for a simple '1+1=2' test
        with open('./instances/instance', 'r') as f:
            a, b, c = f.readlines()
            
            self.input_sequence = [a, b]
            self.obtained_answers = []
            self.expected_answers = [c]
            self.sequence_index = 0

    def _scoring_function(self, obtained_answer: str, expected_answer: str) -> int:
        """Function to evaluate the obtained answer against the expected answer."""
        return 1 if obtained_answer == expected_answer else 0
    
    def _score(self):
        # calculate the scores
        scores = [self._scoring_function(obtained_answer, expected_answer) for
                  obtained_answer, expected_answer in
                  zip(self.obtained_answers, self.expected_answers)]
        
        # calculate the sum of the scores
        return {"score":sum(scores)}

    def obtain_data(self, prompt: str) -> str:
        """Data input function. Replaces input()."""
        if self.sequence_index < len(self.input_sequence):
            user_input = self.input_sequence[self.sequence_index]
            self.sequence_index += 1
        else:
            user_input = 0 # Value after running out of values
        
        return user_input

    def push_data(self, text: str) -> float:
        """Data output function. Replaces print()."""
        obtained_answer = text
        self.obtained_answers.append(obtained_answer)
        return 1 # a 'goodness' value can be returned, for dynamic problems

    def obtain_dataset(self) -> list: # optional
        """Data input function. Replaces a sequence of input() calls."""
        return self.input_sequence