import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { BookAddComponent } from './book-add.component';
import { AppRoutingModule } from 'src/app/app-routing.module';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { BrowserModule } from '@angular/platform-browser';
import { ScrollingModule } from '@angular/cdk/scrolling';
import { HttpClientModule } from '@angular/common/http';
import { SharedModule } from 'src/app/shared/shared.module';
import { FlexLayoutModule } from '@angular/flex-layout';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { BookService } from '../../../shared/services/book.service';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { AuthorService, AuthorServiceStub } from '../../../shared/services/author.service';
import { MatDialogRef } from '@angular/material/dialog';



describe('BookAddComponent', () => {
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
      declarations: [BookAddComponent],
      providers: [
        BookService,
        {
          provide: MatDialogRef, useValue: {
            close: () => { }
          }
        }
      ]
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
      service = TestBed.get(BookService);
      fixture = TestBed.createComponent(BookAddComponent);
      authorService = fixture.debugElement.injector.get(AuthorService);
      component = fixture.componentInstance;
      fixture.detectChanges();
    });
    it('should create', () => {
      expect(component).toBeTruthy();
    });

    describe('ngOnInit()', () => {
      beforeEach(() => {
      });
      it('should initialize form', () => {
        spyOn(component, 'initForm');
        component.ngOnInit();
        expect(component.initForm).toHaveBeenCalled();
      });
      it('should initialize book', () => {
        spyOn(component, 'initBook');
        component.ngOnInit();
        expect(component.initBook).toHaveBeenCalled();
      });

      it('should call getAuthors() and initialize authors array', () => {
        spyOn(authorService, 'getAll').and.callThrough();
        component.ngOnInit();
        fixture.whenStable().then(() => {
          expect(component.authors).toEqual(authorService.authorsArrayMock);
          expect(authorService.getAll).toHaveBeenCalled();
        });
      });

      it('should set the book the same as the service book if is editing', () => {
        service.currentItem = { title: 'Test', author: { name: 'Test Author' } };
        service.editing = true;
        component.ngOnInit();
        expect(component.book).toEqual(service.currentItem);
      });
    });

    describe('form', () => {
      describe('on author change', () => {
        let mock;
        beforeAll(() => {
          component.authors = authorService.authorsArrayMock;
          mock = { author: component.authors[0] };
        });
        describe('valid input', () => {
          afterEach(() => {
            fixture.whenStable().then(() => {
              component.filteredAuthors.subscribe(res => {
                const foundAuthor = res.find(item => item.name === mock.author.name);
                expect(foundAuthor).toBeDefined();
                expect(res.length).toBeLessThan(component.authors.length);
              });
            });
          });
          it('should change filteredAuthors with a string input', () => {
            component.form.patchValue({ author: mock.author.name });
          });
          it('should change filteredAuthors with an object input', () => {
            component.form.patchValue(mock);
          });
        });
        describe('invalid input', () => {
          afterEach(() => {
            fixture.whenStable().then(() => {
              component.filteredAuthors.subscribe(res => {
                const foundAuthor = res.find(item => item.name === mock.author.name);
                expect(foundAuthor).toBeUndefined();
                expect(res.length).toBe(0);
              });
            });
          });
          it('should change filteredAuthors with a string input', () => {
            component.form.patchValue({ author: 'ShouldNotExist' });
          });
          it('should change filteredAuthors with an object input', () => {
            component.form.patchValue({ author: { name: 'ShouldNotExist' } });
          });
        });
      });

      describe('on series change', () => {
        let mock;
        beforeEach(() => {
          spyOn(authorService, 'getSeries').and.callThrough();
          component.series = authorService.seriesArrayMock;
          mock = { series: component.series[0] };
          component.getSeries(component.series[0].id);
        });
        describe('valid input', () => {
          afterEach(() => {
            fixture.whenStable().then(() => {
              component.filteredSeries.subscribe(res => {
                const foundSeries = res.find(item => item.title === mock.series.title);
                expect(foundSeries).toBeDefined();
                expect(res.length).toBeLessThan(component.series.length);
              });
            });
          });
          it('should change filteredSeries with a string input', () => {
            component.form.patchValue({ series: mock.series.title });
          });
          it('should change filteredSeries with an object input', () => {
            component.form.patchValue(mock);
          });
        });
        describe('invalid input', () => {
          afterEach(() => {
            fixture.whenStable().then(() => {
              component.filteredSeries.subscribe(res => {
                const foundSeries = res.find(item => item.title === mock.series.title);
                expect(foundSeries).toBeUndefined();
                expect(res.length).toBe(0);
              });
            });
          });
          it('should change filteredSeries with a string input', () => {
            component.form.patchValue({ series: 'ShouldNotExist' });
          });
          it('should change filteredSeries with an object input', () => {
            component.form.patchValue({ series: { title: 'ShouldNotExist' } });
          });
        });
      });
    });

    describe('getSeries()', () => {
      it('should populate the series array', () => {
        spyOn(authorService, 'getSeries').and.callThrough();
        component.getSeries(1);
        fixture.whenStable().then(() => {
          expect(component.series).toEqual(authorService.seriesArrayMock);
          expect(authorService.getSeries).toHaveBeenCalled();
        });
      });
    });

    describe('authorSelected()', () => {
      it('should call getSeries()', () => {
        spyOn(component, 'getSeries');
        component.authorSelected(authorService.authorsArrayMock[0]);
        expect(component.getSeries).toHaveBeenCalled();
      });
    });

    describe('addBook()', () => {
      beforeEach(() => {
        // spyOn(component, 'addBook');
      });
      it('should assign form values to book object', () => {
        const mockFormData = { title: 'Test', author: { name: 'Test Author' }, series: { title: 'Test Series' } };
        component.form.setValue(mockFormData);
        component.addBook();
        fixture.whenStable().then(() => {
          expect(component.book).toEqual(mockFormData);
        });
      });
      it('should close the dialog', () => {
        spyOn(component.dialogRef, 'close');
        component.addBook();
        expect(component.dialogRef.close).toHaveBeenCalled();
      });
    });

  });

});
