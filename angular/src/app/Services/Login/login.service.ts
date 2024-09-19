import { inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { map } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class LoginService {

  // constructor(private http: HttpClient) {}
  private _http = inject(HttpClient)

  con = "https://dummyjson.com/auth/login"

  logar(username: string, password: string){
    return this._http.post(this.con, {
      username: username,
      password: password
    }).pipe(map((res: any) => {
      return {
        email: res.email,
        firstName: res.firstName,
        lastName: res.lastName,
        image: res.image,
      }
    }))
  }
}
