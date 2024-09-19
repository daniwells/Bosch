from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings
import torch
import torchvision.transforms as transforms
from PIL import Image
import os
import torchvision


def load_model(model_path):
    model = torchvision.models.resnet18(weights=torchvision.models.ResNet18_Weights.IMAGENET1K_V1)
    num_features = model.fc.in_features
    model.fc = torch.nn.Linear(num_features, 6)  # 38 classes do PlantVillage, ajuste conforme necessário
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    model.eval()  # Coloca o modelo em modo de avaliação
    return model


def preprocess_image(image):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    image = Image.open(image).convert('RGB')
    return transform(image).unsqueeze(0)

model = load_model(os.path.join(settings.BASE_DIR, 'modelo_plantvillage.pth'))


@csrf_exempt
def home(request):
    if request.method == "POST":
        plant_file = request.FILES.get("plant")
        if plant_file:
            print(f'IMAGEMMMM: {plant_file}')
            print(f'IMAGEMMMM NAMMEEEE: {plant_file.name}')
            return post_plant_classify(request, plant_file)
        return render(request, 'homepage.html', {"status":"Imagem não encontrada!"})
    return render(request, 'homepage.html')


def post_plant_classify(request, image_file):
    if not image_file:
        return JsonResponse({'error': 'No image uploaded'}, status=400)

    processed_image = preprocess_image(image_file)

    with torch.no_grad():
        outputs = model(processed_image)
        _, predicted = torch.max(outputs, 1)

    class_idx = predicted.item()
    print(class_idx)

    class_names = [
        'Pepper Bell Bacterial','Pepper Bell Healthy','Potato Early Blight', 
        'Potato Late Blight','Tomato Bacterial Spot','Potato Healthy',
    ]

    class_name = class_names[class_idx]

    file_path = os.path.join(settings.MEDIA_ROOT, 'images', image_file.name)

    with open(file_path, 'wb+') as media:
        for chunk in image_file.chunks():
            media.write(chunk)

    if os.path.exists(file_path):
        print(settings.MEDIA_URL)
        return render(request, 'homepage.html', {
            "image":{"class":class_name, 
            "src":image_file.name
        }})



        