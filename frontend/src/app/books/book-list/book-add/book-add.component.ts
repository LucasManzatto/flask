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
import { MatDialogRef } from '@angular/material/dialog';

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
    private formBuilder: FormBuilder,
    public dialogRef: MatDialogRef<BookAddComponent>) { }

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
      this.filteredSeries = this.initFilteredOptions(this.series, 'series', 'title');
    });
  }
  getAuthors() {
    this.authorService.getAll('{items{id,name}}').subscribe(res => {
      this.authors = res.items;
      this.filteredAuthors = this.initFilteredOptions(this.authors, 'author', 'name');
    });
  }

  initFilteredOptions(arrayToFilter: any[], control: string, propToFilter: string) {
    return this.form.controls[control].valueChanges
      .pipe(
        startWith(''),
        map(() => this._filterArray(arrayToFilter, this.form.get(control), propToFilter)),
      );
  }
  private _filterArray(array: any[], formControl: any, property: string): any[] {
    const element = formControl.value;
    const filterValue = (typeof element === 'string' ? element : element[property]).toLowerCase();
    return array.filter(option => option[property].toLowerCase().indexOf(filterValue) === 0);
  }

  authorDisplayFn = (author?: Author): string | undefined => author ? author.name : undefined;

  seriesDisplayFn = (series?: Series): string | undefined => series ? series.title : undefined;

  addBook() {
    this.book = { title: this.form.value['title'], author: this.form.value['author'], series: this.form.value['series'] };
    this.dialogRef.close();
  }

  authorSelected(author: Author) {
    this.book.author = author;
    this.getSeries(author.id);
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
