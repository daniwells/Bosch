import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader

import os

def main():
    print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
    # Diretório onde o dataset foi extraído
    data_dir = './PlantVillage'

    # Transformações de dados (normalização, aumento de dados, etc.)
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    # Carregando o dataset PlantVillage
    train_dataset = ImageFolder(os.path.join(data_dir, 'train'), transform=transform)
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True, num_workers=4)

    test_dataset = ImageFolder(os.path.join(data_dir, 'test'), transform=transform)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False, num_workers=4)

    # Definindo a rede neural (usaremos uma versão pré-treinada da ResNet)
    # Atualize a linha abaixo para usar o parâmetro 'weights'
    model = torchvision.models.resnet18(weights=torchvision.models.ResNet18_Weights.IMAGENET1K_V1)
    num_features = model.fc.in_features
    model.fc = nn.Linear(num_features, len(train_dataset.classes))  # Ajustando para o número de classes do PlantVillage

    # Função de perda e otimizador
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    print("Modelo em treinamento")
    # Treinamento da rede
    num_epochs = 10
    for epoch in range(num_epochs):
        print(f"Treinando {epoch}")
        model.train()
        running_loss = 0.0
        for inputs, labels in train_loader:
            print(f"Treinando {labels}")
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()

        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {running_loss/len(train_loader):.4f}')

    torch.save(model.state_dict(), 'modelo_plantvillage.pth')
    print("Modelo em avaliação")
    # Avaliação do modelo
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for inputs, labels in test_loader:
            outputs = model(inputs)
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    print(f'Accuracy on test set: {100 * correct / total:.2f}%')

if __name__ == "__main__":
    main()
