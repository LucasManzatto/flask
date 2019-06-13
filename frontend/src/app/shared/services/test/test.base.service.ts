import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BaseService } from '../base.service';
import { Test } from '../../models/application/test.model';
import { GlobalService } from '../global.service';

@Injectable({
  providedIn: 'root',
})

export class TestService extends BaseService<Test, Test> {

  constructor(http: HttpClient, globalService: GlobalService) {
    super(http, 'test', globalService);
  }
}
