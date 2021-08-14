import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { AuthService } from './auth.service';
import { NgForm } from '@angular/forms';

@Component({
  selector: 'app-auth',
  templateUrl: './auth.component.html',
  styleUrls: ['./auth.component.css']
})
export class AuthComponent implements OnInit {

    loading = false;
    signInMode = true;
    
    signInError: string|null = null
    signUpError: string|null = null;

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
        this.loading = true
        this.authService.signin(
            form.value.email,
            form.value.password,
        ).subscribe(
            data => {
                this.signInError = null
                console.log(data)
                this.loading = false
            },
            error => {
                this.signInError = error.error.error
                this.loading = false
            }
        )
    }

    onSignUp(form: NgForm){
        this.loading = true
        const password = form.value.password
        const passwordConfirmation = form.value.passwordConfirmation
        if (password !== passwordConfirmation){
            this.signUpError = "WRONG_PASSWORD_CONFIRMATION_ERROR"
            this.loading = false
            return
        }
        this.authService.signup(
            form.value.email,
            form.value.firstName,
            form.value.secondName,
            form.value.password
        ).subscribe(
            data => {
                this.signUpError = null
                console.log(data)
                this.loading = false
            },
            error => {
                this.signUpError = error.error.error
                this.loading = false
            },
        )
    }

}
