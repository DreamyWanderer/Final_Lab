import json
import requests
from PIL import Image
from io import BytesIO
from pathlib import Path

pathDataset = Path("Dataset//Raw//FakeVN")

if __name__ == "__main__":

    for i in range(5, 9):
        datasetFile = pathDataset / f"data_{i}.json"
        print("Processing", datasetFile)
        with open(datasetFile, "r", encoding = "utf-8") as f:
            data = json.load(f)["dataset"]
        for i in range(len(data)):
            imageURL = data[i]["imageURL"]
            image = None
            if imageURL == None:
                image = Image.new("RGB", (224, 224), (0, 0, 0))
            else:
                try:
                    response = requests.get(imageURL)
                    image = Image.open(BytesIO(response.content))
                    image = image.convert("RGB")
                except:
                    image = Image.new("RGB", (224, 224), (0, 0, 0))

            image.save(datasetFile.parent / "Image" / f"{datasetFile.stem}_{i}.jpg")