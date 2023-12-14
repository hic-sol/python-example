###
# Code for handling the gpt-2 algorithm
###

import gpt_2_simple as gpt2


class Algorithm:
    def __init__(self):
        self.sess = gpt2.start_tf_sess()
        self.gpt_run_name = "locations"
        gpt2.load_gpt2(self.sess, run_name=self.gpt_run_name)

    def generate(self, prefix, trunc="<|endoftext|>", temp=1.0, include=True, length=50):
        return gpt2.generate(self.sess, run_name=self.gpt_run_name, length=length, truncate=trunc, prefix=prefix,
                             return_as_list=True, temperature=temp, include_prefix=include)[0]

    def generate_room(self, location):
        prefix = "ROOM:\nLocation: %s\n" % location
        text = self.generate(prefix)
        subtext = text.split("Description: ")
        if subtext[1]:
            return subtext[1]
        else:
            return "A barren room"

    def generate_first_room_location(self):
        prefix = "ROOM:\nLocation: "
        text = self.generate(prefix)
        subtext = text.split("\nDescription: ")
        if len(subtext) >= 2:
            return subtext[0], subtext[1]
        else:
            return "Nowhere", "A barren room"

    def generate_item(self):
        prefix = "This object is the"
        postfix = "."
        text = self.generate(prefix, postfix, temp=1.6, length=20)
        subtext1 = text.split("This object is the ")
        subtext2 = subtext1[1].split(" ")
        return subtext2[0].strip(), text

    def generate_character(self):
        name = self.generate("", "", temp=10, length=1)
        prefix = name + " is a person who"
        text = self.generate(prefix, ".", temp=1.6, length=20)
        return name.strip(), text
