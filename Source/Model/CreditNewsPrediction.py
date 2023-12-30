import sys
import numpy as np
import tensorflow as tf
import json
from PIL import Image
from transformers import AutoTokenizer, TFMT5ForConditionalGeneration, TFPreTrainedModel, AutoImageProcessor, TFViTModel
from tensorflow import keras # type: ignore
from keras import losses, layers, callbacks, models
from pathlib import Path
from sklearn.utils import class_weight

ID_DATASET_PROCESSING = 13

class CreditNewsPrediction:
    def __init__(self):
        self.model = None

    def loadModelFromHuggingFace(self, modelTextName, modelImageName):
        self.tokenizer = AutoTokenizer.from_pretrained(modelTextName)
        self.modelMT5 : TFMT5ForConditionalGeneration = TFMT5ForConditionalGeneration.from_pretrained(modelTextName)
        self.imageProcessor = AutoImageProcessor.from_pretrained(modelImageName)
        self.modelViT : TFViTModel = TFViTModel.from_pretrained(modelImageName)

    def loadModelFromCheckpoint(self, modelCheckpointPath):
        self.model.load_weights(modelCheckpointPath)

    def preprocessTextFunction(self, text, max_length = 512):
        return self.tokenizer(text, padding = "max_length", truncation = True, max_length = max_length, return_tensors = "tf").data
    
    def preprocessImageFunction(self, image):
        return self.imageProcessor(image, return_tensors = "tf").data

    def _getImage(self, datasetFile: Path, index):
        return Image.open(datasetFile.parent / "Image" / f"{datasetFile.stem}_{index}.jpg")
    
    def _savePreprocessedData(self, idFile, fromIndex = 0, toIndex = -1):
        # Save to Numpy file
        np.savez(f"Dataset//Preprocessed_Multimodel//Common//X_train_{idFile}.npz", 
                 input_ids = self.X_train["input_ids"][fromIndex:toIndex], 
                 attention_mask = self.X_train["attention_mask"][fromIndex:toIndex],
                 labels = self.X_train["labels"][fromIndex:toIndex],
                 pixel_values = self.X_train["pixel_values"][fromIndex:toIndex])

    def _shuffleDataset(self):
        p = np.random.permutation(len(self.X_train["input_ids"]))
        self.X_train["input_ids"] = self.X_train["input_ids"][p]
        self.X_train["attention_mask"] = self.X_train["attention_mask"][p]
        self.X_train["pixel_values"] = self.X_train["pixel_values"][p]
        self.X_train["labels"] = self.X_train["labels"][p]

    def prepareData(self):
        self.X_train = {"input_ids": [], "attention_mask": [], "pixel_values": []}
        self.y_train = {"input_ids": []}
        listDatasetFile = [f"Dataset//Raw//VnExpress//data_{i}.json" for i in range(1, 14)]
        listDatasetFile.extend([f"Dataset//Raw//FakeVN//data_{i}.json" for i in range(1, 9)])

        for datasetFile in listDatasetFile:
            with open(datasetFile, "r", encoding = "utf-8") as f:
                dataset = json.load(f)
                for i, data in enumerate(dataset["dataset"]):
                    if i % 100 == 0:
                        print("Processing", datasetFile, i)
                    if data["content"] != None:
                        X = self.preprocessTextFunction(data["content"])
                        X_I = self.preprocessImageFunction( self._getImage( Path(datasetFile), i))
                        y = self.preprocessTextFunction( str(data["label"]), max_length = 2)
                        y["input_ids"] = np.where(y["input_ids"] == self.tokenizer.pad_token_id,
                                                   -100, y["input_ids"])
                        self.X_train["input_ids"].append(np.squeeze(X["input_ids"]))
                        self.X_train["attention_mask"].append(np.squeeze(X["attention_mask"]))
                        self.X_train["pixel_values"].append(np.squeeze(X_I["pixel_values"]))
                        self.y_train["input_ids"].append(np.squeeze(y["input_ids"]))

        # Convert to numpy array
        self.X_train["input_ids"] = np.array(self.X_train["input_ids"][0:])
        self.X_train["attention_mask"] = np.array(self.X_train["attention_mask"][0:])
        self.X_train["pixel_values"] = np.array(self.X_train["pixel_values"][0:])
        self.X_train["labels"] = np.array(self.y_train["input_ids"][0:])
        self._shuffleDataset()
        
        # Save to Numpy file. Each file has 500 samples
        for i in range(0, len(self.X_train["input_ids"]), 500):
            self._savePreprocessedData(i // 500, i, i + 500)

    def _loadPreprocessedData(self, idFile):
        data = np.load(f"Dataset//Preprocessed_Multimodel//Common//X_train_{idFile}.npz", allow_pickle = True)
        # Check size of data in MB
        print(sys.getsizeof(data) / 1024 / 1024)
        self.X_train = {"input_ids": data["input_ids"], "attention_mask": data["attention_mask"], "pixel_values": data["pixel_values"], "labels": data["labels"]}
     
    def createModel(self):
        testModel.loadModelFromHuggingFace("google/mt5-small",
                                         "google/vit-base-patch16-224")
        inputA = keras.Input(name="input_ids", shape=(512,), dtype="int32")
        inputB = keras.Input(name="attention_mask", shape=(512,), dtype="int32")
        inputC = keras.Input(name="labels", shape=(2,), dtype="int32")
        inputD = keras.Input(name="pixel_values", shape=(3, 224, 224), dtype="float32")
        outputMT5 = self.modelMT5(inputA, attention_mask = inputB, labels = inputC, training = True, return_dict = False)
        outputViT = self.modelViT(inputD, training = True, return_dict = False)
        pooledMT5 = layers.GlobalAveragePooling1D()(outputMT5[1])
        pooledViT = layers.GlobalAveragePooling1D()(outputViT[0])
        output = layers.Concatenate()([pooledMT5, pooledViT])
        output = layers.Dense(1, activation='sigmoid')(output)

        self.model : keras.Model = keras.Model(inputs=[inputA, inputB, inputC, inputD], outputs=output)
        self.model.compile(loss = losses.BinaryCrossentropy(), optimizer = "adam",
                           metrics = [metrics = [metrics.F1Score(average="macro")]])
        #keras.utils.plot_model(self.model, to_file='Source//Model//model.pdf', dpi=120, show_shapes=True, show_layer_names=True)

    def trainModel(self):
        self._loadPreprocessedData(ID_DATASET_PROCESSING)
        batchSize = 1
        epochs = 5

        self.y_train = np.array([int(self.tokenizer.decode(y, skip_special_tokens = True))
                     for y in self.X_train["labels"]])
        class_weights = class_weight.compute_class_weight(class_weight='balanced', classes=np.unique(self.y_train), y=self.y_train)
        class_weights = dict(enumerate(class_weights))
        
        callback = callbacks.EarlyStopping(patience=1, monitor='val_accuracy')
        checkpoint = callbacks.ModelCheckpoint("/content/drive/MyDrive/Model/CredibilityPrediction/model.weights.h5",
                               monitor='val_accuracy', verbose=1, save_best_only=True, mode='max',
                               save_weights_only=True)

        self.model.fit(x = [self.X_train["input_ids"], self.X_train["attention_mask"],
                       self.X_train["labels"], self.X_train["pixel_values"]],
                       y = self.y_train, batch_size = batchSize, epochs = epochs,
                       callbacks = [callback, checkpoint], validation_split = 0.2,
                       class_weight = class_weights)
        

if __name__ == "__main__":
    testModel = CreditNewsPrediction()
    testModel.loadModelFromHuggingFace("google/mt5-small", "google/vit-base-patch16-224")
    testModel.trainModel()

