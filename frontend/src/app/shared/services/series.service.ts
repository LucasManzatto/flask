import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BaseService } from './base.service';
import { Series, SeriesDTO } from '../models/backend/series.model';
import { GlobalService } from './global.service';

@Injectable({
  providedIn: 'root',
})
export class SeriesService extends BaseService<Series, SeriesDTO> {

  constructor(http: HttpClient, globalService: GlobalService) {
    super(http, 'series', globalService);
  }
}
