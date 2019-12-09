import numpy as np
from keras.models import Model, Input
from keras.layers import LSTM, Embedding, Dense, Dropout
from keras.preprocessing.sequence import pad_sequences

class IdentifyCommentedOutCode(object):
  CHARS="abcdefghijklmnopqrstuvwxyz0123456789 -,;.!?:'\"/\|_@#$%ˆ&*˜‘+-=()[]{}<>"
  
  def __init__(self, weights_file="./model/weights_file.hdf5", max_line_size=200, model=None):
    print("Initializing identifier" )
    self.weights_file = weights_file 
    self.max_line_size = max_line_size
    self.model = self.lstm_model() if model is None else model()
    self.char2idx = self.set_char_dict()

  def lstm_model(self): 
    print("Creating Model") 
    char_in = Input(shape=(self.max_line_size,))
    emb_char = Embedding(input_dim=len(self.CHARS) + 2, output_dim=32,
                              input_length=self.max_line_size, mask_zero=True)(char_in)
    main_lstm = LSTM(units=200, return_sequences=False,
                                  recurrent_dropout=0.5)(emb_char)
    out = (Dense(8,input_shape=(16,), activation='relu'))(main_lstm)
    #out = Dropout(0.2)(out)
    out = (Dense(1, activation='sigmoid'))(out)
    model = Model(char_in, out)

    model.summary()
    
    print("Loading weights")
    model.load_weights(self.weights_file)

    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["acc"])
    return model

  def set_char_dict(self):
    char2idx = {c: i + 2 for i, c in enumerate(self.CHARS)}
    char2idx["UNK"] = 1
    char2idx["PAD"] = 0
    return char2idx
    
  def transform_sentence(self,senteces):
    processed_sentences = []
    for sentence in senteces:
      sentence = sentence[0:].lower()
      processed_sentence = []
      
      for i in range(self.max_line_size):
        try:
          index = self.char2idx.get(sentence[i])
          if index == None:
            processed_sentence.append(self.char2idx["UNK"])
          else:
            processed_sentence.append(index)
        except:
          processed_sentence.append(self.char2idx.get("PAD"))
      processed_sentences.append(np.array(processed_sentence))
    
    processed_sentences = pad_sequences(maxlen=self.max_line_size, 
                                        sequences=processed_sentences, 
                                        value=self.char2idx["PAD"], 
                                        padding='post', 
                                        truncating='post')
    return processed_sentences

  def predict(self,line):
    processed_line = self.transform_sentence(line)
    pred = self.model.predict(processed_line)
    return map(lambda p: 0 if p < 0.6 else 1, pred)

if __name__ == "__main__":
    identifier = IdentifyCommentedOutCode()
    predicts = identifier.predict(["this is probably a comment",
                                   "-------------- this section describe it ------------",
                                   "this.line = isCode(probably)"])
    for p in predicts:
      print(p)