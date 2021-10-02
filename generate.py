import pickle
import numpy

from music21 import instrument, note, stream, chord

def generate():
    """ Generate a piano midi file """
    pass


def generate_notes(model, network_input, pitchnames, n_vocab):
    """ Generate notes from neural net based on input sequence of notes. """
    print('Generating notes...')

    # Pick random sequence from input as starting point
    start = numpy.random.randint(0, len(network_input)-1)

    int_to_note = dict((number, note) for number, note in enumerate(pitchnames))

    pattern = network_input[start]
    prediction_output = []

    # Generate 200 notes
    n = 250
    for note_index in range(n):
        prediction_input = numpy.reshape(pattern, (1, len(pattern), 1))
        prediction_input = prediction_input / float(n_vocab)

        prediction = model.predict(prediction_input, verbose=0)

        # Take most probable prediction, convert to note, append to output
        index = numpy.argmax(prediction)
        result = int_to_note[index]
        prediction_output.append(result)

        # Scoot input over by 1 note
        pattern.append(index)
        pattern = pattern[1:len(pattern)]

    return prediction_output


def create_midi(prediction_output):
    print('Creating midi...')
    """ Convert prediction output to notes. Create midi file!!!! """
    offset = 0
    output_notes = []

    stored_instrument = instrument.Guitar()

    # Create Note and Chord objects
    for pattern in prediction_output:
        # Pattern is a Chord
        if ('.' in pattern) or pattern.isdigit():
            notes_in_chord = pattern.split('.')
            notes = []
            for current_note in notes_in_chord:
                new_note = note.Note(int(current_note))
                new_note.storedInstrument = stored_instrument
                notes.append(new_note)

            new_chord = chord.Chord(notes)
            new_chord.offset = offset
            output_notes.append(new_chord)
        else: # Pattern is a note
            new_note = note.Note(pattern)
            new_note.offset = offset
            new_note.storedInstrument = stored_instrument
            output_notes.append(new_note)

        # Increase offset for note
        # Possible extension: ~ RHYTHM ~
        offset += 0.5

    midi_stream = stream.Stream(output_notes)
    midi_stream.write('midi', fp='output_song.mid')


if __name__ == '__main__':
    generate()
