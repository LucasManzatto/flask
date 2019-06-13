import { Injectable } from '@angular/core';
import { HttpEvent, HttpRequest, HttpResponse, HttpInterceptor, HttpHandler } from '@angular/common/http';

import { Observable } from 'rxjs';
import { of } from 'rxjs';
import { startWith, tap } from 'rxjs/operators';
import { RequestCache } from './request.cache';
import { GlobalService } from './services/global.service';


@Injectable()
export class CachingInterceptor implements HttpInterceptor {
    cache: RequestCache;
    constructor(public globalService: GlobalService) {
        this.cache = new RequestCache();
    }
    intercept(req: HttpRequest<any>, next: HttpHandler) {
        const cachedResponse = this.cache.get(req);
        // Manda a requisição novamente para qualquer método que nao seja o GET, se não houver a resposta em cache
        // ou se está criando ou editando uma tabela.
        if (req.method !== 'GET' || !cachedResponse || this.globalService.reloadData) {
            return this.sendRequest(req, next, this.cache);
        } else {
            return of(cachedResponse);
        }
    }

    sendRequest(
        req: HttpRequest<any>,
        next: HttpHandler,
        cache: RequestCache): Observable<HttpEvent<any>> {
        return next.handle(req).pipe(
            tap(event => {
                if (event instanceof HttpResponse) {
                    cache.put(req, event);
                }
            })
        );
    }
}
