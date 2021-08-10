import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { AuthService } from './auth.service';
import { NgForm } from '@angular/forms';
import { catchError, tap } from 'rxjs/operators';

@Component({
  selector: 'app-auth',
  templateUrl: './auth.component.html',
  styleUrls: ['./auth.component.css']
})
export class AuthComponent implements OnInit {

    loading = false;
    signInMode = true;

    constructor(private authService: AuthService,
                private route: ActivatedRoute) { }

    ngOnInit(): void {
        this.route.url.subscribe(
            segments => {
                const url = segments.join('')
                this.signInMode = url == "login" ? true : false
            }
        )
    }

    onSignIn(form: NgForm){
        this.authService.signin(
            form.value.email,
            form.value.password,
        ).subscribe(
            data => {
                
            }
        )
    }

    onSignUp(form: NgForm){
        const password = form.value.password
        const passwordConfirmation = form.value.passwordConfirmation
        if (password !== passwordConfirmation){
            console.log("LOX")
            return
        }
        this.authService.signup(
            form.value.email,
            form.value.firstName,
            form.value.secondName,
            form.value.password
        ).subscribe(
            data => {

            }
        )
    }

}
