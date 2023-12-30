import numpy as np
import tensorflow as tf
import json
from transformers import AutoTokenizer, TFMT5ForConditionalGeneration, TFPreTrainedModel
from tensorflow import keras # type: ignore
from keras import losses, layers, callbacks

ID_DATASET_PROCESSING = 13

class TopicClassify:
    def __init__(self):
        self.id2lable = {
            "0": "Thời sự",
            "1": "Thế giới",
            "2": "Kinh tế",
            "3": "Bất động sản",
            "4": "Khoa học",
            "5": "Giải trí",
            "6": "Thể thao",
            "7": "Pháp luật",
            "8": "Giáo dục",
            "9": "Sức khỏe",
            "10": "Đời sống",
            "11": "Du lịch",
            "12": "Công nghệ"
        }

        self.label2id = {
            "Thời sự": "0",
            "Thế giới": "1",
            "Kinh tế": "2",
            "Bất động sản": "3",
            "Khoa học": "4",
            "Giải trí": "5",
            "Thể thao": "6",
            "Pháp luật": "7",
            "Giáo dục": "8",
            "Sức khỏe": "9",
            "Đời sống": "10",
            "Du lịch": "11",
            "Công nghệ": "12"
        }

    def loadModelFromHuggingFace(self, modelName):
        self.tokenizer = AutoTokenizer.from_pretrained(modelName)
        self.model : TFMT5ForConditionalGeneration = TFMT5ForConditionalGeneration.from_pretrained(modelName)

    def loadModelFromCheckpoint(self, checkpointPath):
        self.model : TFMT5ForConditionalGeneration = TFMT5ForConditionalGeneration.from_pretrained(checkpointPath)

    def preprocessFunction(self, text, max_length = 512):
        return self.tokenizer(text, padding = "max_length", truncation = True, max_length = max_length, return_tensors = "tf").data
    
    def _savePreprocessedData(self, idFile, fromIndex = 0, toIndex = -1):
        # Save to Numpy file
        np.savez(f"Dataset//Preprocessed//VnExpress//X_train_{idFile}.npz", 
                 input_ids = self.X_train["input_ids"][fromIndex:toIndex], 
                 attention_mask = self.X_train["attention_mask"][fromIndex:toIndex],
                 labels = self.X_train["labels"][fromIndex:toIndex])
        data = np.load(f"Dataset//Preprocessed//VnExpress//X_train_{idFile}.npz", allow_pickle = True)
        print(data["labels"])

    def prepareData(self):
        self.X_train = {"input_ids": [], "attention_mask": []}
        self.y_train = {"input_ids": []}
        listDatasetFile = [f"Dataset//Raw//VnExpress//data_{i}.json" for i in range(1, 14)]

        for datasetFile in listDatasetFile:
            with open(datasetFile, "r", encoding = "utf-8") as f:
                dataset = json.load(f)
                for i, data in enumerate(dataset["dataset"]):
                    if i % 100 == 0:
                        print("Processed: ", i)
                    if data["content"] != None:
                        X = self.preprocessFunction(data["content"])
                        y = self.preprocessFunction( self.label2id[data["topic"][0]], max_length = 2)
                        y["input_ids"] = np.where(y["input_ids"] == self.tokenizer.pad_token_id,
                                                   -100, y["input_ids"])
                        self.X_train["input_ids"].append(np.squeeze(X["input_ids"]))
                        self.X_train["attention_mask"].append(np.squeeze(X["attention_mask"]))
                        self.y_train["input_ids"].append(np.squeeze(y["input_ids"]))

        print("X_train: ", len(self.X_train["input_ids"]))
        print("y_train: ", len(self.y_train["input_ids"]))

        # Convert to numpy array
        self.X_train["input_ids"] = np.array(self.X_train["input_ids"][0:])
        self.X_train["attention_mask"] = np.array(self.X_train["attention_mask"][0:])
        self.X_train["labels"] = np.array(self.y_train["input_ids"][0:])

        # Shuffle all the dataset
        p = np.random.permutation(len(self.X_train["input_ids"]))
        self.X_train["input_ids"] = self.X_train["input_ids"][p]
        self.X_train["attention_mask"] = self.X_train["attention_mask"][p]
        self.X_train["labels"] = self.X_train["labels"][p]

        # Save to Numpy file. Each file has 500 samples
        for i in range(0, len(self.X_train["input_ids"]), 500):
            self._savePreprocessedData(i // 500, i, i + 500)

    def _loadPreprocessedData(self, idFile):
        data = np.load(f"Dataset//Preprocessed//VnExpress//X_train_{idFile}.npz", allow_pickle = True)
        self.X_train = {"input_ids": data["input_ids"], "attention_mask": data["attention_mask"],
                        "labels": data["labels"]}
     
    def trainModel(self):
        self._loadPreprocessedData(ID_DATASET_PROCESSING)
        batchSize = 1
        epochs = 5

        '''
        Input layout:
            input_ids has shape (batch_size, sequence_length)
            attention_mask has shape (batch_size, sequence_length)
            labels has shape (batch_size, sequence_length_of_labels)
        Output layout (logits):
            logits has shape (batch_size, sequence_length_of_labels, config.vocab_size)
        '''
        callback = callbacks.EarlyStopping()
        self.model.compile(
            optimizer = keras.optimizers.AdamW(learning_rate = 1e-4)
        )
        history = self.model.fit(
            x = self.X_train,
            batch_size = batchSize,
            epochs = epochs,
            callbacks = [callback],
            validation_split = 0.2
        )

        TFPreTrainedModel.save_pretrained(self.model, "Model//TopicClassify//")
        

if __name__ == "__main__":
    testModel = TopicClassify()
    testModel.loadModelFromHuggingFace("google/mt5-small")
    testModel.prepareData()

