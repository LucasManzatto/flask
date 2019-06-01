import { TestBed } from '@angular/core/testing';
import { BookService } from './book.service';
import {
    HttpClientTestingModule,
    HttpTestingController
} from '@angular/common/http/testing';
import { DefaultQuery } from 'src/app/shared/models/query.model';
import { Book } from '../../shared/models/book.model';
import { Author } from '../../shared/models/author.model';
import { HttpRequest } from '@angular/common/http';
import { isEqual, sortBy } from 'lodash';
import { Query } from '../../shared/models/query.model';

describe('BookService', () => {
    // We declare the variables that we'll use for the Test Controller and for our Service
    let backend: HttpTestingController;
    let service: BookService;

    const defaultParams = ['page', 'direction', 'sort_column', 'query_all'];
    const defaultQuery: DefaultQuery = {
        direction: 'ASC',
        page: '1',
        per_page : '10',
        query_all: '',
        sort_column: 'id'
    };
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
            providers: [BookService],
            imports: [HttpClientTestingModule]
        });

        // We inject our service (which imports the HttpClient) and the Test Controller
        backend = TestBed.get(HttpTestingController);
        service = TestBed.get(BookService);
    });

    afterEach(() => {
        backend.verify();
    });

    it('should be created', () => {
        expect(service).toBeTruthy();
    });
    it('returned Observable should match the right data', () => {
        const params = sortBy(['id', 'title', 'author_name'].concat(defaultParams));
        service.getAll(defaultQuery).subscribe(res => {
            expect(res.page).toEqual(query.page);
            expect(res.total).toBe(query.total);
            expect(res.items).toEqual(items);
        });

        backend.match((request: HttpRequest<any>) => {
            return request.url === service.getAllBooksUrl &&
                request.method === 'GET' &&
                isEqual(sortBy(request.params.keys()), params) &&
                request.params.get('direction') === defaultQuery.direction &&
                request.params.get('page') === defaultQuery.page &&
                request.params.get('sort_column') === defaultQuery.sort_column &&
                request.params.get('query_all') === defaultQuery.query_all &&
                request.responseType === 'json';
        })[0].flush(query);
    });

    it('should match when no parameters are passed on getAll()', () => {
        const params = sortBy(['id', 'title', 'author_name'].concat(defaultParams));
        service.getAll().subscribe(res => {
            expect(res.page).toEqual(1);
            expect(res.total).toBe(2);
            expect(res.items).toEqual(items);
        });
        backend.match(request => {
            return request.url === service.getAllBooksUrl &&
                request.method === 'GET' &&
                isEqual(sortBy(request.params.keys()), params);
        })[0].flush(query);
    });

    it('should return book from getBook()', () => {
        const book = items[0];
        service.getBook(book.id).subscribe(res => {
            expect(res).toEqual(book);
        });
        backend.expectOne(`${service.booksUrl}/${book.id}`).flush(book);
    });

    it('should return not found from getBook()', () => {
        service.getBook(-1).subscribe();
        backend.expectOne(`${service.booksUrl}/-1`);
    });
});
