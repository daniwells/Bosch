import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { MenuComponent } from '../menu/menu.component';

@Component({
  selector: 'app-main',
  standalone: true,
  imports: [CommonModule, MenuComponent],
  templateUrl: './main.component.html',
  styleUrl: './main.component.css'
})
export class MainComponent {
  products?: any = [{}]

  constructor(private router: Router) {
    this.getProducts();
  }

  getProducts(){
    fetch('https://dummyjson.com/products')
    .then(res => res.json())
    .then((data) => {
        console.log(data.products)
        this.products = data.products;
      }
    );  
  }
}
