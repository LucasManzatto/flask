import { async, ComponentFixture, TestBed, fakeAsync } from '@angular/core/testing';

import { BookAddComponent } from './book-add.component';
import { AppRoutingModule } from 'src/app/app-routing.module';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { BrowserModule } from '@angular/platform-browser';
import { ScrollingModule } from '@angular/cdk/scrolling';
import { HttpClientModule, HttpClient } from '@angular/common/http';
import { SharedModule } from 'src/app/shared/shared.module';
import { FlexLayoutModule } from '@angular/flex-layout';
import { FormsModule, ReactiveFormsModule, FormBuilder } from '@angular/forms';
import { BookService } from '../../../shared/services/book.service';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { tick } from '@angular/core/src/render3';
import { defer, Observable, of } from 'rxjs';
import { AuthorService, AuthorServiceStub } from '../../../shared/services/author.service';
import { Query } from '../../../shared/models/query.model';
import { SeriesService } from 'src/app/shared/services/series.service';
import { Author } from '../../../shared/models/author.model';
import { createQuery, asyncData } from '../../../shared/utils';



fdescribe('BookAddComponent', () => {
  let component: BookAddComponent;
  let fixture: ComponentFixture<BookAddComponent>;
  let service: BookService;
  let authorService: AuthorService;
  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [AppRoutingModule,
        BrowserAnimationsModule,
        BrowserModule,
        ScrollingModule,
        HttpClientModule,
        SharedModule,
        FlexLayoutModule,
        FormsModule,
        ReactiveFormsModule],
      declarations: [BookAddComponent]
    }).overrideComponent(BookAddComponent, {
      set: {
        providers: [
          { provide: AuthorService, useClass: AuthorServiceStub },
        ]
      }
    }).compileComponents();
  }));

  describe('unit tests', () => {
    beforeEach(() => {
      TestBed.configureTestingModule({
        providers: [BookService, { provide: AuthorService, useClass: AuthorServiceStub },
        ],
        imports: [HttpClientTestingModule]
      });

      service = TestBed.get(BookService);
      fixture = TestBed.createComponent(BookAddComponent);
      authorService = fixture.debugElement.injector.get(AuthorService);
      component = fixture.componentInstance;
      fixture.detectChanges();
    });
    fit('should create', () => {
      expect(component).toBeTruthy();
    });

    fdescribe('ngOnInit()', () => {
      beforeEach(() => {
      });
      fit('should initialize form', () => {
        spyOn(component, 'initForm');
        component.ngOnInit();
        expect(component.initForm).toHaveBeenCalled();
      });
      fit('should initialize book', () => {
        spyOn(component, 'initBook');
        component.ngOnInit();
        expect(component.initBook).toHaveBeenCalled();
      });

      fit('should call getAuthors() and initialize authors array', () => {
        spyOn(authorService, 'getAll').and.callThrough();
        component.ngOnInit();
        fixture.whenStable().then(() => {
          expect(component.authors).toEqual(authorService.authorsArrayMock);
          expect(authorService.getAll).toHaveBeenCalled();
        });
      });

      fit('should set the book the same as the service book if is editing', () => {
        service.currentItem = { title: 'Test', author: { name: 'Test Author' } };
        service.editing = true;
        component.ngOnInit();
        expect(component.book).toEqual(service.currentItem);
      });
    });

    fit('should change filteredAuthors when form changes', () => {
      spyOn(authorService, 'getAll').and.callThrough();
      component.ngOnInit();
      fixture.whenStable().then(() => {
        component.form.patchValue({ author: 'Author 2' });
        component.filteredAuthors.subscribe(res => {
          console.log(res);
        })
      });
    });

    describe('getSeries()', () => {
      fit('should populate the series array', () => {
        spyOn(authorService, 'getSeries').and.callThrough();
        component.getSeries(1);
        fixture.whenStable().then(() => {
          expect(component.series).toEqual(authorService.seriesArrayMock);
          expect(authorService.getSeries).toHaveBeenCalled();
        });
      });
    });

  });

});
