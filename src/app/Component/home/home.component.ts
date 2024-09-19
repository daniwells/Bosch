import { Component, inject } from '@angular/core';
import { FooterComponent } from '../footer/footer.component';
import { FormBuilder, Validators } from '@angular/forms';
import { LoginService } from '../../Services/Login/login.service';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import { LoginResponse } from '../../Interfaces/login-response';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [FooterComponent, FormsModule, ReactiveFormsModule, CommonModule],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent {
  _fb = inject(FormBuilder)
  loginService = inject(LoginService)
  resposta?: LoginResponse
  error: string | null = null
  
  constructor(private router: Router) {}
  
  form = this._fb.group({
    username: ["", Validators.required],
    password: ["", Validators.required]
  })

  logar(){
    this.loginService.logar(
      this.form.controls.username.value!, 
      this.form.controls.password.value!
    ).subscribe({
      next: (val: LoginResponse) => {
        this.resposta = val 

        if (val) { 
          this.router.navigate(['/main']);
        }
        
      },
      error: (err) => {
        this.error = "Incorrect email or password!";
      }
    })
  }
}
