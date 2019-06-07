import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BaseService } from './base.service';
import { Series, SeriesDTO } from '../models/series.model';

@Injectable({
  providedIn: 'root',
})
export class SeriesService extends BaseService<Series, SeriesDTO> {

  constructor(http: HttpClient) {
    super(http, 'series');
  }
}
