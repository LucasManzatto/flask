import { Component, OnInit } from '@angular/core';
import { BookService } from '../../../shared/services/book.service';
import { Book } from '../../../shared/models/book.model';
import { FormControl } from '@angular/forms';
import { Observable } from 'rxjs';
import { startWith, map } from 'rxjs/operators';
import { Author } from '../../../shared/models/author.model';
import { AuthorService } from '../../../shared/services/author.service';
import { SeriesService } from '../../../shared/services/series.service';
import { Series } from '../../../shared/models/series.model';

@Component({
  selector: 'app-book-add',
  templateUrl: './book-add.component.html',
  styleUrls: ['./book-add.component.scss']
})
export class BookAddComponent implements OnInit {

  authorFormControl = new FormControl();
  seriesFormControl = new FormControl();
  book: Book;
  series: Series[] = [];
  filteredSeries: Observable<Series[]>;
  authors: Author[] = [];
  filteredAuthors: Observable<Author[]>;
  constructor(private bookService: BookService,
    private authorService: AuthorService,
    private seriesService: SeriesService) { }

  ngOnInit() {
    this.book = this.initBook();
    this.getAuthors();
    if (this.bookService.editing) {
      this.book = this.bookService.currentItem;
    }
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
    return this.authorFormControl.valueChanges
      .pipe(
        startWith(''),
        map((value: Author) => typeof value === 'string' ? value : value.name),
        map(name => name ? this._filterAuthor(name) : this.authors.slice())
      );
  }
  authorDisplayFn = (author?: Author): string | undefined => author ? author.name : undefined;

  private _filterAuthor(name: string): Author[] {
    const filterValue = name.toLowerCase();
    return this.authors.filter(option => option.name.toLowerCase().indexOf(filterValue) === 0);
  }

  initFilteredOptionsSeries() {
    return this.seriesFormControl.valueChanges
      .pipe(
        startWith(''),
        map((value: Series) => typeof value === 'string' ? value : value.title),
        map(title => title ? this._filterSeries(title) : this.series.slice())
      );
  }
  seriesDisplayFn = (series?: Series): string | undefined => series ? series.title : undefined;

  private _filterSeries(title: string): Series[] {
    const filterValue = title.toLowerCase();
    return this.series.filter(option => option.title.toLowerCase().indexOf(filterValue) === 0);
  }

  addBook() {

  }

  authorChanged(author: Author) {
    console.log(author);
    // if (typeof (author) === 'string') {

    // }
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
