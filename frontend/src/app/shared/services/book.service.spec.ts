import { TestBed } from '@angular/core/testing';
import { BookService, BookServiceStub } from './book.service';
import {
  HttpClientTestingModule,
  HttpTestingController
} from '@angular/common/http/testing';
import { Book } from '../models/book.model';
import { HttpRequest } from '@angular/common/http';
import { isEqual, sortBy } from 'lodash';
import { Query } from '../models/query.model';
import { DEFAULT_PARAMETERS_KEYS, DEFAULT_PARAMETERS } from '../parameters';

describe('BookService', () => {
  // We declare the variables that we'll use for the Test Controller and for our Service
  let backend: HttpTestingController;
  let service: BookService;
  let serviceStub: BookServiceStub;

  const defaultParams = DEFAULT_PARAMETERS;
  const defaultParamKeys = DEFAULT_PARAMETERS_KEYS;
  const bookQueryParamKeys = ['id', 'title', 'author_name'];
  const bookQuery = {
    'id': '',
    'title': '',
    'author_name': ''
  };
  const allQueryParams = sortBy(bookQueryParamKeys.concat(defaultParamKeys));
  const defaultQuery = DEFAULT_PARAMETERS;
  const items: Book[] = [{
    id: 1,
    title: 'Test 1',
    author: {
      name: 'Author 1'
    }
  },
  {
    id: 2,
    title: 'Test 2',
    author: {
      name: 'Author 2'
    }
  }];
  const query: Query = {
    items,
    page: 1,
    per_page: 10,
    total: items.length
  };

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [BookService, BookServiceStub],
      imports: [HttpClientTestingModule]
    });
    // We inject our service (which imports the HttpClient) and the Test Controller
    backend = TestBed.get(HttpTestingController);
    service = TestBed.get(BookService);
    serviceStub = TestBed.get(BookServiceStub);
  });

  afterEach(() => {
    backend.verify();
  });


  describe('BookServiceStub', () => {
    it('should getAll()', () => {
      serviceStub.getAll().subscribe(res => {
        expect(res.items).toEqual(service.booksArrayMock);
      });
      backend.expectNone(service.baseUrl);
    });
    it('should getAllWithParameters()', () => {
      serviceStub.getAllWithParameters().subscribe(res => {
        expect(res.items).toEqual(service.booksArrayMock);
      });
    });
  });

});
