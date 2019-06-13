import { Component, OnInit } from '@angular/core';
import { BookService } from '../../../shared/services/book.service';
import { Book, BookDTO } from '../../../shared/models/backend/book.model';
import { FormControl, FormGroup, FormArray, FormBuilder, Validators, ValidatorFn, AbstractControl } from '@angular/forms';
import { Observable } from 'rxjs';
import { startWith, map } from 'rxjs/operators';
import { Author } from '../../../shared/models/backend/author.model';
import { AuthorService } from '../../../shared/services/author.service';
import { SeriesService } from '../../../shared/services/series.service';
import { Series } from '../../../shared/models/backend/series.model';
import { MatDialogRef } from '@angular/material/dialog';
import { GlobalService } from '../../../shared/services/global.service';

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
  editing = false;

  constructor(private bookService: BookService,
    private authorService: AuthorService,
    private formBuilder: FormBuilder,
    public dialogRef: MatDialogRef<BookAddComponent>) { }

  ngOnInit() {
    this.editing = this.bookService.editing;
    this.book = this.editing ? this.bookService.currentItem : this.initBook();
    if (this.book.author.id) {
      this.getSeries(this.book.author.id);
    }
    this.form = this.initForm();
    this.getAuthors();
  }

  initForm() {
    return this.formBuilder.group({
      title: [this.book.title, Validators.required],
      description: [this.book.description, Validators.required],
      author: [this.book.author, [Validators.required, this.validateAutocomplete]],
      series: [this.book.series, this.validateAutocomplete]
    });
  }
  validateAutocomplete(control: FormControl) {
    return typeof control.value === 'string' && control.value !== '' ? {
      validateAutocomplete: {
        valid: false
      }
    } : null;
  }

  getSeries(authorId: number) {
    this.authorService.getSeries(authorId).subscribe(res => {
      this.series = res;
      this.filteredSeries = this.initFilteredOptions(this.series, 'series', 'title', this.form);
    });
  }
  getAuthors() {
    this.authorService.getAll('{items{id,name}}').subscribe(res => {
      this.authors = res.items;
      this.filteredAuthors = this.initFilteredOptions(this.authors, 'author', 'name', this.form);
    });
  }

  initFilteredOptions(arrayToFilter: any[], control: string, propToFilter: string, form: FormGroup) {
    return form.controls[control].valueChanges
      .pipe(
        startWith(''),
        map(() => this._filterArray(arrayToFilter, form.get(control), propToFilter)),
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
    const series_id = this.form.value['series'].id ? this.form.value['series'].id : undefined;
    const bookDTO: BookDTO = {
      title: this.form.value['title'],
      description: this.form.value['description'],
      author_id: this.form.value['author'].id,
      series_id
    };
    this.bookService.post(bookDTO).subscribe(res => {
      this.dialogRef.close();
    });
  }

  authorSelected(author: Author) {
    if (author.id) {
      this.getSeries(author.id);
    }
  }

  initBook(): Book {
    return {
      title: '',
      description: '',
      author: {
        name: ''
      },
      series: {
        title: ''
      }
    };
  }
  checkField(elem) {
    if (typeof elem === 'string') {
      this.series = [];
      this.form.patchValue({ 'series': '' });
      this.filteredSeries = this.initFilteredOptions(this.series, 'series', 'title', this.form);
    }
  }
}
