import { Routes } from '@angular/router';
import { HomeComponent } from './Component/home/home.component';
import { MainComponent } from './Component/main/main.component';

export const routes: Routes = [
    {
        path:"",
        component: HomeComponent
    },
    {
        path: "main",
        component: MainComponent
    }
];
