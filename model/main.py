import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import requests
import torch
from transformers import Owlv2Processor, Owlv2ForObjectDetection
import pandas as pd
import json



def get_ingredients(image, threshold=0.25, ingredients_list_path="ingredients_list.json"):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    # device = "cpu"
    print("device is ", device) 
    with open("ingredients_list.json", "r") as file:
        ingredients_list = json.load(file)
    processor = Owlv2Processor.from_pretrained("google/owlv2-base-patch16-ensemble")
    model = Owlv2ForObjectDetection.from_pretrained("google/owlv2-base-patch16-ensemble").to(device)
    # model = torch.compile(model, mode="reduce-overhead")
    # image = Image.open(requests.get(url, stream=True).raw)
    image = image.resize((672, 672))
    texts = [[f"a photo of {ingredient}" for ingredient in ingredients_list]]
    inputs = processor(text=texts, images=image,return_tensors="pt").to(device)
    with torch.no_grad(), torch.cuda.amp.autocast():
        outputs = model(**inputs)
    target_sizes = torch.Tensor([image.size[::-1]]).to(device)
    results = processor.post_process_grounded_object_detection(
        outputs=outputs,
        target_sizes=target_sizes,
        threshold=threshold,
        text_labels=texts
    )
    clean_list = set()
    for result in results:
        for box, score, label in zip(result["boxes"], result["scores"], result["text_labels"]):
            clean_label = label.replace("a photo of ", "").strip()
            confidence = round(score.item(), 3)
            
            # Convert box coordinates to integers
            box = [int(coord) for coord in box.tolist()]
            # Create a Rectangle patch
            clean_list.add(clean_label)
    return list(clean_list)

def plot_image(results, image):
    clean_list = set()
    fig, ax = plt.subplots(1, figsize=(16, 12))
    ax.imshow(image)

    # Process and visualize results
    for result in results:
        for box, score, label in zip(result["boxes"], result["scores"], result["text_labels"]):
            clean_label = label.replace("a photo of ", "").strip()
            confidence = round(score.item(), 3)
            
            # Convert box coordinates to integers
            box = [int(coord) for coord in box.tolist()]
            if (confidence < 0.2):
                continue
            # Create a Rectangle patch
            clean_list.add(clean_label)
            rect = patches.Rectangle((box[0], box[1]), box[2] - box[0], box[3] - box[1],
                                    linewidth=2, edgecolor='r', facecolor='none')
            
            # Add the patch to the Axes
            ax.add_patch(rect)
            
            # Add label and confidence score
            ax.text(box[0], box[1] - 5, f'{clean_label}: {confidence:.2f}',
                    color='red', fontweight='bold', backgroundcolor='white')

            print(f"Detected: {clean_label}, Confidence: {confidence:.2f}, Box: {box}")

        plt.axis('off')
        plt.tight_layout()
        plt.show()

# print(get_ingredients(image = Image.open(requests.get(url, stream=True).raw)))
