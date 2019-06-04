import { Component, OnInit } from '@angular/core';
import { BookService } from '../../../shared/services/book.service';
import { Book } from '../../../shared/models/book.model';
import { FormControl, FormGroup, FormArray, FormBuilder, Validators, ValidatorFn, AbstractControl } from '@angular/forms';
import { Observable } from 'rxjs';
import { startWith, map } from 'rxjs/operators';
import { Author } from '../../../shared/models/author.model';
import { AuthorService } from '../../../shared/services/author.service';
import { SeriesService } from '../../../shared/services/series.service';
import { Series } from '../../../shared/models/series.model';
import { controlNameBinding } from '@angular/forms/src/directives/reactive_directives/form_control_name';

@Component({
  selector: 'app-book-add',
  templateUrl: './book-add.component.html',
  styleUrls: ['./book-add.component.scss']
})
export class BookAddComponent implements OnInit {

  book: Book;
  series: Series[] = [];
  filteredSeries: Observable<Series[]>;
  authors: Author[] = [];
  filteredAuthors: Observable<Author[]>;
  form: FormGroup;

  constructor(private bookService: BookService,
    private authorService: AuthorService,
    private seriesService: SeriesService,
    private formBuilder: FormBuilder) { }

  ngOnInit() {
    this.initForm();
    this.book = this.initBook();
    this.getAuthors();
    if (this.bookService.editing) {
      this.book = this.bookService.currentItem;
    }
  }

  initForm() {
    this.form = this.formBuilder.group({
      title: ['', Validators.required],
      author: ['', [Validators.required, this.validateAutocomplete]],
      series: ['', this.validateAutocomplete]
    });
  }
  validateAutocomplete(control: FormControl) {
    return typeof control.value === 'string' && control.value !== '' ? {
      validateAutocomplete: {
        valid: false
      }
    } : null;
  }

  getSeries(authorId) {
    this.authorService.getSeries(authorId).subscribe(res => {
      this.series = res;
      this.filteredSeries = this.initFilteredOptionsSeries();
    });
  }
  getAuthors() {
    this.authorService.getAll('{items{id,name}}').subscribe(res => {
      this.authors = res.items;
      this.filteredAuthors = this.initFilteredOptionsAuthor();
    });
  }

  initFilteredOptionsAuthor() {
    return this.form.valueChanges
      .pipe(
        startWith(''),
        map((value: any) => value ? value.author : ''),
        map((value: Author | string) => typeof value === 'string' ? value : value.name),
        map(name => name ? this._filterAuthor(name) : this.authors.slice())
      );
  }
  authorDisplayFn = (author?: Author): string | undefined => author ? author.name : undefined;

  private _filterAuthor(name: string): Author[] {
    const filterValue = name.toLowerCase();
    return this.authors.filter(option => option.name.toLowerCase().indexOf(filterValue) === 0);
  }

  initFilteredOptionsSeries() {
    return this.form.valueChanges
      .pipe(
        startWith(''),
        map((value: any) => value ? value.series : ''),
        map((value: Series | string) => typeof value === 'string' ? value : value.title),
        map(title => title ? this._filterSeries(title) : this.series.slice())
      );
  }

  displayFn = (object, prop): string | undefined => object ? object[prop] : undefined;
  seriesDisplayFn = (series?: Series): string | undefined => series ? series.title : undefined;

  private _filterSeries(title: string): Series[] {
    const filterValue = title.toLowerCase();
    return this.series.filter(option => option.title.toLowerCase().indexOf(filterValue) === 0);
  }

  addBook() {

  }

  authorChanged(author: Author, form) {
    if (typeof (author) === 'string') {

    }
  }

  authorSelected(author: Author) {
    this.book.author = author;
    this.getSeries(author.id);
  }
  seriesSelected(series: Series) {
    this.book.series = series;
  }

  initBook(): Book {
    return {
      title: '',
      author: {
        name: ''
      },
      series: {
        title: ''
      }
    };
  }
}
