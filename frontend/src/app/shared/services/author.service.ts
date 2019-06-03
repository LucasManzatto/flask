import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BaseService } from './base.service';
import { Author } from '../models/author.model';
import { Observable } from 'rxjs';
import { Series } from '../models/series.model';

@Injectable({
  providedIn: 'root',
})
export class AuthorService extends BaseService<Author> {

  constructor(http: HttpClient) {
    super(http, 'authors');
  }

  getSeries(id: number): Observable<Series[]> {
    return this.http.get<Series[]>(`${this.baseUrl}${id}/series`);
  }
}
