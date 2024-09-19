from fastapi import FastAPI, File, UploadFile
from PIL import Image
import io

app = FastAPI()

# Carregar o modelo treinado
model = torchvision.models.resnet18(pretrained=False)
num_features = model.fc.in_features
model.fc = nn.Linear(num_features, len(train_dataset.classes))  # Número de classes do PlantVillage
model.load_state_dict(torch.load('modelo_apple_scab.pth'))
model.eval()

# Definir as transformações de imagem
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    image = Image.open(io.BytesIO(await file.read()))
    image = transform(image).unsqueeze(0)  # Adiciona uma dimensão para o batch

    with torch.no_grad():
        outputs = model(image)
        _, predicted = torch.max(outputs, 1)
        class_idx = predicted.item()

    class_name = train_dataset.classes[class_idx]
    return {"class": class_name}