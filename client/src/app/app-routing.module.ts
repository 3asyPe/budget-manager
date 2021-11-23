import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthComponent } from './auth/auth.component';
import { HomeComponent } from './home/home.component';


const routes: Routes = [
    { path: "login", component: AuthComponent, pathMatch: "full" },
    { path: "registration", component: AuthComponent, pathMatch: "full" },
    { path: "home", component: HomeComponent, pathMatch: "full" },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
