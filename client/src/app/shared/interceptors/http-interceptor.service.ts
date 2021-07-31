import { HttpEvent, HttpHandler, HttpInterceptor, HttpRequest } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable } from "rxjs";

import { environment } from "src/environments/environment";

@Injectable({
    providedIn: "root",
})
export class ApiInterceptor implements HttpInterceptor {
  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const url = environment.apiUri;
    if (req.url.startsWith('/api') || req.url.startsWith('/media')){
        req = req.clone({
            url: url + req.url
        });
    }
    return next.handle(req);
  }
}